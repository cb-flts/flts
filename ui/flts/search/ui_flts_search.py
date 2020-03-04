# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_flts_search.ui'
#
# Created: Wed Mar  4 11:08:16 2020
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_flts_search(object):
    def setupUi(self, flts_search):
        flts_search.setObjectName(_fromUtf8("flts_search"))
        flts_search.resize(400, 368)
        self.gridLayout = QtGui.QGridLayout(flts_search)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 2)
        self.lineEdit_search = QtGui.QLineEdit(flts_search)
        self.lineEdit_search.setObjectName(_fromUtf8("lineEdit_search"))
        self.gridLayout.addWidget(self.lineEdit_search, 1, 0, 1, 2)
        self.label_filter = QtGui.QLabel(flts_search)
        self.label_filter.setObjectName(_fromUtf8("label_filter"))
        self.gridLayout.addWidget(self.label_filter, 2, 0, 1, 1)
        self.filter_cbx = QtGui.QComboBox(flts_search)
        self.filter_cbx.setObjectName(_fromUtf8("filter_cbx"))
        self.gridLayout.addWidget(self.filter_cbx, 2, 1, 1, 1)
        self.lst_search_results = QtGui.QListView(flts_search)
        self.lst_search_results.setObjectName(_fromUtf8("lst_search_results"))
        self.gridLayout.addWidget(self.lst_search_results, 3, 0, 1, 2)
        self.buttonBox_search = QtGui.QDialogButtonBox(flts_search)
        self.buttonBox_search.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox_search.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox_search.setCenterButtons(True)
        self.buttonBox_search.setObjectName(_fromUtf8("buttonBox_search"))
        self.gridLayout.addWidget(self.buttonBox_search, 4, 0, 1, 2)

        self.retranslateUi(flts_search)
        QtCore.QMetaObject.connectSlotsByName(flts_search)

    def retranslateUi(self, flts_search):
        flts_search.setWindowTitle(_translate("flts_search", "Form", None))
        self.label_filter.setText(_translate("flts_search", "Search Filter", None))

from stdm import resources_rc
