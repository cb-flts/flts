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


class CertificateInfo(object):
    """
    Container with the details of the certificate validation process.
    """
    # Validation status
    CAN_UPLOAD, CANNOT_UPLOAD, UNDEFINED = range(0, 3)

    def __init__(self, **kwargs):
        self.certificate_number = kwargs.pop('certificate_number', '')
        self.description = kwargs.pop('description', '')
        self.filename = kwargs.pop('filename', '')
        self.status = kwargs.pop('status', CertificateInfo.UNDEFINED)
