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
from PyQt4.QtCore import (
    Qt,
    QDir
)
from PyQt4.QtGui import (
    QWidget,
    QMessageBox,
    QFileDialog,
    QStandardItem,
    QIcon,
    QProgressDialog,
    QProgressBar,
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

        # Set the certificate status text label
        self._status_txt = self.lbl_status.text()

        # CMIS Manager
        self._cmis_mngr = CmisManager()
        # Certificate table model
        self._cert_model = CertificateTableModel(parent=self)
        # Set the table view model
        self.tbvw_certificate.setModel(self._cert_model)
        # Certificate validator
        self._cert_validator = CertificateValidator(parent=self)
        # Certificate upload handler
        self._cert_upload_handler = CertificateUploadHandler(
            cmis_mngr=self._cmis_mngr,
            parent=self
        )

        # Get table horizontal header count
        tbvw_h_header = self.tbvw_certificate.horizontalHeader()
        tbvw_h_header_count = tbvw_h_header.count()

        # Resize horizontal headers proportionately
        for item in range(tbvw_h_header_count):
            tbvw_h_header.setResizeMode(item, QHeaderView.Stretch)

        # All controls disabled by default
        self._enable_controls(False)

        # Check connection to CMIS repository
        self._check_cmis_connection()

        # Connecting signals
        self.cbo_scheme_number.currentIndexChanged.connect(
            self.on_cbo_scheme_changed
        )
        self.btn_select_folder.clicked.connect(
            self.on_select_folder
        )
        self.btn_upload_certificate.clicked.connect(
            self._on_upload_certificates
        )
        self._cert_validator.validated.connect(
            self._on_cert_info_validated
        )
        self._cert_validator.validation_completed.connect(
            self._on_validation_complete
        )
        self._cert_upload_handler.uploaded.connect(
            self._on_cert_info_uploaded
        )
        self._cert_upload_handler.upload_completed.connect(
            self._on_upload_complete
        )
        self._cert_upload_handler.persisted.connect(
            self._on_persist_certificates
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

    def on_cbo_scheme_changed(self):
        """
        Slot raised when the scheme selection combobox is changed.
        """
        if not self.cbo_scheme_number.currentText():
            self.btn_select_folder.setEnabled(False)
            self.lbl_status.setText(self._status_txt)
        else:
            self.btn_select_folder.setEnabled(True)
            self.tbvw_certificate.setEnabled(True)
            self.lbl_status.setText(
                self._status_txt + 'Select certificates folder')

    def on_select_folder(self):
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
                cert_info.certificate_number = f.completeBaseName()
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
        # Show/update record count
        record_count = 'Number of files: ' + str(
            self._cert_model.rowCount()
        )

        self.lbl_records_count.clear()

        self.lbl_records_count.setText(record_count)

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
        # Upload certificates
        if cert_info.validation_status == CertificateInfo.CAN_UPLOAD:
            self._upload_certificates(cert_info.filename)

    def _upload_certificates(self, filepath):
        """
        Upload the certificates to the Temp folder in CMIS document repository
        :param filepath: Location path of the certificate
        """
        self._cert_upload_handler.upload_certificate(
            filepath
        )

    def _on_cert_info_uploaded(self, cert_info):
        """
        Slot raised when the certificate info item has been uploaded.
        :param cert_info: Certificate info object.
        :type cert_info: CertificateInfo
        """
        # Update upload status text and icon
        self._cert_model.update_upload_status(
            cert_info.certificate_number
        )

    def _on_upload_complete(self):
        """
        Slot raised when all the certificates have been uploaded.
        """
        pass

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
        else:
            self.btn_upload_certificate.setEnabled(True)

        self.lbl_status.setText(self._status_txt + 'Ready to upload')

    def _on_upload_certificates(self):
        """
        Slot raised when the upload button is clicked.
        """
        # Set status label
        self.lbl_status.setText(
            self._status_txt + 'Uploading certificates...'
        )

        cert_info_items = self._cert_model.cert_info_items

        # Check if certificate items is empty
        if len(cert_info_items) == 0:
            self.notif_bar.clear()
            self.notif_bar.insertWarningNotification(
                self.tr(
                    "There are no certificates to be uploaded."
                )
            )
            return

        try:
            cert_numbers = iter(
                [str(cert.certificate_number) for cert in cert_info_items]
            )

            # Loop though the iterator
            self._cert_upload_handler.persist_certificates(
                    next(cert_numbers)
            )

        except (IOError, OSError, Exception) as e:
            self.show_error_message(
                "Failed to upload: {}".format(e)
            )

    def _on_persist_certificates(self):
        """
        Slot raised when certificates have been moved from the temp folder to
        the permanent folder in the document repository.
        """
        self.notif_bar.clear()
        msg = self.tr(
            "Certificates have been uploaded."
        )
        self.notif_bar.insertSuccessNotification(msg)

    def show_error_message(self, message):
        """
        Show custom error message depending on the process.
        :param message: Error message to be shown.
        :type message: str
        """
        QMessageBox.critical(
            self,
            self.tr(
                'Certificate Upload Error'
            ),
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
        self._cert_upload_handler.reset()
        # Close the widget
        self.close()

    def closeEvent(self, event):
        self._on_close()

