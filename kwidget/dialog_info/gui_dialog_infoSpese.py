# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_dialog_infoSpese.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogInfoSpese(object):
    def setupUi(self, DialogInfoSpese):
        DialogInfoSpese.setObjectName("DialogInfoSpese")
        # DialogInfoSpese.setWindowModality(QtCore.Qt.WindowModal)
        DialogInfoSpese.resize(400, 300)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DialogInfoSpese.sizePolicy().hasHeightForWidth())
        DialogInfoSpese.setSizePolicy(sizePolicy)
        DialogInfoSpese.setMinimumSize(QtCore.QSize(400, 300))
        DialogInfoSpese.setMaximumSize(QtCore.QSize(400, 300))
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(DialogInfoSpese)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableWidget = MyTableWidget(DialogInfoSpese)
        self.tableWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tableWidget.setFrameShadow(QtWidgets.QFrame.Plain)
        self.tableWidget.setLineWidth(0)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        self.tableWidget.setTabKeyNavigation(False)
        self.tableWidget.setProperty("showDropIndicator", False)
        self.tableWidget.setDragDropOverwriteMode(False)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget.setCornerButtonEnabled(False)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(170)
        self.tableWidget.horizontalHeader().setHighlightSections(False)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(160)
        self.tableWidget.horizontalHeader().setStretchLastSection(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.horizontalLayout.addWidget(self.tableWidget)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.bot_addLine = QtWidgets.QPushButton(DialogInfoSpese)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bot_addLine.sizePolicy().hasHeightForWidth())
        self.bot_addLine.setSizePolicy(sizePolicy)
        self.bot_addLine.setMinimumSize(QtCore.QSize(30, 23))
        self.bot_addLine.setMaximumSize(QtCore.QSize(30, 23))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.bot_addLine.setFont(font)
        self.bot_addLine.setFocusPolicy(QtCore.Qt.NoFocus)
        self.bot_addLine.setObjectName("bot_addLine")
        self.verticalLayout.addWidget(self.bot_addLine)
        self.bot_removeLine = QtWidgets.QPushButton(DialogInfoSpese)
        self.bot_removeLine.setMinimumSize(QtCore.QSize(30, 23))
        self.bot_removeLine.setMaximumSize(QtCore.QSize(30, 23))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.bot_removeLine.setFont(font)
        self.bot_removeLine.setFocusPolicy(QtCore.Qt.NoFocus)
        self.bot_removeLine.setObjectName("bot_removeLine")
        self.verticalLayout.addWidget(self.bot_removeLine)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.bot_ok = QtWidgets.QPushButton(DialogInfoSpese)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bot_ok.sizePolicy().hasHeightForWidth())
        self.bot_ok.setSizePolicy(sizePolicy)
        self.bot_ok.setMinimumSize(QtCore.QSize(40, 40))
        self.bot_ok.setMaximumSize(QtCore.QSize(40, 40))
        self.bot_ok.setObjectName("bot_ok")
        self.horizontalLayout_2.addWidget(self.bot_ok)
        self.bot_esci = QtWidgets.QPushButton(DialogInfoSpese)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bot_esci.sizePolicy().hasHeightForWidth())
        self.bot_esci.setSizePolicy(sizePolicy)
        self.bot_esci.setMinimumSize(QtCore.QSize(40, 40))
        self.bot_esci.setMaximumSize(QtCore.QSize(40, 40))
        self.bot_esci.setObjectName("bot_esci")
        self.horizontalLayout_2.addWidget(self.bot_esci)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        self.retranslateUi(DialogInfoSpese)
        QtCore.QMetaObject.connectSlotsByName(DialogInfoSpese)

    def retranslateUi(self, DialogInfoSpese):
        _translate = QtCore.QCoreApplication.translate
        DialogInfoSpese.setWindowTitle(_translate("DialogInfoSpese", "Spese"))
        self.bot_addLine.setText(_translate("DialogInfoSpese", "+"))
        self.bot_removeLine.setText(_translate("DialogInfoSpese", "-"))
        self.bot_ok.setText(_translate("DialogInfoSpese", "Ok"))
        self.bot_esci.setText(_translate("DialogInfoSpese", "Esci"))


from kwidget.mytablewidget.mytablewidget import MyTableWidget

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    DialogInfoSpese = QtWidgets.QDialog()
    ui = Ui_DialogInfoSpese()
    ui.setupUi(DialogInfoSpese)
    DialogInfoSpese.show()
    sys.exit(app.exec_())
