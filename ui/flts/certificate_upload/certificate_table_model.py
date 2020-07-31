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
    QAbstractTableModel,
    QModelIndex
)
from stdm.ui.flts.certificate_upload.certificate_info import CertificateInfo


class CertificateTableModel(QAbstractTableModel):
    """
    Container for the certificate table model objects.
    """

    def __init__(self, cert_info=None, parent=None):
        super(CertificateTableModel, self).__init__(parent)
        self._cert_info_items = cert_info
        if not self._cert_info_items:
            self._cert_info_items = []

        self._headers = ['Certificate Number', 'Status', 'View']

    @property
    def cert_info_items(self):
        """
        :return: Returns a list of certificate info items.
        :rtype: list
        """
        return self._cert_info_items

    @cert_info_items.setter
    def cert_info_items(self, cert_info):
        """
        Sets the collection of the CertificateInfo objects to be validated.
        :param cert_info: List of certificate items.
        :type cert_info: list
        """
        num_certs = len(cert_info)
        if num_certs > 0:
            self.clear()
            self._cert_info_items = cert_info
            self.insertRows(0, num_certs)

    @property
    def headers(self):
        """
        :return: Returns horizontal headers.
        """
        return self._headers

    def columnCount(self, index=QModelIndex()):
        """
        Returns number of columns based on the valid mapped columns.
        """
        return len(self._headers)

    def rowCount(self, index=QModelIndex()):
        """
        Returns number of rows based on the valid mapped columns.
        """
        return len(self._cert_info_items)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """
        Set the horizontal and vertical header labels.
        """
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self._headers[section]
        else:
            return int(section) + 1

        return None

    def data(self, index, role=Qt.DisplayRole):
        """
        Returns the data stored in the given role for an item referred to by
        the index.
        """
        # Check if index of data is valid
        if not index.isValid():
            return None

        # Define the row and column
        row = index.row()
        col = index.column()

        # Check if row number exceeds number of cert info items or is less
        # than zero
        if row < 0 or row >= len(self._cert_info_items):
            return None

        cert_info = self._cert_info_items[row]

        # Model display role that handles certificate number
        if role == Qt.DisplayRole:
            if col == 0:
                return cert_info.certificate_number

        # Model tooltip role that handles tooltips for upload and validation
        # statuses.
        if role == Qt.ToolTipRole:
            if col == 1:
                if cert_info.upload_status == CertificateInfo.NOT_UPLOADED:
                    return cert_info.validation_status_text()
                else:
                    return cert_info.upload_status_text()

        # Model decoration role that handles rendering icons for upload and
        # validation statuses.
        if role == Qt.DecorationRole:
            if col == 1:
                if cert_info.upload_status == CertificateInfo.NOT_UPLOADED:
                    return cert_info.validation_status_icon()
                else:
                    return cert_info.upload_status_icon()

            if col == 2:
                return cert_info.view_document_icon()

        return None

    def _notify_cert_status_changed(self, cert_number):
        """
        Emit signal when certificate status changes for a certificate number.
        :param cert_number: Certificate number that status is to be changed.
        :type cert_number: str
        """
        # Get the list of cert info indexes
        cert_idx_items = self.match(
            self.index(0, 0),
            Qt.DisplayRole,
            cert_number,
            1,
            Qt.MatchFixedString
        )

        # Check if the list is empty
        if len(cert_idx_items) == 0:
            return

        cert_idx = cert_idx_items[0]
        cert_row = cert_idx.row()
        icon_idx = self.index(cert_row, 1)

        # Check if the icon index is valid
        if not icon_idx.isValid():
            return

        # Emit signal
        self.dataChanged.emit(icon_idx, icon_idx)

    def update_validation_status(self, cert_number):
        """
        Update the validation status of the certificate.
        :param cert_number: Certificate number that validation status to be
        changed.
        :type cert_number: str
        """
        self._notify_cert_status_changed(cert_number)

    def update_upload_status(self, cert_number):
        """
        Update the upload status of the certificate.
        :param cert_number: Certificate number that validation status to be
        changed.
        :type cert_number: str
        """
        self._notify_cert_status_changed(cert_number)

    def insertRows(self, position, count=1, index=QModelIndex()):
        """
        Insert rows to the table model.
        """
        self.beginInsertRows(QModelIndex(), position, position + count - 1)
        self.endInsertRows()

        return True

    def removeRows(self, position, count=1, index=QModelIndex()):
        """
        Remove rows from the table model.
        """
        self.beginRemoveRows(QModelIndex(), position, position + count - 1)
        del self._cert_info_items[position:position + count]
        self.endRemoveRows()

        return None

    def clear(self):
        """
        Removes any previous certificate information items in the model.
        """
        self.removeRows(0, len(self._cert_info_items))
        self._cert_info_items = []
