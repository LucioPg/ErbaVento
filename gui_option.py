# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_option.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_opt(object):
    def setupUi(self, Dialog_opt):
        Dialog_opt.setObjectName("Dialog_opt")
        Dialog_opt.setWindowModality(QtCore.Qt.WindowModal)
        Dialog_opt.resize(571, 385)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog_opt.sizePolicy().hasHeightForWidth())
        Dialog_opt.setSizePolicy(sizePolicy)
        Dialog_opt.setMinimumSize(QtCore.QSize(571, 385))
        Dialog_opt.setMaximumSize(QtCore.QSize(571, 385))
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog_opt)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 143, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 2, 2, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog_opt)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_2.addWidget(self.buttonBox, 1, 2, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(Dialog_opt)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_struttura = QtWidgets.QWidget()
        self.tab_struttura.setObjectName("tab_struttura")
        self.gridLayout = QtWidgets.QGridLayout(self.tab_struttura)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.tab_struttura)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.line = QtWidgets.QFrame(self.tab_struttura)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.combo_stagione = QtWidgets.QComboBox(self.tab_struttura)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo_stagione.sizePolicy().hasHeightForWidth())
        self.combo_stagione.setSizePolicy(sizePolicy)
        self.combo_stagione.setMinimumSize(QtCore.QSize(61, 23))
        self.combo_stagione.setMaximumSize(QtCore.QSize(61, 23))
        self.combo_stagione.setObjectName("combo_stagione")
        self.combo_stagione.addItem("")
        self.combo_stagione.addItem("")
        self.combo_stagione.addItem("")
        self.verticalLayout.addWidget(self.combo_stagione)
        self.horizontalLayout_7.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        self.gridLayout.addLayout(self.verticalLayout_2, 1, 0, 1, 1)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.line_2 = QtWidgets.QFrame(self.tab_struttura)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_5.addWidget(self.line_2)
        self.label_4 = QtWidgets.QLabel(self.tab_struttura)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_5.addWidget(self.label_4)
        self.verticalLayout_6.addLayout(self.verticalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_5 = QtWidgets.QLabel(self.tab_struttura)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QtCore.QSize(81, 20))
        self.label_5.setMaximumSize(QtCore.QSize(81, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.label_numeroLetti = QtWidgets.QLabel(self.tab_struttura)
        self.label_numeroLetti.setObjectName("label_numeroLetti")
        self.horizontalLayout_3.addWidget(self.label_numeroLetti)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.bot_sottraiLetto = QtWidgets.QPushButton(self.tab_struttura)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bot_sottraiLetto.sizePolicy().hasHeightForWidth())
        self.bot_sottraiLetto.setSizePolicy(sizePolicy)
        self.bot_sottraiLetto.setMinimumSize(QtCore.QSize(21, 23))
        self.bot_sottraiLetto.setMaximumSize(QtCore.QSize(21, 23))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.bot_sottraiLetto.setFont(font)
        self.bot_sottraiLetto.setStyleSheet("\n"
                                            "                                                    font:rgba(126, 240, 87, 229);\n"
                                            "                                                ")
        self.bot_sottraiLetto.setObjectName("bot_sottraiLetto")
        self.horizontalLayout_5.addWidget(self.bot_sottraiLetto)
        self.bot_aggiungiLetto = QtWidgets.QPushButton(self.tab_struttura)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bot_aggiungiLetto.sizePolicy().hasHeightForWidth())
        self.bot_aggiungiLetto.setSizePolicy(sizePolicy)
        self.bot_aggiungiLetto.setMinimumSize(QtCore.QSize(21, 23))
        self.bot_aggiungiLetto.setMaximumSize(QtCore.QSize(21, 23))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.bot_aggiungiLetto.setFont(font)
        self.bot_aggiungiLetto.setStyleSheet("\n"
                                             "                                                    font:rgba(126, 240, 87, 229);\n"
                                             "                                                ")
        self.bot_aggiungiLetto.setObjectName("bot_aggiungiLetto")
        self.horizontalLayout_5.addWidget(self.bot_aggiungiLetto)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.line_4 = QtWidgets.QFrame(self.tab_struttura)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout_4.addWidget(self.line_4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_8 = QtWidgets.QLabel(self.tab_struttura)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setMinimumSize(QtCore.QSize(81, 20))
        self.label_8.setMaximumSize(QtCore.QSize(81, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_8.addWidget(self.label_8)
        self.spinbox_provvigione = QtWidgets.QDoubleSpinBox(self.tab_struttura)
        self.spinbox_provvigione.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinbox_provvigione.sizePolicy().hasHeightForWidth())
        self.spinbox_provvigione.setSizePolicy(sizePolicy)
        self.spinbox_provvigione.setMinimumSize(QtCore.QSize(65, 20))
        self.spinbox_provvigione.setMaximumSize(QtCore.QSize(65, 20))
        self.spinbox_provvigione.setAlignment(QtCore.Qt.AlignCenter)
        self.spinbox_provvigione.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.spinbox_provvigione.setMinimum(0.0)
        self.spinbox_provvigione.setMaximum(100.0)
        self.spinbox_provvigione.setSingleStep(1.0)
        self.spinbox_provvigione.setProperty("value", 0.0)
        self.spinbox_provvigione.setObjectName("spinbox_provvigione")
        self.horizontalLayout_8.addWidget(self.spinbox_provvigione)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.horizontalLayout_8)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.line_3 = QtWidgets.QFrame(self.tab_struttura)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_4.addWidget(self.line_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_9 = QtWidgets.QLabel(self.tab_struttura)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setMinimumSize(QtCore.QSize(81, 20))
        self.label_9.setMaximumSize(QtCore.QSize(81, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_2.addWidget(self.label_9)
        self.spinbox_tasse = QtWidgets.QDoubleSpinBox(self.tab_struttura)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinbox_tasse.sizePolicy().hasHeightForWidth())
        self.spinbox_tasse.setSizePolicy(sizePolicy)
        self.spinbox_tasse.setMinimumSize(QtCore.QSize(65, 20))
        self.spinbox_tasse.setMaximumSize(QtCore.QSize(65, 20))
        self.spinbox_tasse.setAlignment(QtCore.Qt.AlignCenter)
        self.spinbox_tasse.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.spinbox_tasse.setMinimum(0.0)
        self.spinbox_tasse.setMaximum(100.0)
        self.spinbox_tasse.setSingleStep(1.0)
        self.spinbox_tasse.setProperty("value", 0.0)
        self.spinbox_tasse.setObjectName("spinbox_tasse")
        self.horizontalLayout_2.addWidget(self.spinbox_tasse)
        self.radio_attivaTassa = QtWidgets.QRadioButton(self.tab_struttura)
        self.radio_attivaTassa.setObjectName("radio_attivaTassa")
        self.horizontalLayout_2.addWidget(self.radio_attivaTassa)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.line_5 = QtWidgets.QFrame(self.tab_struttura)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.verticalLayout_4.addWidget(self.line_5)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_10 = QtWidgets.QLabel(self.tab_struttura)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setMinimumSize(QtCore.QSize(81, 20))
        self.label_10.setMaximumSize(QtCore.QSize(81, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_9.addWidget(self.label_10)
        self.bot_scegliColore = QtWidgets.QPushButton(self.tab_struttura)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bot_scegliColore.sizePolicy().hasHeightForWidth())
        self.bot_scegliColore.setSizePolicy(sizePolicy)
        self.bot_scegliColore.setMinimumSize(QtCore.QSize(55, 13))
        self.bot_scegliColore.setMaximumSize(QtCore.QSize(55, 13))
        self.bot_scegliColore.setStyleSheet("QPushButton{border:0px}\n"
                                            "                                                                        ")
        self.bot_scegliColore.setText("")
        self.bot_scegliColore.setObjectName("bot_scegliColore")
        self.horizontalLayout_9.addWidget(self.bot_scegliColore)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_9)
        self.line_6 = QtWidgets.QFrame(self.tab_struttura)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.verticalLayout_4.addWidget(self.line_6)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem4)
        self.horizontalLayout_6.addLayout(self.verticalLayout_4)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_6 = QtWidgets.QLabel(self.tab_struttura)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMinimumSize(QtCore.QSize(81, 20))
        self.label_6.setMaximumSize(QtCore.QSize(81, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_4.addWidget(self.label_6)
        self.combo_platform = QtWidgets.QComboBox(self.tab_struttura)
        self.combo_platform.setObjectName("combo_platform")
        self.combo_platform.addItem("")
        self.combo_platform.addItem("")
        self.combo_platform.addItem("")
        self.horizontalLayout_4.addWidget(self.combo_platform)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.tableWidget__importi = QtWidgets.QTableWidget(self.tab_struttura)
        self.tableWidget__importi.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        self.tableWidget__importi.setDragDropOverwriteMode(False)
        self.tableWidget__importi.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget__importi.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget__importi.setShowGrid(True)
        self.tableWidget__importi.setGridStyle(QtCore.Qt.DashLine)
        self.tableWidget__importi.setWordWrap(False)
        self.tableWidget__importi.setCornerButtonEnabled(False)
        self.tableWidget__importi.setRowCount(1)
        self.tableWidget__importi.setColumnCount(2)
        self.tableWidget__importi.setObjectName("tableWidget__importi")
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget__importi.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget__importi.setHorizontalHeaderItem(1, item)
        self.tableWidget__importi.horizontalHeader().setVisible(True)
        self.tableWidget__importi.horizontalHeader().setHighlightSections(False)
        self.tableWidget__importi.horizontalHeader().setMinimumSectionSize(70)
        self.tableWidget__importi.horizontalHeader().setStretchLastSection(True)
        self.tableWidget__importi.verticalHeader().setVisible(False)
        self.verticalLayout_3.addWidget(self.tableWidget__importi)
        self.horizontalLayout_6.addLayout(self.verticalLayout_3)
        self.verticalLayout_6.addLayout(self.horizontalLayout_6)
        self.gridLayout.addLayout(self.verticalLayout_6, 2, 0, 1, 1)
        self.label.raise_()
        self.tabWidget.addTab(self.tab_struttura, "")
        self.tab_generale = QtWidgets.QWidget()
        self.tab_generale.setEnabled(True)
        self.tab_generale.setObjectName("tab_generale")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_generale)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_7 = QtWidgets.QLabel(self.tab_generale)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_generale, "")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 5, 2)

        self.retranslateUi(Dialog_opt)
        self.tabWidget.setCurrentIndex(0)
        self.buttonBox.accepted.connect(Dialog_opt.accept)
        self.buttonBox.rejected.connect(Dialog_opt.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_opt)

    def retranslateUi(self, Dialog_opt):
        _translate = QtCore.QCoreApplication.translate
        Dialog_opt.setWindowTitle(_translate("Dialog_opt", "EvInterface -Configurazione"))
        self.label.setText(_translate("Dialog_opt", "Stagione"))
        self.combo_stagione.setItemText(0, _translate("Dialog_opt", "Alta"))
        self.combo_stagione.setItemText(1, _translate("Dialog_opt", "Media"))
        self.combo_stagione.setItemText(2, _translate("Dialog_opt", "Bassa"))
        self.label_4.setText(_translate("Dialog_opt", "Importi"))
        self.label_5.setText(_translate("Dialog_opt", "Numero Letti:"))
        self.label_numeroLetti.setText(_translate("Dialog_opt", "TextLabel"))
        self.bot_sottraiLetto.setText(_translate("Dialog_opt", "-"))
        self.bot_aggiungiLetto.setText(_translate("Dialog_opt", "+"))
        self.label_8.setText(_translate("Dialog_opt", "Provvigione:"))
        self.spinbox_provvigione.setSuffix(_translate("Dialog_opt", "%"))
        self.label_9.setText(_translate("Dialog_opt", "Tasse:"))
        self.spinbox_tasse.setSuffix(_translate("Dialog_opt", "€"))
        self.radio_attivaTassa.setText(_translate("Dialog_opt", "Attiva"))
        self.label_10.setText(_translate("Dialog_opt", "Colore"))
        self.label_6.setText(_translate("Dialog_opt", "Platform:"))
        self.combo_platform.setItemText(0, _translate("Dialog_opt", "Booking"))
        self.combo_platform.setItemText(1, _translate("Dialog_opt", "AirB&B"))
        self.combo_platform.setItemText(2, _translate("Dialog_opt", "Privati"))
        self.tableWidget__importi.setToolTip(_translate("Dialog_opt", "Doppio click su una riga per impostare il\n"
                                                                      "                                                                    prezzo\n"
                                                                      "                                                                "))
        item = self.tableWidget__importi.horizontalHeaderItem(0)
        item.setText(_translate("Dialog_opt", "Numero Letti"))
        item = self.tableWidget__importi.horizontalHeaderItem(1)
        item.setText(_translate("Dialog_opt", "€"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_struttura), _translate("Dialog_opt", "Struttura"))
        self.label_7.setText(_translate("Dialog_opt", "UNDER CONSTRUCTION"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_generale), _translate("Dialog_opt", "Generale"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog_opt = QtWidgets.QDialog()
    ui = Ui_Dialog_opt()
    ui.setupUi(Dialog_opt)
    Dialog_opt.show()
    sys.exit(app.exec_())
