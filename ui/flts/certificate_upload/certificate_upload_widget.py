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
    QDir
)
from PyQt4.QtGui import (
    QWidget,
    QMessageBox,
    QFileDialog,
    QStandardItem
)

from stdm.network.cmis_manager import (
    CmisManager,
    CmisDocumentMapperException
)
from stdm.data.pg_utils import export_data

from stdm.ui.notification import NotificationBar, ERROR
from stdm.ui.flts.certificate_upload.certificate_table_model import CertificateTableModel
from stdm.ui.flts.certificate_upload.certificate_upload_handler import CertificateUploadHandler
from stdm.ui.flts.certificate_upload.certificate_validator import CertificateValidator
from stdm.ui.flts.certificate_upload.ui_flts_certificate_upload import Ui_FltsCertUploadWidget

VIEW_IMG = ':/plugins/stdm/images/icons/flts_view_file.png'
# TODO Set Icon sizes to 16 x 16


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
        self._cmis_mngr = CmisManager()

        self._cert_model = CertificateTableModel()
        self._cert_upload = CertificateUploadHandler()
        self._cert_validator = CertificateValidator()

        self._enable_controls(False)

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

        # self.btn_upload_certificate.clicked.connect()
        self.btn_close.clicked.connect(self.close)

        self._cert_model.clear()

        # std = QStandardItem('hempire', 'fiona', 'faith', 'george')
        #TODO Test with a raw model

        self.tbvw_certificate.setModel(std)

    def _enable_controls(self, enable):
        """
        Enable or disable UI controls.
        :param enable: Status of the controls.
        :type enable: bool
        """
        self.btn_select_folder.setEnabled(enable)
        self.cbo_scheme_number.setEnabled(enable)
        self.btn_upload_certificate.setEnabled(enable)
        self.tbvw_certificate.setEnabled(enable)

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
        Populate the combobox with items from the database
        """
        # Clear combobox
        self.cbo_scheme_number.clear()
        self.cbo_scheme_number.addItem('')
        # Get scheme table data
        schm_data = export_data('cb_scheme')
        # Check if no schemes loaded
        if schm_data is None:
            msg = self.tr(
                'Schemes could not be loaded.'
            )
            self.show_error_message(msg)
        else:
            # Loop through result proxy to get scheme number and add to
            # combobox
            for s in schm_data:
                self.cbo_scheme_number.addItem(s.scheme_number, s.id)
            # Sort region combobox items
            self.cbo_scheme_number.model().sort(0)

    def on_cbo_scheme_changed(self):
        """
        Slot raised when the scheme selection combobox is changed.
        """
        if not self.cbo_scheme_number.currentText():
            self.btn_select_folder.setEnabled(False)
        else:
            self.btn_select_folder.setEnabled(True)

    def on_select_folder(self):
        """
        Slot raised when the select folder button is clicked
        """
        # Check if combobox has scheme selected.
        if not self.cbo_scheme_number.currentText():
            self.notif_bar.clear()
            self.notif_bar.insertWarningNotification(
                self.tr(
                    "Scheme value must be selected first."
                )
            )
        else:
            cert_dir = QFileDialog.getExistingDirectory(
                self,
                caption="Browse Certificates Source Folder"
            )
            return cert_dir

    def certificate_name_from_directory(self, cert_name):
        """
        Get certificate name from the selected directory.
        :param cert_name: Name of the certificate in the selected directory.
        :type cert_name: Str
        :return: Returns the name of the certificate in the directory.
        :rtype: Str
        """
        pdf_filter = '.pdf'
        # Get a list of files in the directory
        file_info = QDir(self.on_select_folder()).entryInfoList(
            QDir.NoDot | QDir.NoDotDot | QDir.Files
        )
        # Get list of file names from the selected directory
        file_name = [cert.fileName() for cert in file_info]
        # Check if list contains file names
        if len(file_name) == 0:
            msg = self.tr(
                'There are no files in the selected directory.'
            )
            self.show_error_message(msg)
        elif len(file_name) > 0:
            # Check if list contains PDF files
            if not any(pdf_filter in string for string in file_name):
                msg = self.tr(
                    'There are no PDF files in the selected directory.'
                )
                self.show_error_message(msg)
            else:
                for file_ in file_name:
                    if not cert_name:
                        # Assign variable to file name without PDF extension
                        cert_name = file_.split(pdf_filter)[0]

                return cert_name

    def _populate_table_view(self, filenames):
        """
        Populate table view with the list of certificates that have been
        loaded from the folder.
        :param filenames: List of certificates in the folder.
        :type filenames: list
        """
        # Clear previous items in the model.
        self._cert_model.clear()
        if not filenames:
            filenames = []

        for file_ in filenames:
            filenames.append(
                self.certificate_name_from_directory(file_)
                )
        model = QStandardItemModel(filenames)
        self._cert_model.setModel(model)

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

    def _validate_items(self, cert_info):
        """
        Validate list of certificate items loaded in the  table view.
        :param cert_info: List of certificate items in the table view.
        :type cert_info: list
        """
        pass

    def _on_cert_info_uploaded(self, cert_info):
        """
        :param cert_info:
        :return:
        """
        pass

    def _on_upload_certificates(self):
        """
        :return:
        """
        pass

    def _upload_certificates(self, cert_info):
        """
        Initiates upload session of list of certificate info objects by
        calling the upload method in certificate upload handler.
        :param cert_info: List of certificate items to be uploaded.
        :type cert_info: list
        """
        pass

    def check_validation_status(self):
        """
        Checks the validation status of the certificates
        """

    def validate(self):
        """
        Validate certificates
        """

    def _on_cert_info_validated(self, cert_info):
        """
        Slot raised when the certificate info item has been validated.
        :param cert_info:
        """

    def _update_status_icons(self):
        """
        Update the icons in the table widget based on the status of
        upload.
        """

    def _update_status_description(self):
        """
        Update the icons in the table widget based on the status of
        upload.
        """
