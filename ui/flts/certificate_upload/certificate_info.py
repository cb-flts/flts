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
        self.certificate_number = kwargs.pop('certificate_number', '')
        self.validation_description = kwargs.pop('validation_description', '')
        self.upload_description = kwargs.pop('upload_description', '')
        self.filename = kwargs.pop('filename', '')
        self.validation_status = kwargs.pop('Undefined', CertificateInfo.UNDEFINED)
        self.upload_status = kwargs.pop('Not Uploaded', CertificateInfo.NOT_UPLOADED)
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
        if self.upload_status == CertificateInfo.ERROR:
            self.upload_description = 'Error'
            return self.upload_description
        elif self.upload_status == CertificateInfo.SUCCESS:
            self.upload_description = 'Success'
            return self.upload_description

    def cert_validation_status(self):
        """
        Returns validation status description of the certificate corresponding
        to the validation status value.
        :return: Returns the certificate validation description.
        :rtype: str
        """
        if self.validation_status == CertificateInfo.CANNOT_UPLOAD:
            self.validation_description = 'Cannot Upload'
            return self.validation_description
        elif self.validation_status == CertificateInfo.CAN_UPLOAD:
            self.validation_description = 'Can Upload'
            return self.validation_description

    def upload_status_icon(self):
        """
        Returns validation status icon of the certificate corresponding
        to the validation status value.
        :return: Returns the upload status icon.
        :rtype: object
        """
        if self.upload_status == CertificateInfo.ERROR:
            return self.icons.get('error')
        elif self.upload_status == CertificateInfo.NOT_UPLOADED:
            return self.icons.get('warning')
        elif self.upload_status == CertificateInfo.SUCCESS:
            return self.icons.get('success')

    def validation_status_icon(self):
        """
        Returns validation status icon of the certificate corresponding
        to the validation status value.
        :return: Returns the validation status icon.
        :rtype: object
        """
        if self.validation_status == CertificateInfo.UNDEFINED:
            return self.icons.get('warning')
        elif self.validation_status == CertificateInfo.CANNOT_UPLOAD:
            return self.icons.get('error')
        elif self.validation_status == CertificateInfo.CAN_UPLOAD:
            return self.icons.get('success')
