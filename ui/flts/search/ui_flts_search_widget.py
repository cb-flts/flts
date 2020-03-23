# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_flts_search_widget.ui'
#
# Created: Thu Mar 12 12:59:30 2020
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_FltsSearchWidget(object):
    def setupUi(self, FltsSearchWidget):
        FltsSearchWidget.setObjectName(_fromUtf8("FltsSearchWidget"))
        FltsSearchWidget.resize(819, 403)
        FltsSearchWidget.setWindowTitle(_fromUtf8(""))
        self.gridLayout = QtGui.QGridLayout(FltsSearchWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.vlNotification = QtGui.QVBoxLayout()
        self.vlNotification.setObjectName(_fromUtf8("vlNotification"))
        self.gridLayout.addLayout(self.vlNotification, 0, 0, 1, 8)
        self.label = QtGui.QLabel(FltsSearchWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 2)
        self.label_2 = QtGui.QLabel(FltsSearchWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.cbo_column = QtGui.QComboBox(FltsSearchWidget)
        self.cbo_column.setMinimumSize(QtCore.QSize(120, 0))
        self.cbo_column.setObjectName(_fromUtf8("cbo_column"))
        self.gridLayout.addWidget(self.cbo_column, 2, 1, 1, 1)
        self.label_3 = QtGui.QLabel(FltsSearchWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 2, 1, 1)
        self.cbo_expression = QtGui.QComboBox(FltsSearchWidget)
        self.cbo_expression.setMinimumSize(QtCore.QSize(120, 0))
        self.cbo_expression.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.cbo_expression.setObjectName(_fromUtf8("cbo_expression"))
        self.gridLayout.addWidget(self.cbo_expression, 2, 3, 1, 1)
        self.txt_keyword = QgsFilterLineEdit(FltsSearchWidget)
        self.txt_keyword.setMinimumSize(QtCore.QSize(0, 0))
        self.txt_keyword.setMaxLength(50)
        self.txt_keyword.setObjectName(_fromUtf8("txt_keyword"))
        self.gridLayout.addWidget(self.txt_keyword, 2, 4, 1, 1)
        self.btn_search = QtGui.QPushButton(FltsSearchWidget)
        self.btn_search.setMaximumSize(QtCore.QSize(16777215, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/stdm/images/icons/flts_search.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_search.setIcon(icon)
        self.btn_search.setIconSize(QtCore.QSize(16, 16))
        self.btn_search.setObjectName(_fromUtf8("btn_search"))
        self.gridLayout.addWidget(self.btn_search, 2, 5, 1, 1)
        self.btn_clear = QtGui.QPushButton(FltsSearchWidget)
        self.btn_clear.setMinimumSize(QtCore.QSize(0, 0))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/stdm/images/icons/reset.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_clear.setIcon(icon1)
        self.btn_clear.setObjectName(_fromUtf8("btn_clear"))
        self.gridLayout.addWidget(self.btn_clear, 2, 6, 1, 1)
        spacerItem = QtGui.QSpacerItem(177, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 7, 1, 1)
        self.btn_advanced_search = QtGui.QPushButton(FltsSearchWidget)
        self.btn_advanced_search.setMinimumSize(QtCore.QSize(150, 0))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/stdm/images/icons/expression.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_advanced_search.setIcon(icon2)
        self.btn_advanced_search.setObjectName(_fromUtf8("btn_advanced_search"))
        self.gridLayout.addWidget(self.btn_advanced_search, 3, 0, 1, 2)
        spacerItem1 = QtGui.QSpacerItem(622, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 2, 1, 6)
        self.tb_results = QtGui.QTableWidget(FltsSearchWidget)
        self.tb_results.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tb_results.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tb_results.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tb_results.setObjectName(_fromUtf8("tb_results"))
        self.tb_results.setColumnCount(0)
        self.tb_results.setRowCount(0)
        self.gridLayout.addWidget(self.tb_results, 4, 0, 1, 8)
        self.lbl_results_count = QtGui.QLabel(FltsSearchWidget)
        self.lbl_results_count.setObjectName(_fromUtf8("lbl_results_count"))
        self.gridLayout.addWidget(self.lbl_results_count, 5, 0, 1, 2)

        self.retranslateUi(FltsSearchWidget)
        QtCore.QMetaObject.connectSlotsByName(FltsSearchWidget)

    def retranslateUi(self, FltsSearchWidget):
        self.label.setText(QtGui.QApplication.translate("FltsSearchWidget", "<html><head/><body><p><span style=\" font-weight:600;\">Define Filter:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("FltsSearchWidget", "Search in", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("FltsSearchWidget", "Expression", None, QtGui.QApplication.UnicodeUTF8))
        self.txt_keyword.setPlaceholderText(QtGui.QApplication.translate("FltsSearchWidget", "Search keyword", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_search.setText(QtGui.QApplication.translate("FltsSearchWidget", "Search", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_clear.setText(QtGui.QApplication.translate("FltsSearchWidget", "Clear Results", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_advanced_search.setText(QtGui.QApplication.translate("FltsSearchWidget", "Advanced Search...", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_results_count.setText(QtGui.QApplication.translate("FltsSearchWidget", "Search Results:", None, QtGui.QApplication.UnicodeUTF8))

from qgis.gui import QgsFilterLineEdit
from stdm import resources_rc
