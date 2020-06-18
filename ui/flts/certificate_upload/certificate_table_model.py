"""
/***************************************************************************
Name                 : Certificate table model
Description          : Container for the certificate table model objects.
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
    QAbstractItemModel
)
from stdm.ui.flts.certificate_upload.certificate_info import CertificateInfo


class CertificateTableModel(QAbstractItemModel):
    """
    Container for the certificate table model objects.
    """
    def __init__(self, cert_info=None, parent=None):
        super(CertificateTableModel, self).__init__(parent)
        self._cert_info = cert_info
        if not self._cert_info:
            self._cert_info = []
        # Headers for the model columns
        self._headers = ["Certificate Number", "Upload Status", "Size"]

    def cert_info_from_filename(self, filename):
        """
        Get the certificate filename from the certificate information object.
        :param filename: Filename of the certificate
        :type filename: str
        """
        if not filename:
            CertificateInfo().filename = filename

        return filename

    def set_certificate_info(self, cert_info):
        """
        :param cert_info:
        :return:
        """

    def data(self, index, role):
        """
        Returns the data to be displayed for the given index and the given
        role.This method will be called implicitly by QTableView.
        :param index:
        :param role:
        :return:
        """

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """
        Implementation of the QAbstractItemModel header method.
        """
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return int(Qt.AlignLeft | Qt.AlignVCenter)
            return int(Qt.AlignRight | Qt.AlignVCenter)
        elif role != Qt.DisplayRole:
            return
        if orientation == Qt.Horizontal:
            if self._headers:
                return self._headers[section]
        if self._vertical_header:
            return section + 1

    def rowCount(self):
        """
        Implementation of the QAbstractItemModel rowCount method.
        """

    def columnCount(self):
        """
        Implementation of the QAbstractItemModel columnCount method.
        """

    def reset(self):
        """
        Reset the certificate table model.
        """

