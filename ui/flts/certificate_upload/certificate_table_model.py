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
        return self._cert_info_items

    @cert_info_items.setter
    def cert_info_items(self, cert_info):
        """
        Sets the collection of the CertificateInfo objects to be validated.
        :param cert_info: List of certificate items.
        :type cert_info: list
        """
        if not cert_info:
            self._cert_info_items = cert_info

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

    def data(self, index, role):
        """
        Returns the data stored in the given role for an item referred to by
        the index.
        """
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()
        result = self._cert_info_items[row]
        if row < 0 or row >= len(self._cert_info_items):
            return None

        if role == Qt.DisplayRole:
            if col == 0:
                return result

        if role == Qt.ToolTipRole:
            if col == 1:
                if result.validation_status:
                    return result.validation_status
                elif result.upload_status:
                    return result.upload_status

        if role == Qt.DecorationRole:
            if col == 1:
                if result.validation_status:
                    return result.validation_status
                elif result.upload_status:
                    return result.upload_status

        return None

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
        self.beginResetModel()
        self.removeRows(0, len(self._cert_info_items))
        self._cert_info_items = []
        self._headers = []
        self.endResetModel()

