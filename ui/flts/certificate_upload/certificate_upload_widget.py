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
from PyQt4.QtGui import (
    QWidget,
    QMessageBox,
    QFileDialog,
    QDirModel
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
from ui_flts_certificate_upload import Ui_FltsCertUploadWidget


class CertificateUploadWidget(QWidget, Ui_FltsCertUploadWidget):
    """
    Parent widget containing all the widgets for uploading the certificates.
    """
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.setupUi(self)
        self.notif_bar = NotificationBar(
            self.vlNotification
        )
        self._cmis_mngr = CmisManager()
        self._check_cmis_connection()

        self._cert_model = CertificateTableModel()
        self._cert_upload = CertificateUploadHandler()
        self._cert_validator = CertificateValidator()

        self.btn_close.clicked.connect(self.close)

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
            self._enable_controls(True)
            self._populate_schemes()

    def show_error_message(self, message):
        """
        Show custom error message depending on the process.
        :param message: Error message to be shown.
        :type message: str
        """
        QMessageBox.critical(
            self,
            self.tr(
                'Error'
            ),
            message
        )

    def _enable_controls(self, enable):
        """
        Enable or disable UI controls.
        :param enable: Status of the controls.
        :type enable: bool
        """
        self.btn_select_folder.setEnabled(enable)
        self.cbo_scheme_number.setEnabled(enable)
        self.btn_upload_certificate.setEnabled(enable)

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

    def load_certificates_from_folder(self, folder):
        """
        Get the path of the folder containing the certificates.
        :param folder: Folder containing the certificates.
        :type folder: str
        :return: Returns the name of the folder containing the certificates.
        :rtype: str
        """
        if not folder:
            folder = QFileDialog.getExistingDirectory(
                self,
                caption="Browse Certificates Source Folder"
            )

        return str(folder)

    def _populate_table_view(self, filename):
        """
        Populate table view with the list of certificates that have been
        loaded from the folder.
        :param filename: List of certificates in the folder.
        :type filename: list
        """

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


