# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_cal.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets


class Ui_MyCalendar(object):
    def setupUi(self, MyCalendar):
        MyCalendar.setObjectName("MyCalendar")
        MyCalendar.resize(520, 558)
        self.gridLayout = QtWidgets.QGridLayout(MyCalendar)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, 10, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.bot_prev = QtWidgets.QPushButton(MyCalendar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bot_prev.sizePolicy().hasHeightForWidth())
        self.bot_prev.setSizePolicy(sizePolicy)
        self.bot_prev.setMinimumSize(QtCore.QSize(40, 40))
        self.bot_prev.setMaximumSize(QtCore.QSize(40, 40))
        self.bot_prev.setObjectName("bot_prev")
        self.horizontalLayout.addWidget(self.bot_prev)
        self.combo = ComboSenzaFreccia(MyCalendar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo.sizePolicy().hasHeightForWidth())
        self.combo.setSizePolicy(sizePolicy)
        self.combo.setMinimumSize(QtCore.QSize(30, 40))
        self.combo.setStyleSheet("")
        self.combo.setMaxVisibleItems(12)
        self.combo.setMaxCount(12)
        self.combo.setModelColumn(0)
        self.combo.setObjectName("combo")
        self.horizontalLayout.addWidget(self.combo)
        self.bot_next = QtWidgets.QPushButton(MyCalendar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bot_next.sizePolicy().hasHeightForWidth())
        self.bot_next.setSizePolicy(sizePolicy)
        self.bot_next.setMinimumSize(QtCore.QSize(40, 40))
        self.bot_next.setMaximumSize(QtCore.QSize(40, 40))
        self.bot_next.setObjectName("bot_next")
        self.horizontalLayout.addWidget(self.bot_next)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.table = Mytable(MyCalendar)
        self.table.setMinimumSize(QtCore.QSize(0, 0))
        self.table.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.table.setFrameShadow(QtWidgets.QFrame.Plain)
        self.table.setLineWidth(0)
        self.table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.setObjectName("table")
        self.table.horizontalHeader().setStretchLastSection(False)
        self.verticalLayout.addWidget(self.table)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(MyCalendar)
        QtCore.QMetaObject.connectSlotsByName(MyCalendar)

    def retranslateUi(self, MyCalendar):
        _translate = QtCore.QCoreApplication.translate
        MyCalendar.setWindowTitle(_translate("MyCalendar", "Form"))
        self.bot_prev.setText(_translate("MyCalendar", "Prev"))
        self.bot_next.setText(_translate("MyCalendar", "Next"))
from combosenzafreccia import ComboSenzaFreccia
from saves.mytable import Mytable


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MyCalendar = QtWidgets.QWidget()
    ui = Ui_MyCalendar()
    ui.setupUi(MyCalendar)
    MyCalendar.show()
    sys.exit(app.exec_())
