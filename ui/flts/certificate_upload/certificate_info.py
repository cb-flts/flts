"""
/***************************************************************************
Name                 : CertificateInfo
Description          : Container with the details of the certificate
                       validation process.
Date                 : 25/May/2020
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

from PyQt4.QtGui import QIcon


class CertificateInfo(object):
    """
    Container with the details of the certificate validation process.
    """
    # Validation status
    CAN_UPLOAD, CANNOT_UPLOAD, UNDEFINED = range(0, 3)

    # Upload status
    NOT_UPLOADED, SUCCESS, ERROR = range(0, 3)

    def __init__(self, **kwargs):
        self.upload_status = CertificateInfo.UNDEFINED
        self.validation_status = CertificateInfo.NOT_UPLOADED
        self.certificate_number = kwargs.pop('certificate_number', '')
        self.validation_description = kwargs.pop('validation_description', '')
        self.upload_description = kwargs.pop('upload_description', '')
        self.filename = kwargs.pop('filename', '')
        # Icons representing state of the certificate
        self.icons = {
            'error': QIcon(":/plugins/stdm/images/icons/flts_error.png"),
            'warning': QIcon(":/plugins/stdm/images/icons/warning.png"),
            'success': QIcon(":/plugins/stdm/images/icons/success.png")
        }

    def cert_upload_status(self):
        """
        Returns upload status description of the certificate corresponding to
        the upload status value.
        :return: Returns the certificate upload description.
        :rtype: str
        """
        status = self.upload_status
        upload_desc = self.upload_description
        if status == CertificateInfo.CANNOT_UPLOAD:
            upload_desc = 'Cannot upload'
        elif status == CertificateInfo.SUCCESS:
            upload_desc = 'Successfully uploaded'

        return upload_desc

    def cert_validation_status(self):
        """
        Returns validation status description of the certificate corresponding
        to the validation status value.
        :return: Returns the certificate validation description.
        :rtype: str
        """
        status = self.validation_status
        valid_desc = self.validation_description
        if status == CertificateInfo.CANNOT_UPLOAD:
            valid_desc = 'Cannot Upload'
        elif status == CertificateInfo.CAN_UPLOAD:
            valid_desc = 'Can Upload'

        return valid_desc

    def upload_status_icon(self):
        """
        Returns validation status icon of the certificate corresponding
        to the validation status value.
        :return: Returns the upload status icon.
        :rtype: QIcon, str
        """
        upload_icon = None
        upload_status = self.upload_status
        if upload_status == CertificateInfo.ERROR:
            upload_icon = self.icons.get('error')
        elif upload_status == CertificateInfo.SUCCESS:
            upload_icon = self.icons.get('success')

        return upload_icon

    def validation_status_icon(self):
        """
        Returns validation status icon of the certificate corresponding
        to the validation status value.
        :return: Returns the validation status icon.
        :rtype: QIcon, str
        """
        validation_icon = None
        validation_status = self.validation_status
        if validation_status == CertificateInfo.CANNOT_UPLOAD:
            validation_icon = self.icons.get('warning')
        elif validation_status == CertificateInfo.CAN_UPLOAD:
            validation_icon = self.icons.get('success')

        return validation_icon
