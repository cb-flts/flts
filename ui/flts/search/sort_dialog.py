"""
/***************************************************************************
Name                 : SortDialog
Description          : Dialog for specifying the sorting of column values.
Date                 : 06/April/2020
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
from collections import OrderedDict

from PyQt4.QtGui import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QStandardItem,
    QStandardItemModel,
    QStyledItemDelegate
)

from PyQt4.QtCore import (
    Qt
)

from ui_flts_sort_dialog import Ui_SortColumnDialog

# Enumeration for sort order
ASCENDING, DESCENDING, NOT_SET = range(0, 3)

# Display name based on sort enum
SORT_ORDER_NAME = {
    0: 'Ascending',
    1: 'Descending'
}

# Role for storing sort-related data
DATA_ROLE = Qt.UserRole + 1023


class SortItemModel(QStandardItemModel):
    """
    Provides a model for defining the sorting of column values.
    """
    def __init__(self, column_mapping, parent=None):
        super(SortItemModel, self).__init__(parent)
        self._column_mapping = column_mapping
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels([
            'Column',
            'Sort Order'
        ])

        # Add columns
        for col_name, disp_name in self._column_mapping.iteritems():
            self.add_column(col_name, disp_name)

        # Flag for preventing infinite loop of slots when a
        # complementary item is changed.
        self._complementary_source = 0

    def add_column(self, column_name, display_name, order=NOT_SET):
        """
        Adds a new column row to the model and sets the sort order.
        :param column_name: Column name in the data source.
        :type column_name: str
        :param display_name: Friendly column display name.
        :type display_name: str
        :param order: Sort order.
        :type order: int
        """
        col_item = QStandardItem(display_name)
        col_item.setCheckable(True)
        col_item.setData(column_name, DATA_ROLE)
        sort_item = QStandardItem()
        if order != NOT_SET:
            sort_txt = SORT_ORDER_NAME.get(order)
            sort_item.setText(sort_txt)
            sort_item.setData(order, DATA_ROLE)
        self.appendRow([col_item, sort_item])

    def sort_mapping(self):
        """
        :return: Returns a list of tuples with each tuple containing the
        name and the corresponding sort order enum e.g.
        [('name', 0), ('age', 1)].
        :rtype: list
        """
        sorted_cols = []
        rows = self.rowCount()
        for i in range(rows):
            col_item = self.item(i, 0)
            check_state = col_item.checkState()
            if check_state == Qt.Checked:
                col_name = col_item.data(DATA_ROLE)
                sort_item = self.item(i, 1)
                sort_order = sort_item.data(DATA_ROLE)
                sorted_cols.append((col_name, sort_order))

        return sorted_cols

    def flags(self, idx):
        """
        Enable editing of the sort order column.
        """
        if not idx.isValid():
            return Qt.ItemIsEnabled

        col = idx.column()
        if col == 0:
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled | \
                   Qt.ItemIsUserCheckable
        elif col == 1:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

        return Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def set_sorting_order(self, row, enable_sort=True, sort_order=ASCENDING):
        """
        Enable or disable the sort order of the column in the given row.
        :param row: Row number.
        :type row: int
        :param enable_sort: True to enable sort or False to set the order
        to None.
        :type enable_sort: bool
        :param sort_order: If enable_sort is True, then the sort order to use,
        otherwise it is not applied.
        :type sort_order: int
        """
        if self._complementary_source == 1:
            self._complementary_source = 0
            return

        sort_item = self.item(row, 1)
        text = ''
        if enable_sort:
            text = SORT_ORDER_NAME.get(sort_order)
        else:
            sort_order = None

        self._complementary_source = 1
        sort_item.setText(text)
        self._complementary_source = 1
        sort_item.setData(sort_order, DATA_ROLE)

    def enable_sort_state(self, row, sort_order):
        """
        Enables or disables the sort state for the column name based on the
        value of the sort order.
        :param row: Row number.
        :type row: int
        :param sort_order: Sort order. -1 disables sorting for the column
        in the given row.
        :type sort_order: int
        """
        if self._complementary_source == 1:
            self._complementary_source = 0
            return

        col_item = self.item(row, 0)
        self._complementary_source = 1
        if sort_order != -1:
            col_item.setCheckState(Qt.Checked)
        else:
            col_item.setCheckState(Qt.Unchecked)

    def reset_complementary_source(self):
        self._complementary_source = 0


class SortOrderItemDelegate(QStyledItemDelegate):
    """
    Delegate for specifying the sort order in a table view.
    """
    def __init__(self, parent=None):
        super(SortOrderItemDelegate, self).__init__(parent)
        self._sort_cold_idx = 1

    def createEditor(self, parent, option, index):
        # Create combobox editor for sort order column
        if index.column() == self._sort_cold_idx:
            combo = QComboBox(parent)
            for enum, txt in SORT_ORDER_NAME.iteritems():
                combo.addItem(txt, enum)

            return combo
        else:
            QStyledItemDelegate.createEditor(self, parent, option, index)

    def setEditorData(self, editor, index):
        # Set the combobox index
        if index.column() == self._sort_cold_idx:
            sort_enum = index.data(DATA_ROLE)
            idx = editor.findData(sort_enum)
            if idx != -1:
                editor.setCurrentIndex(idx)
        else:
            QStyledItemDelegate.setEditorData(self, editor, index)

    def setModelData(self, editor, model, index):
        # Store data from the editor to the model.
        if index.column() == self._sort_cold_idx:
            disp_text = editor.currentText()
            enum = editor.itemData(editor.currentIndex())
            model.setData(index, enum, DATA_ROLE)
            model.setData(index, disp_text)
            model.reset_complementary_source()
        else:
            QStyledItemDelegate.setModelData(self, editor, model, index)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class SortColumnDialog(QDialog, Ui_SortColumnDialog):
    """
    Dialog for specifying the sort order of column values.
    """
    def __init__(self, columns, parent=None):
        super(SortColumnDialog, self).__init__(parent)
        self.setupUi(self)
        self._columns = columns
        self._model = SortItemModel(self._columns)
        self.tv_sort_config.setModel(self._model)
        self._model.itemChanged.connect(
            self.on_item_changed
        )

        # Rename 'Save' button
        save_btn = self.buttonBox.button(QDialogButtonBox.Save)
        if save_btn:
            save_btn.setText('Save and Close')

        # Set delegate for editing the sort order
        sort_order_delegate = SortOrderItemDelegate(self)
        self.tv_sort_config.setItemDelegate(sort_order_delegate)

    @property
    def columns(self):
        """
        :return: Returns the mapping of column names to their corresponding
        display names.
        :rtype: OrderedDict
        """
        return self._columns

    def sort_mapping(self):
        """
        :return: Returns the mapping of column names and corresponding sort
        order.
        :rtype: list
        """
        return self._model.sort_mapping()

    def on_item_changed(self, item):
        """
        Slot raised when an item in the model changes.
        :param item: Item which has its data changed
        :type item: QStandardItem
        """
        row = item.row()
        col = item.column()

        # If check state has changed
        if col == 0:
            check_state = True if item.checkState() == Qt.Checked else False
            self._model.set_sorting_order(row, check_state)
        else:
            # Sort order has changed
            sort_order = item.data(DATA_ROLE)
            if sort_order is None:
                sort_order = -1
            self._model.enable_sort_state(row, sort_order)

    def _enable_ok_btn(self, enabled):
        # Enable/disable OK button.
        if self._ok_btn:
            self._ok_btn.setEnabled(enabled)