# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_flts_certificate_upload.ui'
#
# Created: Mon Jun  8 04:46:48 2020
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

class Ui_FltsCertUploadWidget(object):
    def setupUi(self, FltsCertUploadWidget):
        FltsCertUploadWidget.setObjectName(_fromUtf8("FltsCertUploadWidget"))
        FltsCertUploadWidget.setWindowModality(QtCore.Qt.NonModal)
        FltsCertUploadWidget.resize(455, 601)
        FltsCertUploadWidget.setMinimumSize(QtCore.QSize(0, 400))
        self.gridLayout = QtGui.QGridLayout(FltsCertUploadWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tbvw_certificate = QtGui.QTableView(FltsCertUploadWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tbvw_certificate.sizePolicy().hasHeightForWidth())
        self.tbvw_certificate.setSizePolicy(sizePolicy)
        self.tbvw_certificate.setMinimumSize(QtCore.QSize(0, 300))
        self.tbvw_certificate.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tbvw_certificate.setObjectName(_fromUtf8("tbvw_certificate"))
        self.gridLayout.addWidget(self.tbvw_certificate, 2, 0, 1, 5)
        self.lbl_records_count = QtGui.QLabel(FltsCertUploadWidget)
        self.lbl_records_count.setText(_fromUtf8(""))
        self.lbl_records_count.setObjectName(_fromUtf8("lbl_records_count"))
        self.gridLayout.addWidget(self.lbl_records_count, 3, 0, 1, 1)
        self.btn_select_folder = QtGui.QPushButton(FltsCertUploadWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_select_folder.sizePolicy().hasHeightForWidth())
        self.btn_select_folder.setSizePolicy(sizePolicy)
        self.btn_select_folder.setMinimumSize(QtCore.QSize(100, 0))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/stdm/images/icons/flts_open_file.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_select_folder.setIcon(icon)
        self.btn_select_folder.setObjectName(_fromUtf8("btn_select_folder"))
        self.gridLayout.addWidget(self.btn_select_folder, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(10, 18, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 3, 1, 1)
        self.btn_close = QtGui.QPushButton(FltsCertUploadWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_close.sizePolicy().hasHeightForWidth())
        self.btn_close.setSizePolicy(sizePolicy)
        self.btn_close.setMinimumSize(QtCore.QSize(100, 0))
        self.btn_close.setObjectName(_fromUtf8("btn_close"))
        self.gridLayout.addWidget(self.btn_close, 3, 4, 1, 1)
        self.cbo_scheme_number = QtGui.QComboBox(FltsCertUploadWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbo_scheme_number.sizePolicy().hasHeightForWidth())
        self.cbo_scheme_number.setSizePolicy(sizePolicy)
        self.cbo_scheme_number.setMinimumSize(QtCore.QSize(100, 0))
        self.cbo_scheme_number.setObjectName(_fromUtf8("cbo_scheme_number"))
        self.gridLayout.addWidget(self.cbo_scheme_number, 1, 1, 1, 1)
        self.btn_upload_certificate = QtGui.QPushButton(FltsCertUploadWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_upload_certificate.sizePolicy().hasHeightForWidth())
        self.btn_upload_certificate.setSizePolicy(sizePolicy)
        self.btn_upload_certificate.setMinimumSize(QtCore.QSize(100, 0))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/stdm/images/icons/flts_export_file.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_upload_certificate.setIcon(icon1)
        self.btn_upload_certificate.setObjectName(_fromUtf8("btn_upload_certificate"))
        self.gridLayout.addWidget(self.btn_upload_certificate, 1, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(8, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 3, 1, 1)
        self.vlNotification = QtGui.QVBoxLayout()
        self.vlNotification.setSpacing(6)
        self.vlNotification.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.vlNotification.setContentsMargins(-1, -1, -1, 0)
        self.vlNotification.setObjectName(_fromUtf8("vlNotification"))
        self.gridLayout.addLayout(self.vlNotification, 0, 0, 1, 5)

        self.retranslateUi(FltsCertUploadWidget)
        QtCore.QMetaObject.connectSlotsByName(FltsCertUploadWidget)

    def retranslateUi(self, FltsCertUploadWidget):
        FltsCertUploadWidget.setWindowTitle(_translate("FltsCertUploadWidget", "Upload Scanned Certificate", None))
        self.btn_select_folder.setText(_translate("FltsCertUploadWidget", "Select Folder...", None))
        self.btn_close.setText(_translate("FltsCertUploadWidget", "Close", None))
        self.cbo_scheme_number.setToolTip(_translate("FltsCertUploadWidget", "<html><head/><body><p>Select Scheme</p></body></html>", None))
        self.btn_upload_certificate.setText(_translate("FltsCertUploadWidget", "Upload", None))

from stdm import resources_rc
