# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_dialog_info.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog=None):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_dialog_info = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_dialog_info.setFont(font)
        self.label_dialog_info.setAlignment(QtCore.Qt.AlignCenter)
        self.label_dialog_info.setObjectName("label_dialog_info")
        self.verticalLayout.addWidget(self.label_dialog_info)
        self.textBrowser_dialog_info = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser_dialog_info.setObjectName("textBrowser_dialog_info")
        self.verticalLayout.addWidget(self.textBrowser_dialog_info)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.buttonBox_dialog_info = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox_dialog_info.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox_dialog_info.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox_dialog_info.setCenterButtons(True)
        self.buttonBox_dialog_info.setObjectName("buttonBox_dialog_info")
        self.gridLayout.addWidget(self.buttonBox_dialog_info, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox_dialog_info.accepted.connect(Dialog.accept)
        self.buttonBox_dialog_info.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Informazioni"))
        self.label_dialog_info.setText(_translate("Dialog", "Statistiche"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
