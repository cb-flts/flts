# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_flts_sort_dialog.ui'
#
# Created: Thu Apr  9 14:33:17 2020
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SortColumnDialog(object):
    def setupUi(self, SortColumnDialog):
        SortColumnDialog.setObjectName(_fromUtf8("SortColumnDialog"))
        SortColumnDialog.resize(417, 364)
        self.gridLayout = QtGui.QGridLayout(SortColumnDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(SortColumnDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.tv_sort_config = QtGui.QTableView(SortColumnDialog)
        self.tv_sort_config.setEditTriggers(QtGui.QAbstractItemView.DoubleClicked|QtGui.QAbstractItemView.SelectedClicked)
        self.tv_sort_config.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tv_sort_config.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tv_sort_config.setObjectName(_fromUtf8("tv_sort_config"))
        self.tv_sort_config.horizontalHeader().setDefaultSectionSize(150)
        self.tv_sort_config.horizontalHeader().setStretchLastSection(True)
        self.gridLayout.addWidget(self.tv_sort_config, 1, 0, 3, 1)
        self.btn_up = QtGui.QPushButton(SortColumnDialog)
        self.btn_up.setMaximumSize(QtCore.QSize(32, 16777215))
        self.btn_up.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/stdm/images/icons/up.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_up.setIcon(icon)
        self.btn_up.setObjectName(_fromUtf8("btn_up"))
        self.gridLayout.addWidget(self.btn_up, 1, 1, 1, 1)
        self.btn_down = QtGui.QPushButton(SortColumnDialog)
        self.btn_down.setMaximumSize(QtCore.QSize(32, 16777215))
        self.btn_down.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/stdm/images/icons/down.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_down.setIcon(icon1)
        self.btn_down.setObjectName(_fromUtf8("btn_down"))
        self.gridLayout.addWidget(self.btn_down, 2, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 235, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(SortColumnDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 2)

        self.retranslateUi(SortColumnDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SortColumnDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SortColumnDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SortColumnDialog)

    def retranslateUi(self, SortColumnDialog):
        SortColumnDialog.setWindowTitle(QtGui.QApplication.translate("SortColumnDialog", "Sort Column Values", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("SortColumnDialog", "Select the column names and specify the sort order ", None, QtGui.QApplication.UnicodeUTF8))

from stdm import resources_rc
