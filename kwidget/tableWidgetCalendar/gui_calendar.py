# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_calendar.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CalendarTableWid(object):
    def setupUi(self, CalendarTableWid):
        CalendarTableWid.setObjectName("CalendarTableWid")
        CalendarTableWid.resize(624, 526)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CalendarTableWid.sizePolicy().hasHeightForWidth())
        CalendarTableWid.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(CalendarTableWid)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.bot_prev = QtWidgets.QPushButton(CalendarTableWid)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bot_prev.sizePolicy().hasHeightForWidth())
        self.bot_prev.setSizePolicy(sizePolicy)
        self.bot_prev.setMinimumSize(QtCore.QSize(40, 40))
        self.bot_prev.setMaximumSize(QtCore.QSize(40, 40))
        self.bot_prev.setObjectName("bot_prev")
        self.horizontalLayout.addWidget(self.bot_prev)
        self.combo_mesi = ComboSenzaFreccia(CalendarTableWid)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo_mesi.sizePolicy().hasHeightForWidth())
        self.combo_mesi.setSizePolicy(sizePolicy)
        self.combo_mesi.setMinimumSize(QtCore.QSize(0, 40))
        self.combo_mesi.setMaximumSize(QtCore.QSize(16777215, 40))
        self.combo_mesi.setObjectName("combo_mesi")
        self.combo_mesi.addItem("")
        self.combo_mesi.addItem("")
        self.combo_mesi.addItem("")
        self.combo_mesi.addItem("")
        self.combo_mesi.addItem("")
        self.combo_mesi.addItem("")
        self.combo_mesi.addItem("")
        self.combo_mesi.addItem("")
        self.combo_mesi.addItem("")
        self.combo_mesi.addItem("")
        self.combo_mesi.addItem("")
        self.combo_mesi.addItem("")
        self.horizontalLayout.addWidget(self.combo_mesi)
        self.bot_next = QtWidgets.QPushButton(CalendarTableWid)
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
        self.tableWidget_calendario = QtWidgets.QTableWidget(CalendarTableWid)
        self.tableWidget_calendario.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_calendario.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_calendario.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.tableWidget_calendario.setAutoScroll(False)
        self.tableWidget_calendario.setTabKeyNavigation(False)
        self.tableWidget_calendario.setProperty("showDropIndicator", False)
        self.tableWidget_calendario.setDragDropOverwriteMode(False)
        self.tableWidget_calendario.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget_calendario.setWordWrap(False)
        self.tableWidget_calendario.setCornerButtonEnabled(False)
        self.tableWidget_calendario.setRowCount(6)
        self.tableWidget_calendario.setColumnCount(7)
        self.tableWidget_calendario.setObjectName("tableWidget_calendario")
        self.tableWidget_calendario.verticalHeader().setVisible(False)
        self.tableWidget_calendario.verticalHeader().setMinimumSectionSize(44)
        self.verticalLayout.addWidget(self.tableWidget_calendario)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(CalendarTableWid)
        QtCore.QMetaObject.connectSlotsByName(CalendarTableWid)

    def retranslateUi(self, CalendarTableWid):
        _translate = QtCore.QCoreApplication.translate
        CalendarTableWid.setWindowTitle(_translate("CalendarTableWid", "Form"))
        self.bot_prev.setText(_translate("CalendarTableWid", "Prev"))
        self.combo_mesi.setItemText(0, _translate("CalendarTableWid", "Gennaio"))
        self.combo_mesi.setItemText(1, _translate("CalendarTableWid", "Febbraio"))
        self.combo_mesi.setItemText(2, _translate("CalendarTableWid", "Marzo"))
        self.combo_mesi.setItemText(3, _translate("CalendarTableWid", "Aprile"))
        self.combo_mesi.setItemText(4, _translate("CalendarTableWid", "Maggio"))
        self.combo_mesi.setItemText(5, _translate("CalendarTableWid", "Giugno"))
        self.combo_mesi.setItemText(6, _translate("CalendarTableWid", "Luglio"))
        self.combo_mesi.setItemText(7, _translate("CalendarTableWid", "Agosto"))
        self.combo_mesi.setItemText(8, _translate("CalendarTableWid", "Settembre"))
        self.combo_mesi.setItemText(9, _translate("CalendarTableWid", "Ottobre"))
        self.combo_mesi.setItemText(10, _translate("CalendarTableWid", "Novembre"))
        self.combo_mesi.setItemText(11, _translate("CalendarTableWid", "Dicembre"))
        self.bot_next.setText(_translate("CalendarTableWid", "Next"))


from kwidget.combosenzafreccia.combosenzafreccia import ComboSenzaFreccia


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CalendarTableWid = QtWidgets.QWidget()
    ui = Ui_CalendarTableWid()
    ui.setupUi(CalendarTableWid)
    CalendarTableWid.show()
    sys.exit(app.exec_())
