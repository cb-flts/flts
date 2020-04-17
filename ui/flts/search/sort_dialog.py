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

# Action source enumeration
COLUMN_NAME, SORT_ORDER, NO_SOURCE = range(0, 3)

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
        self.action_source = NO_SOURCE

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
        sort_txt = SORT_ORDER_NAME.get(order, '')
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
        if self.action_source != COLUMN_NAME:
            return

        sort_item = self.item(row, 1)
        text = ''
        if enable_sort:
            text = SORT_ORDER_NAME.get(sort_order)
        else:
            sort_order = NOT_SET

        sort_item.setText(text)
        sort_item.setData(sort_order, DATA_ROLE)

    def enable_sort_state(self, row, sort_order, display_name='', column_name=''):
        """
        Enables or disables the sort state for the column name based on the
        value of the sort order.
        :param row: Row number.
        :type row: int
        :param sort_order: Sort order. NOT_SET disables sorting for the column
        in the given row.
        :type sort_order: int
        :param display_name: Display name of the column.
        :type display_name: str
        :param column_name: Column name.
        :type column_name: str
        """
        if self.action_source != SORT_ORDER:
            return

        col_item = self.item(row, 0)
        if sort_order != NOT_SET:
            col_item.setCheckState(Qt.Checked)
        else:
            col_item.setCheckState(Qt.Unchecked)

        if display_name:
            col_item.setText(display_name)
        if column_name:
            col_item.setData(column_name, DATA_ROLE)

        self.action_source = NO_SOURCE

    def reset_complementary_source(self):
        self.action_source = NO_SOURCE


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
            return QStyledItemDelegate.createEditor(
                self,
                parent,
                option,
                index
            )

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

        self.btn_up.clicked.connect(
            self.on_move_row_up
        )
        self.btn_down.clicked.connect(
            self.on_move_row_down
        )

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
            self._model.action_source = COLUMN_NAME
            check_state = True if item.checkState() == Qt.Checked else False
            self._model.set_sorting_order(row, check_state)
            self._model.action_source = NO_SOURCE
        else:
            # Sort order has changed
            self._model.action_source = SORT_ORDER
            sort_order = item.data(DATA_ROLE)
            self._model.enable_sort_state(row, sort_order)
            self._model.action_source = NO_SOURCE

    def move_item(self, current_row, move_up=True):
        """
        Moves the column name and sort order items up (smaller new_row
        number) or down (bigger new_row number).
        :param current_row: Row number of the item to be moved.
        :type current_row: int
        :param move_up: True to move up, False to move down.
        :type move_up: bool
        :return: Returns True if the item was successfully moved, else False
        if the current_row is the first item (for a move up operation) or
        last item (for a move down operation).
        :rtype: bool
        """
        # Cannot be moved any further up
        if current_row == 0 and move_up:
            return False

        # Cannot be moved any further down
        if current_row == self._model.rowCount() -1 and not move_up:
            return False

        if move_up:
            replace_row = current_row - 1
        else:
            replace_row = current_row + 1

        sel_col_item = self._model.item(current_row, 0)
        sel_order_item = self._model.item(current_row, 1)
        replace_col_item = self._model.item(replace_row, 0)
        replace_order_item = self._model.item(replace_row, 1)

        # Capture the data to be replaced in the new row
        rep_col_display, rep_col_checked, rep_col_data = \
            replace_col_item.text(), replace_col_item.checkState(), \
            replace_col_item.data(DATA_ROLE)
        rep_order_text, rep_order_data = \
            replace_order_item.text(), replace_order_item.data(DATA_ROLE)

        # We need to use the approach below to avoid infinite loop of signals
        # Update column item with selection data
        self._model.action_source = SORT_ORDER
        self._model.enable_sort_state(
            replace_row,
            sel_order_item.data(DATA_ROLE),
            sel_col_item.text(),
            sel_col_item.data(DATA_ROLE)
        )
        self._model.action_source = NO_SOURCE

        sort_order = sel_order_item.data(DATA_ROLE)
        enable_sort = True
        if sort_order == NOT_SET:
            enable_sort = False
        # Update sort item with selection data
        self._model.action_source = COLUMN_NAME
        self._model.set_sorting_order(
            replace_row,
            enable_sort,
            sort_order
        )
        self._model.action_source = NO_SOURCE

        # Now update the row that has been pushed
        self._model.action_source= SORT_ORDER
        self._model.enable_sort_state(
            current_row,
            rep_order_data,
            rep_col_display,
            rep_col_data
        )
        self._model.action_source = NO_SOURCE

        enable_sort = True
        if rep_order_data == NOT_SET:
            enable_sort = False
        self._model.action_source = COLUMN_NAME
        self._model.set_sorting_order(
            current_row,
            enable_sort,
            rep_order_data
        )
        self._model.action_source = NO_SOURCE

        # Select the new row
        self.tv_sort_config.selectRow(replace_row)

        return True

    def _selected_row(self):
        # Returns the number of the currently selected row or -1 if there
        # is no selection.
        sel_row = -1
        sel_idxs = self.tv_sort_config.selectedIndexes()
        if len(sel_idxs) > 0:
            sel_idx = sel_idxs[0]
            sel_row = sel_idx.row()

        return sel_row

    def on_move_row_up(self):
        """
        Slot raised to move the selected row up.
        """
        sel_row = self._selected_row()
        if sel_row == -1:
            return

        self.move_item(sel_row)

    def on_move_row_down(self):
        """
        Slot raised to move the selected row down.
        """
        sel_row = self._selected_row()
        if sel_row == -1:
            return

        self.move_item(sel_row, False)