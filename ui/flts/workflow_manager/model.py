"""
/***************************************************************************
Name                 : Workflow Manager Model
Description          : Model for handling scheme table data in
                       Scheme Establishment and First, Second and
                       Third Examination FLTS modules.
Date                 : 11/August/2019
copyright            : (C) 2019
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

from PyQt4.QtCore import *
from sqlalchemy import exc


class WorkflowManagerModel(QAbstractTableModel):
    """
    Handles data for Scheme Establishment and First, Second
    and Third Examination FLTS modules
    """
    def __init__(self, data_service=None):
        super(WorkflowManagerModel, self).__init__()
        self._data_source = None
        self._data_service = data_service
        self.results = []
        self._headers = []

    @property
    def _icons(self):
        """
        Returns QtableView icons
        :return: Icons
        :return: QIcon
        """
        if hasattr(self._data_service, "icons"):
            return self._data_service.icons

    @property
    def _vertical_header(self):
        """
        Returns True if vertical columns
        are allowed
        :return: True
        :return: Boolean
        """
        if self._data_service:
            return self._data_service.vertical_header

    def data(self, index, role=Qt.DisplayRole):
        """
        Implementation of QAbstractTableModel
        data method
        """
        if not index.isValid() or \
           not (0 <= index.row() < len(self.results)):
            return
        result = self.results[index.row()]
        column = index.column()
        value = result.get(column)
        flag = self._item_flag(index)
        if role == Qt.DisplayRole and Qt.DisplayRole in flag:
            return value
        elif role == Qt.DecorationRole and Qt.DecorationRole in flag:
            return self._item_icon(index)
        elif role == Qt.ToolTipRole and Qt.ToolTipRole in flag:
            return self._item_tooltip(index)
        elif role == Qt.CheckStateRole and Qt.ItemIsUserCheckable in flag:
            if isinstance(value, float):
                return Qt.Checked if int(value) == 1 else Qt.Unchecked
        elif role == Qt.TextAlignmentRole:
            if Qt.ItemIsUserCheckable in flag:
                return int(Qt.AlignCenter | Qt.AlignVCenter)
            return int(Qt.AlignLeft | Qt.AlignVCenter)
        return

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """
        Implementation of QAbstractTableModel
        headerData method
        """
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return int(Qt.AlignLeft | Qt.AlignVCenter)
            return int(Qt.AlignRight | Qt.AlignVCenter)
        elif role != Qt.DisplayRole:
            return
        if orientation == Qt.Horizontal:
            if self._headers:
                return self._headers[section].name
        if self._vertical_header:
            return section + 1

    def rowCount(self, index=QModelIndex()):
        """
        Implementation of QAbstractTableModel
        rowCount method
        """
        return len(self.results)

    def columnCount(self, index=QModelIndex()):
        """
        Implementation of QAbstractTableModel
        columnCount method
        """
        return len(self._headers)

    def flags(self, index):
        """
        Implementation of QAbstractTableModel
        flags method
        """
        column = index.column()
        flag = QAbstractTableModel.flags(self, index)
        if Qt.ItemIsUserCheckable in self._headers[column].flag:
            flag |= Qt.ItemIsUserCheckable
        elif Qt.ItemIsEditable in self._headers[column].flag:
            flag |= Qt.ItemIsEditable
        return flag

    def setData(self, index, value, role=Qt.EditRole):
        """
        Implementation of QAbstractTableModel
        setData method
        """
        if index.isValid() and (0 <= index.row() < len(self.results)):
            result = self.results[index.row()]
            column = index.column()
            if role == Qt.CheckStateRole:
                # self.itemAboutToChange.emit(index, value)
                result[column] = 1.0 if value == Qt.Checked else 0.0
            elif role == Qt.EditRole:
                # TODO: Convert back to the data type value
                result[column] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def insertRows(self, position, rows=1, index=QModelIndex()):
        """
        Implementation of QAbstractTableModel insertRows method
        """
        row_data = self._data_source.load()
        rows = len(row_data)
        self.beginInsertRows(
            QModelIndex(), position, position + rows - 1
        )
        for row, data in enumerate(row_data):
            self.results.insert(position + row, data)
        self.endInsertRows()
        return True

    def removeRows(self, position, rows=1, index=QModelIndex()):
        """
        Implementation of QAbstractTableModel removeRows method
        """
        self.beginRemoveRows(
            QModelIndex(), position, position + rows - 1
        )
        self.results = self.results[:position] + \
                       self.results[position + rows:]
        self.endRemoveRows()
        return True

    def _item_flag(self, index):
        """
        Returns item configuration flag
        :param index: Table view item identifier
        :type index: QModelIndex or Boolean
        :return flag: Item configuration flag
        :rtype flag: List
        """
        column = index.column()
        flag = self._headers[column].flag
        result = self.results[index.row()]
        item = result.get("items")
        if item:
            item = item.get(column)
            if item and item.flags:
                flag = [f for f in flag if f != Qt.DisplayRole]
                flag.extend(item.flags)
        return flag

    def _item_tooltip(self, index):
        """
        Returns item tooltip
        :param index: Table view item identifier
        :type index: QModelIndex or Boolean
        :return: Item tooltip
        :rtype: String
        """
        column = index.column()
        result = self.results[index.row()]
        item = result.get("items")
        if item:
            item = item.get(column)
            return item.tooltip if item else None

    def _item_icon(self, index):
        """
        Returns item icon on decoration role
        :param index: Table view item identifier
        :type index: QModelIndex or Boolean
        :return: Item icon
        :rtype: QIcon
        """
        result = self.results[index.row()]
        value = result.get(index.column())
        if self._icons:
            icon_id = self._item_icon_id(index)
            if icon_id:
                value = icon_id
            elif isinstance(value, float):
                value = int(value)
            return self._icons.get(value)

    def _item_icon_id(self, index):
        """
        Returns item icon identifier
        :param index: Table view item identifier
        :type index: QModelIndex or Boolean
        :return: Icon identifier
        :rtype: String
        """
        column = index.column()
        result = self.results[index.row()]
        item = result.get("items")
        if item:
            item = item.get(column)
            return item.icon_id if item else None

    def get_record_id(self, row=0):
        """
        Gets record/entity id (primary key)
        :param row: Row index/number
        :rtype row: Integer
        :return: Record id
        :rtype: integer
        """
        return self.results[row]["data"].id

    def model_item(self, row, column):
        """
        Return model item
        :param row: Row index
        :rtype row: Integer
        :param column: Column index
        :rtype column: Integer
        :return item: Table field value
        :rtype item: Multiple types
        """
        item = self.results[row].get(column)
        return item

    def create_index(self, row, column):
        """
        Safely creates and returns the index
        :param row: Table view row index
        :param column: Table view column
        :return index: Table view item identifier or False
        :rtype index: QModelIndex or Boolean
        """
        index = self.index(row, column)
        if not index.isValid() and \
                not (0 <= index.row() < len(self.results)) and \
                not (0 <= index.column() < len(self._headers)):
            return False
        return index

    def remove_tooltip(self, row, column):
        """
        Removes a tooltip from a column
        :param row: Table view row index
        :param row: Integer
        :param column: Table view column index
        :type column: Integer
        """
        result = self.results[row]
        tooltip = result.get("tooltip")
        if column in tooltip:
            del tooltip[column]

    @property
    def entity_name(self):
        """
        Entity name
        :return _name: Entity name
        :rtype _name: String
        """
        return self._data_service.entity_name

    def load(self, data_source):
        """
        Load results from data source to be used in the table view
        :param data_source: Data source object
        :rtype data_source: Object
        """
        try:
            self.results = data_source.load()
            self._headers = data_source.get_headers()
            self._data_source = data_source
            self.set_data_service(data_source)
        except (AttributeError, exc.SQLAlchemyError, IOError, OSError, Exception) as e:
            raise e

    def load_collection(self, data_source):
        """
        Load collection query results to be used in the table view
        :param data_source: Data source object
        :rtype data_source: Object
        """
        try:
            self.results = data_source.load_collection()
            self._headers = data_source.get_headers()
            self._data_source = data_source
            self.set_data_service(data_source)
        except (AttributeError, exc.SQLAlchemyError, IOError, OSError, Exception) as e:
            raise e

    def set_data_service(self, data_source):
        """
        Sets the data service
        :param data_source: Data source object
        :rtype data_source: Object
        """
        if self._data_service is None:
            self._data_service = data_source._data_service

    def data_source(self):
        """
        Returns data source
        :return _data_source: Data source
        :rtype _data_source: Object
        """
        return self._data_source

    def refresh(self, data_source=None):
        """
        Refreshes the model
        :return data_source: Data source
        :rtype data_source: Object
        """
        if data_source is None:
            data_source = self._data_service
        self.layoutAboutToBeChanged.emit()
        self.results = []
        self._headers = []
        self.load(data_source)
        self.layoutChanged.emit()

    def reset(self):
        """
        Resets model
        """
        self.beginResetModel()
        self.results = []
        self._headers = []
        self.endResetModel()
