# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_flts_certificate_upload.ui'
#
# Created: Sun Aug 30 18:05:11 2020
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
        FltsCertUploadWidget.resize(572, 565)
        FltsCertUploadWidget.setMinimumSize(QtCore.QSize(0, 400))
        self.gridLayout_2 = QtGui.QGridLayout(FltsCertUploadWidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.vlNotification = QtGui.QVBoxLayout()
        self.vlNotification.setSpacing(6)
        self.vlNotification.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.vlNotification.setContentsMargins(-1, -1, -1, 0)
        self.vlNotification.setObjectName(_fromUtf8("vlNotification"))
        self.gridLayout_2.addLayout(self.vlNotification, 0, 0, 1, 3)
        self.frame_2 = QtGui.QFrame(FltsCertUploadWidget)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.gridLayout = QtGui.QGridLayout(self.frame_2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.btn_select_folder = QtGui.QPushButton(self.frame_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_select_folder.sizePolicy().hasHeightForWidth())
        self.btn_select_folder.setSizePolicy(sizePolicy)
        self.btn_select_folder.setMinimumSize(QtCore.QSize(110, 0))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/stdm/images/icons/flts_open_file.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_select_folder.setIcon(icon)
        self.btn_select_folder.setObjectName(_fromUtf8("btn_select_folder"))
        self.gridLayout.addWidget(self.btn_select_folder, 0, 2, 1, 1)
        self.label = QtGui.QLabel(self.frame_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(80, 0))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.btn_upload_certificate = QtGui.QPushButton(self.frame_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_upload_certificate.sizePolicy().hasHeightForWidth())
        self.btn_upload_certificate.setSizePolicy(sizePolicy)
        self.btn_upload_certificate.setMinimumSize(QtCore.QSize(110, 0))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/stdm/images/icons/flts_export_file.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_upload_certificate.setIcon(icon1)
        self.btn_upload_certificate.setObjectName(_fromUtf8("btn_upload_certificate"))
        self.gridLayout.addWidget(self.btn_upload_certificate, 0, 3, 1, 1)
        spacerItem = QtGui.QSpacerItem(97, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 4, 1, 1)
        self.cbo_scheme_number = QtGui.QComboBox(self.frame_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbo_scheme_number.sizePolicy().hasHeightForWidth())
        self.cbo_scheme_number.setSizePolicy(sizePolicy)
        self.cbo_scheme_number.setMinimumSize(QtCore.QSize(127, 0))
        self.cbo_scheme_number.setObjectName(_fromUtf8("cbo_scheme_number"))
        self.cbo_scheme_number.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cbo_scheme_number, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(self.frame_2, 1, 0, 1, 3)
        self.tbvw_certificate = QtGui.QTableView(FltsCertUploadWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tbvw_certificate.sizePolicy().hasHeightForWidth())
        self.tbvw_certificate.setSizePolicy(sizePolicy)
        self.tbvw_certificate.setMinimumSize(QtCore.QSize(0, 300))
        self.tbvw_certificate.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tbvw_certificate.setObjectName(_fromUtf8("tbvw_certificate"))
        self.gridLayout_2.addWidget(self.tbvw_certificate, 2, 0, 1, 3)
        self.lbl_status = QtGui.QLabel(FltsCertUploadWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_status.sizePolicy().hasHeightForWidth())
        self.lbl_status.setSizePolicy(sizePolicy)
        self.lbl_status.setMaximumSize(QtCore.QSize(160, 16777215))
        self.lbl_status.setObjectName(_fromUtf8("lbl_status"))
        self.gridLayout_2.addWidget(self.lbl_status, 3, 0, 1, 1)
        self.line = QtGui.QFrame(FltsCertUploadWidget)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout_2.addWidget(self.line, 3, 1, 1, 1)
        self.lbl_records_count = QtGui.QLabel(FltsCertUploadWidget)
        self.lbl_records_count.setObjectName(_fromUtf8("lbl_records_count"))
        self.gridLayout_2.addWidget(self.lbl_records_count, 3, 2, 1, 1)
        self.frame = QtGui.QFrame(FltsCertUploadWidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.btn_close = QtGui.QPushButton(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_close.sizePolicy().hasHeightForWidth())
        self.btn_close.setSizePolicy(sizePolicy)
        self.btn_close.setMinimumSize(QtCore.QSize(110, 0))
        self.btn_close.setObjectName(_fromUtf8("btn_close"))
        self.horizontalLayout.addWidget(self.btn_close)
        self.gridLayout_2.addWidget(self.frame, 4, 0, 1, 3)

        self.retranslateUi(FltsCertUploadWidget)
        QtCore.QMetaObject.connectSlotsByName(FltsCertUploadWidget)

    def retranslateUi(self, FltsCertUploadWidget):
        FltsCertUploadWidget.setWindowTitle(_translate("FltsCertUploadWidget", "Upload Scanned Certificate", None))
        self.btn_select_folder.setText(_translate("FltsCertUploadWidget", "Select Folder...", None))
        self.label.setText(_translate("FltsCertUploadWidget", "Select scheme", None))
        self.btn_upload_certificate.setText(_translate("FltsCertUploadWidget", "Upload", None))
        self.cbo_scheme_number.setToolTip(_translate("FltsCertUploadWidget", "<html><head/><body><p>Select Scheme</p></body></html>", None))
        self.cbo_scheme_number.setItemText(0, _translate("FltsCertUploadWidget", "OSHKTI. 0001 / 2020", None))
        self.lbl_status.setText(_translate("FltsCertUploadWidget", "Status:  ", None))
        self.lbl_records_count.setText(_translate("FltsCertUploadWidget", "  files", None))
        self.btn_close.setText(_translate("FltsCertUploadWidget", "Close", None))

from stdm import resources_rc
