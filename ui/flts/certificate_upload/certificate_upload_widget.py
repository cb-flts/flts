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
    QDir,
    QModelIndex
)
from PyQt4.QtGui import (
    QWidget,
    QMessageBox,
    QFileDialog,
    QHeaderView,
    QLabel
)

from stdm.network.cmis_manager import (
    CmisManager,
    CmisDocumentMapperException,
    PDFViewerException
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

VIEW_IMG = ':/plugins/stdm/images/icons/flts_view_file.png'


class CertificateUploadWidget(QWidget, Ui_FltsCertUploadWidget):
    """
    Parent widget containing all the widgets for uploading the certificates.
    """

    def __init__(self, parent=None, cmis_mngr=None):
        super(CertificateUploadWidget, self).__init__(parent)
        self.setupUi(self)
        self.notif_bar = NotificationBar(
            self.vlNotification
        )
        # Disables the maximize button
        self.setWindowFlags(Qt.WindowMinimizeButtonHint)
        # Set the default status label
        self._update_status_text('Select scheme')
        self._enable_controls(False)
        # CMIS Manager
        self._cmis_mngr = cmis_mngr
        if not self._cmis_mngr:
            self._cmis_mngr = CmisManager()
        # Certificate table model
        self._cert_model = CertificateTableModel(parent=self)
        # Set the table view model
        self.tbvw_certificate.setModel(self._cert_model)
        # Certificate validator
        self._cert_validator = CertificateValidator(parent=self)
        # Uploaded items
        self._upload_items = OrderedDict()
        # Get table horizontal header count
        tbvw_h_header = self.tbvw_certificate.horizontalHeader()
        tbvw_h_header_count = tbvw_h_header.count()
        # Resize horizontal headers proportionately
        for item in range(tbvw_h_header_count):
            tbvw_h_header.setResizeMode(item, QHeaderView.Stretch)
        # Create an icon delegate for the table view
        icon_delegate = IconDelegate(self.tbvw_certificate)
        # Set icon delegate
        self.tbvw_certificate.setItemDelegate(
            icon_delegate
        )
        # Records count
        self._update_record_count()
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
        self.btn_upload_certificate.clicked.connect(
            self._on_upload_button_clicked
        )
        # Certificate upload flag
        self._can_upload = False
        self.cert_upload_handler_items = OrderedDict()
        # Flag for checking if there is an active upload
        self._has_active_operation = False
        if self._has_active_operation:
            msg_box = QMessageBox()
            msg_box.warning(
                self,
                self.tr('Certificate Upload Close'),
                self.tr(
                    'Are you sure you want to exit the certificate upload?'
                )
            )
        self._idx = QModelIndex()
        self._lbl_idx_prop = 'label_index'

    @property
    def has_active_operation(self):
        """
        :return: Returns True if there is an ongoing upload or removal of
        document.
        :rtype: bool
        """
        return self._has_active_operation

    def create_hyperlink_widget(self, img_src, lbl_index):
        """
        Creates a clickable QLabel widget that appears like a hyperlink.
        :param img_src: Image source.
        :type img_src: str
        :return: Returns the QLabel widget with appearance of a hyperlink.
        :rtype: QLabel
        """
        lbl_link = QLabel()
        lbl_link.setAlignment(Qt.AlignHCenter)
        lbl_link.setText(
            '<a href="placeholder"><img src=\'{0}\'/></a>'.format(
                img_src
            )
        )
        lbl_link.setTextInteractionFlags(Qt.TextBrowserInteraction)
        lbl_link.setProperty(self._lbl_idx_prop, lbl_index)
        lbl_link.linkActivated.connect(
            self._on_view_activated
        )
        return lbl_link

    def _on_view_activated(self):
        """
        Slot raised when the view link is clicked on the table widget.
        """
        view_label = self.sender()
        if not view_label:
            return

        idx = view_label.property(self._lbl_idx_prop)

        try:
            cert_items = self._cert_model.cert_info_items
            cert_info = cert_items[idx.row()]
            path = str(cert_info.filename)
            cert_num = cert_info.certificate_number
            upload_handler = self.cert_upload_handler_items[
                cert_num
            ]
            cert_uuid = upload_handler.certificate_uuid(path)
            cert_name = upload_handler.certificate_name(path)
            pdf_viewer = PDFViewerWidget(cert_uuid, cert_name, self)
            pdf_viewer.view_document()
        except KeyError:
            msg = self.tr(
                'The certificate {} cannot be previewed'.format(cert_num)
            )
            self.show_error_message(msg)

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
        else:
            self.cbo_scheme_number.setEnabled(True)
            self._populate_schemes()

    def _enable_controls(self, enable):
        """
        Enable or disable user interface controls.
        :param enable: Status of the controls.
        :type enable: bool
        """
        self.btn_select_folder.setEnabled(enable)
        self.cbo_scheme_number.setEnabled(enable)
        self.btn_upload_certificate.setEnabled(enable)

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
                'No schemes in the database.'
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
        self.cert_upload_handler_items.clear()
        self._cert_model.clear()
        self._update_record_count()
        if self.cbo_scheme_number.currentText():
            self.btn_select_folder.setEnabled(True)
            self.tbvw_certificate.setEnabled(True)
            self._update_status_text('Select certificates folder')
            self.notif_bar.clear()
            self._update_record_count()
        else:
            self.btn_select_folder.setEnabled(False)
            self._update_status_text('Select scheme')

    def _on_select_folder(self):
        """
        Slot raised when the select folder button is clicked.
        """
        scan_cert_path = scanned_certificate_path()
        if not scan_cert_path:
            scan_cert_path = '~/'
        cert_dir = QFileDialog.getExistingDirectory(
            self,
            "Browse Certificates Source Folder",
            scan_cert_path,
            QFileDialog.ShowDirsOnly
        )
        # Check if selected directory is mapped
        if cert_dir:
            if cert_dir != scan_cert_path:
                # Clear model and Temp CMIS folder
                self._cert_model.clear()
                if len(self.cert_upload_handler_items) > 0:
                    for k, v in self.cert_upload_handler_items.iteritems():
                        v.remove_certificate(
                            k.filename
                        )
                # Set path to the scanned certificate directory
                set_scanned_certificate_path(cert_dir)
                # Get certificate info items from directory
                cert_info_items = self._cert_info_from_dir(cert_dir)
                # Populate cert info items
                self._populate_cert_info_items(cert_info_items)
            else:
                if self._cert_model.rowCount() == 0:
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
                'There are no PDF files in the selected directory.'
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
        # Add view icon for each row in table view
        for cert in cert_info_items:
            cert_idx = cert_info_items.index(cert)
            tbl_idx = self.tbvw_certificate.model().index(cert_idx, 2)
            self._insert_view_label(
                tbl_idx
            )

        self._update_record_count()

        # Validation function call
        self._validate_items(cert_info_items)

    def _insert_view_label(self, index):
        """
        Adds the view icon to the table view when populating the certificates.
        :param index: Index used to locate data in the table view model.
        :type index: QModelIndex
        """
        self.tbvw_certificate.setIndexWidget(
            index,
            self.create_hyperlink_widget(VIEW_IMG, index)
        )

    def _update_record_count(self):
        """
        Update the number of records loaded in the view.
        """
        rec_count = self._cert_model.rowCount()
        self.lbl_records_count.setText(
            '{0} files'.format(rec_count)
        )

    def _update_status_text(self, status_text):
        """
        Update the status label text informing the user of the status for the
        certificate upload.
        """
        self.lbl_status.setText('Status: ' + status_text)

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
        self._has_active_operation = True
        self._update_status_text('Validating...')

    def _on_cert_info_validated(self, cert_info):
        """
        Slot raised when the certificate info item has been validated.
        :param cert_info: Validated certificate info object.
        """
        # Update the validation status icon and tooltip
        self._cert_model.update_validation_status(
            cert_info.certificate_number
        )

        # Upload only if status is can upload
        if cert_info.validation_status == CertificateInfo.CAN_UPLOAD:
            self._can_upload = True
            # Upload the certificate to the Temp CMIS folder
            self._upload_certificate(cert_info)

    def _on_validation_complete(self):
        """
        Slot raised when the validation is complete.
        """
        doc_count = str(self._cert_model.rowCount())
        msg = ' certificates have been validated'
        QMessageBox.information(
            self,
            self.tr('Certificate Upload'),
            self.tr(doc_count + msg)
        )
        self._has_active_operation = False

        if self._can_upload:
            self.btn_upload_certificate.setEnabled(True)
            self._update_status_text('Ready to upload')

    def _upload_certificate(self, cert_info):
        """
        Updates the certificate upload handler. Upload the certificate to
        the Temp folder in CMIS document repository.
        :param cert_info: Certificate upload handler.
        :type cert_info: CertificateUploadHandler
        """
        upload_handler = CertificateUploadHandler(
            cmis_mngr=self._cmis_mngr,
            parent=self
        )
        self.cert_upload_handler_items[cert_info.certificate_number] = upload_handler
        upload_handler.upload_certificate(
            str(cert_info.filename))

    def _on_upload_button_clicked(self):
        """
        Slot raised when the upload button is clicked.
        """
        self._persist_certificate()

    def _persist_certificate(self):
        """
        Moves the certificates from the Temp folder to the permanent CMIS
        folder.
        """
        for num, handler in self.cert_upload_handler_items.iteritems():
            cert_num = str(num).replace('/', '.')
            handler.persist_certificate(cert_num)

    def _clear_uploaded_items(self):
        """
        Clears uploaded items from the CMIS Temp folder.
        """
        cert_items = self._cert_model.cert_info_items

    def show_error_message(self, message):
        """
        Show custom error message depending on the process.
        :param message: Error message to be shown.
        :type message: str
        """
        QMessageBox.critical(
            self,
            self.tr('Certificate Upload Error'),
            self.tr(message)
        )

    def closeEvent(self, event):
        self._on_close()

    def _on_close(self):
        """
        Slot raised when the close button is clicked.
        """
        # Default combo box index
        self.cbo_scheme_number.setCurrentIndex(0)
        # Clear the model and validation items
        self._cert_model.clear()
        self._update_record_count()
        self._cert_validator.clear()
        self._clear_uploaded_items()
        # Clear the document view labels
        self.lbl_link = QLabel()
        # Close the widget
        self.close()
