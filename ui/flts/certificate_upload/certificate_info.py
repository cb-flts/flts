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
        self.upload_status = CertificateInfo.NOT_UPLOADED
        self.validation_status = CertificateInfo.UNDEFINED
        self.certificate_number = kwargs.pop('certificate_number', '')
        self.validation_description = ''
        self.upload_description = ''
        self.filename = kwargs.pop('filename', '')
        # Icons representing state of the certificate
        self.icons = {
            'cannot_upload': QIcon(":/plugins/stdm/images/icons/flts_cert_cannot_upload.png"),
            'undefined': QIcon(":/plugins/stdm/images/icons/flts_cert_undefined.png"),
            'can_upload': QIcon(":/plugins/stdm/images/icons/flts_cert_can_upload.png"),
            'error': QIcon(":/plugins/stdm/images/icons/flts_cert_upload_error.png"),
            'not_uploaded': QIcon(":/plugins/stdm/images/icons/flts_success.png"),
            'success': QIcon(":/plugins/stdm/images/icons/flts_cert_success.png")
        }

    def upload_status_text(self):
        """
        Returns upload status description of the certificate corresponding to
        the upload status value.
        :return: Returns the certificate upload description.
        :rtype: str
        """
        status = self.upload_status
        upload_desc = self.upload_description
        if status == CertificateInfo.NOT_UPLOADED:
            upload_desc = 'Certificate not uploaded'
        elif status == CertificateInfo.SUCCESS:
            upload_desc = 'Certificate successfully uploaded'

        return upload_desc

    def validation_status_text(self):
        """
        Returns validation status description of the certificate corresponding
        to the validation status value.
        :return: Returns the certificate validation description.
        :rtype: str
        """
        status = self.validation_status
        valid_desc = self.validation_description
        if status == CertificateInfo.UNDEFINED:
            valid_desc = 'Certificate is not validated'
        elif status == CertificateInfo.CAN_UPLOAD:
            valid_desc = 'Certificate can be uploaded'

        return valid_desc

    def upload_status_icon(self):
        """
        Returns validation status icon of the certificate corresponding
        to the validation status value.
        :return: Returns the upload status icon.
        :rtype: QIcon
        """
        upload_icon = None
        upload_status = self.upload_status
        if upload_status == CertificateInfo.ERROR:
            upload_icon = self.icons.get('error')
        elif upload_status == CertificateInfo.NOT_UPLOADED:
            upload_icon = self.icons.get('not_uploaded')
        elif upload_status == CertificateInfo.SUCCESS:
            upload_icon = self.icons.get('success')

        return upload_icon

    def validation_status_icon(self):
        """
        Returns validation status icon of the certificate corresponding
        to the validation status value.
        :return: Returns the validation status icon.
        :rtype: QIcon
        """
        validation_icon = None
        validation_status = self.validation_status
        if validation_status == CertificateInfo.CANNOT_UPLOAD:
            validation_icon = self.icons.get('cannot_upload')
        elif validation_status == CertificateInfo.UNDEFINED:
            validation_icon = self.icons.get('undefined')
        elif validation_status == CertificateInfo.CAN_UPLOAD:
            validation_icon = self.icons.get('can_upload')

        return validation_icon
