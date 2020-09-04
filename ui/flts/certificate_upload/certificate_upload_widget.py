"""
/***************************************************************************
Name                 : Certificate upload widget
Description          : Widget for uploading certificates.
Date                 : 30/May/2020
copyright            : (C) 2020 by UN-Habitat and implementing partners.
                       See the accompanying file CONTRIBUTORS.txt in the root
email                : stdm@unhabitat.org
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from collections import OrderedDict
from PyQt4.QtCore import (
    Qt,
    QDir
)
from PyQt4.QtGui import (
    QWidget,
    QMessageBox,
    QFileDialog,
    QHeaderView
)

from stdm.network.cmis_manager import (
    CmisManager,
    CmisDocumentMapperException
)
from stdm.settings.registryconfig import (
    scanned_certificate_path,
    set_scanned_certificate_path
)
from stdm.data.pg_utils import export_data

from stdm.ui.notification import NotificationBar, ERROR
from stdm.ui.flts.certificate_upload.certificate_table_model import CertificateTableModel
from stdm.ui.flts.certificate_upload.certificate_upload_handler import CertificateUploadHandler
from stdm.ui.flts.certificate_upload.certificate_validator import CertificateValidator
from stdm.ui.flts.certificate_upload.ui_flts_certificate_upload import Ui_FltsCertUploadWidget
from stdm.ui.flts.certificate_upload.certificate_info import CertificateInfo
from stdm.ui.flts.workflow_manager.pdf_viewer_widget import PDFViewerWidget
from stdm.ui.flts.certificate_upload.delegate import IconDelegate


class CertificateUploadWidget(QWidget, Ui_FltsCertUploadWidget):
    """
    Parent widget containing all the widgets for uploading the certificates.
    """

    def __init__(self, parent=None):
        super(CertificateUploadWidget, self).__init__(parent)
        self.setupUi(self)
        self.notif_bar = NotificationBar(
            self.vlNotification
        )
        # Disables the maximize button
        self.setWindowFlags(Qt.WindowMinimizeButtonHint)
        # Set the labels text
        self._status_txt = self.lbl_status.text()
        self.lbl_status.setText(self._status_txt + 'Select scheme')
        # CMIS Manager
        self._cmis_mngr = CmisManager()
        # Certificate table model
        self._cert_model = CertificateTableModel(parent=self)
        # Set the table view model
        self.tbvw_certificate.setModel(self._cert_model)
        # Certificate validator
        self._cert_validator = CertificateValidator(parent=self)
        # Uploaded items
        self._upload_items = OrderedDict()
        self._lbl_records_txt = self.lbl_records_count.text()
        self.lbl_records_count.setText(
            str(self._cert_model.rowCount()) + self._lbl_records_txt
        )
        # Get table horizontal header count
        tbvw_h_header = self.tbvw_certificate.horizontalHeader()
        tbvw_h_header_count = tbvw_h_header.count()
        # Resize horizontal headers proportionately
        for item in range(tbvw_h_header_count):
            tbvw_h_header.setResizeMode(item, QHeaderView.Stretch)
        # Create an icon delegate for the table view
        icon_delegate = IconDelegate(self.tbvw_certificate)
        # Set icon delagate
        self.tbvw_certificate.setItemDelegate(
            icon_delegate
        )
        # All controls disabled by default
        self._enable_controls(False)
        # Check connection to CMIS repository
        self._check_cmis_connection()
        # Connecting signals
        self.cbo_scheme_number.currentIndexChanged.connect(
            self._on_cbo_scheme_changed
        )
        self.btn_select_folder.clicked.connect(
            self._on_select_folder
        )
        self._cert_validator.validated.connect(
            self._on_cert_info_validated
        )
        self._cert_validator.validation_completed.connect(
            self._on_validation_complete
        )
        self.btn_close.clicked.connect(
            self._on_close
        )

    def _enable_controls(self, enable):
        """
        Enable or disable user interface controls.
        :param enable: Status of the controls.
        :type enable: bool
        """
        self.btn_select_folder.setEnabled(enable)
        self.cbo_scheme_number.setEnabled(enable)
        self.btn_upload_certificate.setEnabled(enable)

    def _check_cmis_connection(self):
        """
        Checks whether there is connection to the cmis repository.
        :return: Returns true if the connection exists and false if there is
        no connection.
        :rtype: bool
        """
        if not self._cmis_mngr.connect():
            msg = self.tr(
                'Failed to connect to the CMIS Service.'
            )
            self.show_error_message(msg)
            self._enable_controls(False)
        else:
            self.cbo_scheme_number.setEnabled(True)
            self._populate_schemes()

    def _populate_schemes(self):
        """
        Populate the schemes combobox with items from the database.
        """
        # Clear combobox
        self.cbo_scheme_number.clear()
        self.cbo_scheme_number.addItem('')
        # Get scheme table data
        sch_data = export_data('cb_scheme')
        # Check if no schemes loaded
        if not sch_data:
            msg = self.tr(
                'Schemes could not be loaded.'
            )
            self.show_error_message(msg)
        else:
            # Loop through result proxy to get scheme number and add to
            # combobox
            for s in sch_data:
                self.cbo_scheme_number.addItem(s.scheme_number, s.id)
            # Sort region combobox items
            self.cbo_scheme_number.model().sort(0)

    def _on_cbo_scheme_changed(self):
        """
        Slot raised when the scheme selection combobox is changed.
        """
        if not self.cbo_scheme_number.currentText():
            self.btn_select_folder.setEnabled(False)
            self.lbl_status.setText(self._status_txt + 'Select scheme')
        else:
            self.btn_select_folder.setEnabled(True)
            self.tbvw_certificate.setEnabled(True)
            self.lbl_status.setText(
                self._status_txt + 'Select certificates folder')

    def _on_select_folder(self):
        """
        Slot raised when the select folder button is clicked.
        """
        scan_cert_path = scanned_certificate_path()
        if not scan_cert_path:
            scan_cert_path = '~/'
        # Check if combobox has scheme selected.
        if not self.cbo_scheme_number.currentText():
            self.notif_bar.clear()
            self.notif_bar.insertWarningNotification(
                self.tr(
                    "Scheme name must be selected first."
                )
            )
        else:
            cert_dir = QFileDialog.getExistingDirectory(
                self,
                "Browse Certificates Source Folder",
                scan_cert_path,
                QFileDialog.ShowDirsOnly
            )
            # Check if directory is selected
            if cert_dir:
                # Set path to the scanned certificate directory
                set_scanned_certificate_path(cert_dir)
                # Get certificate info items from directory
                cert_info_items = self._cert_info_from_dir(cert_dir)
                # Populate cert info items
                self._populate_cert_info_items(cert_info_items)

    def _cert_info_from_dir(self, path):
        """
        Create certificate info items from the user selected directory.
        :return: cert_info_items: List of certificate info items.
        :rtype cert_info_items: list
        """
        dir_ = QDir(path)
        dir_.setNameFilters(['*.pdf'])
        file_infos = dir_.entryInfoList(
            QDir.NoDot | QDir.NoDotDot | QDir.Files | QDir.Name
        )
        # Check if list contains file names
        cert_info_items = []
        if len(file_infos) == 0:
            msg = self.tr(
                'There are no files in the selected directory.'
            )
            self.show_error_message(msg)
            self._cert_model.clear()
        else:
            # Loop through file info objects
            for f in file_infos:
                # Create certificate info object for each file
                cert_info = CertificateInfo()
                cert_info.filename = f.absoluteFilePath()
                base_name = f.completeBaseName()
                cert_info.certificate_number = base_name.replace('.', '/')
                cert_info_items.append(cert_info)

        return cert_info_items

    def _populate_cert_info_items(self, cert_info_items):
        """
        Populate the table widget with the file info items from the selected
        directory.
        :param cert_info_items: List of file info items fom the selected
        directory.
        :type cert_info_items: list
        """
        self._cert_model.cert_info_items = cert_info_items

        # Check if certificate items is empty
        if len(cert_info_items) == 0:
            self.notif_bar.clear()
            self.notif_bar.insertWarningNotification(
                self.tr(
                    "There are no certificates to be uploaded."
                )
            )
            return

        self._show_record_count()

        # Validation function call
        self._validate_items(cert_info_items)

    def _show_record_count(self):
        """
        Show the number of records loaded in the view.
        """
        self.lbl_records_count.setText(
            str(self._cert_model.rowCount()) + self._lbl_records_txt
        )

    def _validate_items(self, cert_info_items):
        """
        Validate list of certificate items loaded in the table view.
        :param cert_info_items: List of certificate items in the table view.
        :type cert_info_items: list
        """
        # Set certificate info items
        self._cert_validator.cert_info_items = cert_info_items

        # Initiate validation process
        self._cert_validator.start()

        self.lbl_status.setText(self._status_txt + 'Validating...')

    def _on_cert_info_validated(self, cert_info):
        """
        Slot raised when the certificate info item has been validated.
        :param cert_info: Validated certificate info object.
        """
        # Update the validation status icon and tooltip
        self._cert_model.update_validation_status(
            cert_info.certificate_number
        )
        upload_handler = CertificateUploadHandler(
            cmis_mngr=self._cmis_mngr,
            parent=self
        )

        # Upload only if status is can upload
        if cert_info.validation_status == CertificateInfo.CAN_UPLOAD:
            self._upload_certificates(
                cert_info.filename,
                upload_handler
            )

        # Populate upload items
        self._populate_uploaded_items(
            cert_info, upload_handler
        )

    def _on_validation_complete(self):
        """
        Slot raised when the validation is complete.
        """
        # Get loaded certificates from the model
        cert_info_items = self._cert_model.cert_info_items

        # Create an empty list to store certificate statuses
        status_res = []
        for cert in cert_info_items:
            status = cert.validation_status
            status_res.append(status)

        can_upload = CertificateInfo.CAN_UPLOAD

        # Check if any of the loaded certificates can be uploaded
        if can_upload not in status_res:
            self.btn_upload_certificate.setEnabled(False)
            self.lbl_status.setText(self._status_txt + 'Cannot upload')
        else:
            self.btn_upload_certificate.setEnabled(True)
            self.lbl_status.setText(self._status_txt + 'Ready to upload')

    def _upload_certificates(self, filepath, uploader):
        """
        Upload the certificates to the Temp folder in CMIS document
        repository.
        :param filepath: The path to the certificate document.
        :type filepath: str
        :param uploader: Certificate upload handler.
        :type uploader: CertificateUploadHandler
        """
        uploader.upload_certificate(filepath)

    def _populate_uploaded_items(self, cert_info, uploader):
        """
        Map the uploaded items to their corresponding upload handlers.
        :param cert_info: Certificate info items of the uploaded certificate.
        :type cert_info: CertificateInfo
        :param uploader: Certificate upload handler.
        :type uploader: CertificateUploadHandler
        """
        self._upload_items.update({cert_info: uploader})

        self.btn_upload_certificate.clicked.connect(
            lambda: self._on_upload_button_clicked(
                self._upload_items
            )
        )

        self.btn_close.clicked.connect(
            self._on_close
        )
        self.tbvw_certificate.clicked.connect(
            self._on_preview_certificate
        )

    def _on_upload_button_clicked(self, upload_items):
        """
        Slot raised when the upload button is clicked.
        """
        for k, v in upload_items.iteritems():
            cert_number = str(k.certificate_number).replace('/', '.')
            upload_handler = v
            upload_handler.persist_certificates(
                cert_number
            )

    def _on_preview_certificate(self, index):
        """
        Slot raised when the view icon in the table view is clicked.
        :param index: Model index of the table view model.
        :type index: QModelIndex
        """
        cert_items = self._cert_model.cert_info_items
        cert_info = cert_items[index.row()]
        path = cert_info.filename

        items_list = []
        for handler in self._upload_items.iteritems():
            doc_uuid = handler[1].certificate_uuid(path)
            doc_name = handler[1].certificate_name(path)
            items_list.append(doc_uuid)
            items_list.append(doc_name)

        if index.isValid():
            if index.column() == 2:
                self.notif_bar.clear()
                path = cert_info.filename
                validation_status = cert_info.validation_status
                if validation_status != CertificateInfo.CAN_UPLOAD:
                    msg = '{0} could not be found in the list of validated ' \
                                  '/ uploaded documents'.format(cert_info.certificate_number)
                    self.notif_bar.insertWarningNotification(msg)

                pdf_viewer = PDFViewerWidget(
                    items_list[0], items_list[1]
                )
                pdf_viewer.view_document()

    def _on_cert_info_uploaded(self, cert_path):
        """
        Slot raised when the certificate info item has been uploaded to the
        CMIS Temp folder.
        :param cert_path: Path to the certificate document.
        :type cert_path: str
        """

    def _on_upload_complete(self):
        """
        Slot raised when all the certificates have been uploaded.
        """
        pass

    def show_error_message(self, message):
        """
        Show custom error message depending on the process.
        :param message: Error message to be shown.
        :type message: str
        """
        QMessageBox.critical(
            self,
            self.tr('Certificate Upload Error'),
            message
        )

    def _on_close(self):
        """
        Slot raised when the close button is clicked.
        """
        # Reset labels
        self.lbl_status.setText(
            self._status_txt + 'Select Folder'
        )

        # Reset combobox index
        self.cbo_scheme_number.setCurrentIndex(0)

        # Clear the model and validation items
        self._cert_model.clear()
        self._show_record_count()
        self._cert_validator.clear()

        if len(self._upload_items) > 0:
            for k, v in self._upload_items.iteritems():
                v.remove_certificate(
                    k.filename
                )

        # Close the widget
        self.close()

    def closeEvent(self, event):
        self._on_close()

