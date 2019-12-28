"""
/***************************************************************************
Name                 : Workflow Manager Delegate
Description          : A generic delegate for handling presentation
                       and editing of table view data.
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
from PyQt4.QtGui import *


class GenericDelegate(QItemDelegate):
    """
    Generic delegate for table view presentation and editing
    """

    def __init__(self, parent=None):
        super(GenericDelegate, self).__init__(parent)
        self.delegates = {}

    def insert_column_delegate(self, column, delegate):
        """
        Inserts a delegate based on a column type
        :param column: Column ID
        :type column: Integer
        :param delegate: Generic delegate
        :type delegate: QItemDelegate
        """
        delegate.setParent(self)
        self.delegates[column] = delegate

    def remove_column_delegate(self, column):
        """
        Removes a delegate based on a column type
        :param column: Column ID
        :type column: Integer
        """
        if column in self.delegates:
            del self.delegates[column]

    def createEditor(self, parent, option, index):
        """
        Implementation of generic QItemDelegate createEditor method
        """
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            return delegate.createEditor(parent, option, index)
        else:
            return QItemDelegate.createEditor(self, parent, option, index)

    def setEditorData(self, editor, index):
        """
        Implementation of generic QItemDelegate setEditorData method
        """
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            delegate.setEditorData(editor, index)
        else:
            QItemDelegate.setEditorData(self, editor, index)

    def setModelData(self, editor, model, index):
        """
        Implementation of generic QItemDelegate setModelData method
        """
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            delegate.setModelData(editor, model, index)
        else:
            QItemDelegate.setModelData(self, editor, model, index)


class IntegerColumnDelegate(QItemDelegate):
    """
    Generic integer column delegate
    """
    def __init__(self, minimum=0, maximum=100, parent=None):
        super(IntegerColumnDelegate, self).__init__(parent)
        self.minimum = minimum
        self.maximum = maximum

    def createEditor(self, parent, option, index):
        """
        Implementation of generic integer column
        QItemDelegate createEditor method
        """
        spinbox = QSpinBox(parent)
        spinbox.setRange(self.minimum, self.maximum)
        spinbox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        return spinbox

    def setEditorData(self, editor, index):
        """
        Implementation of generic integer column
        QItemDelegate setEditorData method
        """
        value = index.model().data(index, Qt.DisplayRole).toInt()[0]
        editor.setValue(value)

    def setModelData(self, editor, model, index):
        """
        Implementation of generic integer column
        QItemDelegate setModelData method
        """
        editor.interpretText()
        model.setData(index, QVariant(editor.value()))


class DateColumnDelegate(QItemDelegate):
    """
    Generic date column delegate
    """
    def __init__(self, minimum=QDate(), maximum=QDate.currentDate(),
                 format="yyyy-MM-dd", parent=None):
        super(DateColumnDelegate, self).__init__(parent)
        self.minimum = minimum
        self.maximum = maximum
        self.format = QString(format)

    def createEditor(self, parent, option, index):
        """
        Implementation of generic date column
        QItemDelegate createEditor method
        """
        date_edit = QDateEdit(parent)
        date_edit.setDateRange(self.minimum, self.maximum)
        date_edit.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        date_edit.setDisplayFormat(self.format)
        date_edit.setCalendarPopup(True)
        return date_edit

    def setEditorData(self, editor, index):
        """
        Implementation of generic date column
        QItemDelegate setEditorData method
        """
        value = index.model().data(index, Qt.DisplayRole).toDate()
        editor.setDate(value)

    def setModelData(self, editor, model, index):
        """
        Implementation of generic date column
        QItemDelegate setModelData method
        """
        model.setData(index, QVariant(editor.date()))


class ListTextColumnDelegate(QItemDelegate):
    """
    Generic list text column delegate
    """
    def __init__(self, items, parent=None):
        super(ListTextColumnDelegate, self).__init__(parent)
        self.items = items

    def createEditor(self, parent, option, index):
        """
        Implementation of generic list column
        QItemDelegate createEditor method
        """
        combobox = QComboBox(parent)
        combobox.addItems(sorted(self.items))
        combobox.setEditable(True)
        return combobox

    def setEditorData(self, editor, index):
        """
        Implementation of generic list column
        QItemDelegate setEditorData method
        """
        value = index.model().data(index, Qt.DisplayRole).toInt()[0]
        editor.setValue(value)

    def setModelData(self, editor, model, index):
        """
        Implementation of generic list column
        QItemDelegate setModelData method
        """
        editor.interpretText()
        model.setData(index, QVariant(editor.value()))


class PlainTextColumnDelegate(QItemDelegate):
    """
    Generic plain text column delegate
    """
    def __init__(self, parent=None):
        super(PlainTextColumnDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        """
        Implementation of generic plain text column
        QItemDelegate createEditor method
        """
        line_edit = QLineEdit(parent)
        return line_edit

    def setEditorData(self, editor, index):
        """
        Implementation of generic plain text column
        QItemDelegate setEditorData method
        """
        value = index.model().data(index, Qt.DisplayRole).toString()
        editor.setText(value)

    def setModelData(self, editor, model, index):
        """
        Implementation of generic plain text column
        QItemDelegate setModelData method
        """
        model.setData(index, QVariant(editor.text()))
