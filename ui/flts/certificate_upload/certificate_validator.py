"""
/***************************************************************************
Name                 : CertificateValidator
Description          : Class validating certificate name and upload
                       status.
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
from PyQt4.QtCore import (
    pyqtSignal,
    QThread
)

from stdm.ui.flts.certificate_upload import certificate_model_factory
from stdm.ui.flts.certificate_upload.certificate_info import (
    CertificateInfo
)


class CertificateValidator(QThread):
    """
    Validates if certificates can be uploaded to the document repository.
    """

    # Signals
    validated = pyqtSignal(CertificateInfo)
    validation_completed = pyqtSignal()

    def __init__(self, cert_info=None, parent=None):
        super(CertificateValidator, self).__init__(parent)
        self._cert_info = cert_info
        if not self._cert_info:
            self._cert_info = []

    @property
    def cert_info_items(self):
        """
        :return: Returns a list of certificate items.
        :rtype: list
        """
        return self._cert_info

    @cert_info_items.setter
    def cert_info_items(self, cert_info):
        """
        Sets the collection of the CertificateInfo objects to be validated.
        :param cert_info: List of certificate items.
        :type cert_info: list
        """
        if not cert_info:
            self._cert_info = cert_info

    def run(self):
        """
        Initiates a QThread for validation.
        """
        self.validate()

    def validate(self):
        """
        Performs validation process of the certificate information for each
         individual certificate in the list of certificates.
        """
        for cert_info in self._cert_info:
            self._validate_cert_info(cert_info)

        self.validation_completed.emit()

    def clear(self):
        """
        Resets the list of certificate info objects from previous
        validation session.
        """
        self._cert_info = []

    def _query_by_cert_number(self, cert_number):
        """
        Checks whether the certificate number exists in the certificate
        table and returns the SQLAlchemy object corresponding to the
        certificate number, otherwise returns None.
        :param cert_number: Certificate number.
        :type cert_number: str
        :return: Returns the SQLAlchemy object corresponding to the
        certificate number, if not found returns None.
        :rtype: object
        """
        crt_model = certificate_model_factory()
        if not crt_model:
            return None
        else:
            # Unpack certificate model from tuple
            crt_model = crt_model[0]

        # Certificate object
        cert_obj = crt_model()

        # Query certificate number
        result = cert_obj.queryObject().filter(
            crt_model.certificate_number == cert_number
        ).first()
        if not result:
            return None
        else:
            return result

    def _validate_cert_info(self, cert_info):
        """
        Checks if certificate can be uploaded by checking if the certificate
        :param cert_info: Certificate information items.
        :type cert_info: tuple
        """
        cert_obj = self._query_by_cert_number(
            cert_info.certificate_number
        )

        if not cert_obj:
            cert_info.validation_status = CertificateInfo.CANNOT_UPLOAD
            cert_info.validation_description = 'Certificate number does not exist in the' \
                                               ' database.'
        else:
            upload_status = cert_obj.is_uploaded
            if not upload_status:
                cert_info.validation_status = CertificateInfo.CAN_UPLOAD
            else:
                cert_info.validation_status = CertificateInfo.CANNOT_UPLOAD
                cert_info.validation_description = 'Certificate has already been uploaded.'

        self.validated.emit(cert_info)
