# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(200)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.finalLay = QtWidgets.QHBoxLayout()
        self.finalLay.setObjectName("finalLay")
        self.prevLay = QtWidgets.QVBoxLayout()
        self.prevLay.setObjectName("prevLay")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.bot_prev = QtWidgets.QPushButton(Dialog)
        self.bot_prev.setObjectName("bot_prev")
        self.horizontalLayout_3.addWidget(self.bot_prev)
        self.prevLay.addLayout(self.horizontalLayout_3)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.prevLay.addItem(spacerItem1)
        self.finalLay.addLayout(self.prevLay)
        self.centLay = QtWidgets.QVBoxLayout()
        self.centLay.setObjectName("centLay")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.combo = ComboSenzaFreccia(Dialog)
        self.combo.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0.5, y1:0, x2:1, y2:0, stop:0.511364 rgba(102, 191, 255, 214), stop:1 rgba(0, 0, 0, 0));")
        self.combo.setMaxVisibleItems(12)
        self.combo.setMaxCount(12)
        self.combo.setModelColumn(0)
        self.combo.setObjectName("combo")
        self.verticalLayout_2.addWidget(self.combo)
        self.table = MyCalendarCore(Dialog)
        self.table.setMinimumSize(QtCore.QSize(500, 500))
        self.table.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.table.setFrameShadow(QtWidgets.QFrame.Plain)
        self.table.setLineWidth(0)
        self.table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.setObjectName("table")
        self.table.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_2.addWidget(self.table)
        self.centLay.addLayout(self.verticalLayout_2)
        self.finalLay.addLayout(self.centLay)
        self.nextLay = QtWidgets.QVBoxLayout()
        self.nextLay.setObjectName("nextLay")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.bot_next = QtWidgets.QPushButton(Dialog)
        self.bot_next.setObjectName("bot_next")
        self.horizontalLayout_4.addWidget(self.bot_next)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.nextLay.addLayout(self.horizontalLayout_4)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.nextLay.addItem(spacerItem3)
        self.finalLay.addLayout(self.nextLay)
        self.horizontalLayout.addLayout(self.finalLay)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.bot_prev.setText(_translate("Dialog", "PushButton"))
        self.bot_next.setText(_translate("Dialog", "PushButton"))
from combosenzafreccia import ComboSenzaFreccia
from mycalendarcore import MyCalendarCore


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
