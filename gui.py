# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(862, 885)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab1 = QtWidgets.QWidget()
        self.tab1.setObjectName("tab1")
        self.gridLayout = QtWidgets.QGridLayout(self.tab1)
        self.gridLayout.setObjectName("gridLayout")
        self.frame_calendar = QtWidgets.QFrame(self.tab1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_calendar.sizePolicy().hasHeightForWidth())
        self.frame_calendar.setSizePolicy(sizePolicy)
        self.frame_calendar.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_calendar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_calendar.setObjectName("frame_calendar")
        self.gridLayout.addWidget(self.frame_calendar, 0, 0, 1, 1)
        self.horizontalLayout_22 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_22.setObjectName("horizontalLayout_22")
        self.tableWidget_info_ospite = QtWidgets.QTableWidget(self.tab1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget_info_ospite.sizePolicy().hasHeightForWidth())
        self.tableWidget_info_ospite.setSizePolicy(sizePolicy)
        self.tableWidget_info_ospite.setMaximumSize(QtCore.QSize(300, 220))
        self.tableWidget_info_ospite.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tableWidget_info_ospite.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_info_ospite.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_info_ospite.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_info_ospite.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tableWidget_info_ospite.setShowGrid(False)
        self.tableWidget_info_ospite.setObjectName("tableWidget_info_ospite")
        self.tableWidget_info_ospite.setColumnCount(2)
        self.tableWidget_info_ospite.setRowCount(6)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_info_ospite.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_info_ospite.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_info_ospite.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_info_ospite.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_info_ospite.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_info_ospite.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_info_ospite.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_info_ospite.setHorizontalHeaderItem(1, item)
        self.tableWidget_info_ospite.horizontalHeader().setVisible(False)
        self.tableWidget_info_ospite.horizontalHeader().setDefaultSectionSize(115)
        self.tableWidget_info_ospite.horizontalHeader().setMinimumSectionSize(50)
        self.tableWidget_info_ospite.horizontalHeader().setStretchLastSection(False)
        self.horizontalLayout_22.addWidget(self.tableWidget_info_ospite)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_22.addItem(spacerItem)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setContentsMargins(-1, -1, 24, -1)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.bot_spese = QtWidgets.QPushButton(self.tab1)
        self.bot_spese.setObjectName("bot_spese")
        self.horizontalLayout.addWidget(self.bot_spese)
        self.label_data = QtWidgets.QLabel(self.tab1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_data.sizePolicy().hasHeightForWidth())
        self.label_data.setSizePolicy(sizePolicy)
        self.label_data.setMinimumSize(QtCore.QSize(90, 0))
        self.label_data.setText("")
        self.label_data.setObjectName("label_data")
        self.horizontalLayout.addWidget(self.label_data)
        self.verticalLayout_10.addLayout(self.horizontalLayout)
        self.bot_foglio = QtWidgets.QPushButton(self.tab1)
        self.bot_foglio.setObjectName("bot_foglio")
        self.verticalLayout_10.addWidget(self.bot_foglio)
        self.bot_cancella = QtWidgets.QPushButton(self.tab1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bot_cancella.sizePolicy().hasHeightForWidth())
        self.bot_cancella.setSizePolicy(sizePolicy)
        self.bot_cancella.setMinimumSize(QtCore.QSize(131, 51))
        self.bot_cancella.setMaximumSize(QtCore.QSize(131, 51))
        self.bot_cancella.setObjectName("bot_cancella")
        self.verticalLayout_10.addWidget(self.bot_cancella)
        self.horizontalLayout_22.addLayout(self.verticalLayout_10)
        self.gridLayout.addLayout(self.horizontalLayout_22, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab1, "")
        self.tab2 = QtWidgets.QWidget()
        self.tab2.setObjectName("tab2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_referente = QtWidgets.QLabel(self.tab2)
        self.label_referente.setObjectName("label_referente")
        self.horizontalLayout_6.addWidget(self.label_referente)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.line = QtWidgets.QFrame(self.tab2)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.verticalLayout_6.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_nome = QtWidgets.QLabel(self.tab2)
        self.label_nome.setAlignment(QtCore.Qt.AlignCenter)
        self.label_nome.setObjectName("label_nome")
        self.horizontalLayout_2.addWidget(self.label_nome)
        self.lineEdit_nome = QtWidgets.QLineEdit(self.tab2)
        self.lineEdit_nome.setMinimumSize(QtCore.QSize(256, 21))
        self.lineEdit_nome.setMaximumSize(QtCore.QSize(21, 256))
        self.lineEdit_nome.setObjectName("lineEdit_nome")
        self.horizontalLayout_2.addWidget(self.lineEdit_nome)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.tab2)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.lineEdit_cognome = QtWidgets.QLineEdit(self.tab2)
        self.lineEdit_cognome.setMinimumSize(QtCore.QSize(256, 21))
        self.lineEdit_cognome.setMaximumSize(QtCore.QSize(21, 256))
        self.lineEdit_cognome.setObjectName("lineEdit_cognome")
        self.horizontalLayout_3.addWidget(self.lineEdit_cognome)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.tab2)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.lineEdit_telefono = QtWidgets.QLineEdit(self.tab2)
        self.lineEdit_telefono.setMinimumSize(QtCore.QSize(256, 21))
        self.lineEdit_telefono.setMaximumSize(QtCore.QSize(21, 256))
        self.lineEdit_telefono.setObjectName("lineEdit_telefono")
        self.horizontalLayout_4.addWidget(self.lineEdit_telefono)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.verticalLayout_6.addLayout(self.verticalLayout)
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.radio_privato = QtWidgets.QRadioButton(self.tab2)
        self.radio_privato.setObjectName("radio_privato")
        self.horizontalLayout_18.addWidget(self.radio_privato)
        self.radio_booking = QtWidgets.QRadioButton(self.tab2)
        self.radio_booking.setChecked(True)
        self.radio_booking.setObjectName("radio_booking")
        self.horizontalLayout_18.addWidget(self.radio_booking)
        self.radio_air = QtWidgets.QRadioButton(self.tab2)
        self.radio_air.setObjectName("radio_air")
        self.horizontalLayout_18.addWidget(self.radio_air)
        self.verticalLayout_6.addLayout(self.horizontalLayout_18)
        self.horizontalLayout_19.addLayout(self.verticalLayout_6)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_19.addItem(spacerItem5)
        self.verticalLayout_7.addLayout(self.horizontalLayout_19)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_5 = QtWidgets.QLabel(self.tab2)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_5.addWidget(self.label_5)
        self.dateEdit_dal = QtWidgets.QDateEdit(self.tab2)
        self.dateEdit_dal.setDateTime(QtCore.QDateTime(QtCore.QDate(2019, 7, 14), QtCore.QTime(0, 0, 0)))
        self.dateEdit_dal.setMinimumDate(QtCore.QDate(2019, 7, 14))
        self.dateEdit_dal.setObjectName("dateEdit_dal")
        self.horizontalLayout_5.addWidget(self.dateEdit_dal)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem6)
        self.label_6 = QtWidgets.QLabel(self.tab2)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_5.addWidget(self.label_6)
        self.dateEdit_al = QtWidgets.QDateEdit(self.tab2)
        self.dateEdit_al.setDateTime(QtCore.QDateTime(QtCore.QDate(2019, 7, 14), QtCore.QTime(0, 0, 0)))
        self.dateEdit_al.setMinimumDateTime(QtCore.QDateTime(QtCore.QDate(2019, 7, 14), QtCore.QTime(0, 0, 0)))
        self.dateEdit_al.setObjectName("dateEdit_al")
        self.horizontalLayout_5.addWidget(self.dateEdit_al)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem7)
        self.verticalLayout_7.addLayout(self.horizontalLayout_5)
        self.line_3 = QtWidgets.QFrame(self.tab2)
        self.line_3.setMinimumSize(QtCore.QSize(641, 0))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_7.addWidget(self.line_3)
        self.gridLayout_2.addLayout(self.verticalLayout_7, 0, 0, 1, 3)
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.horizontalLayout_24 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_24.setObjectName("horizontalLayout_24")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_8 = QtWidgets.QLabel(self.tab2)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_7.addWidget(self.label_8)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem8)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.line_2 = QtWidgets.QFrame(self.tab2)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_3.addWidget(self.line_2)
        self.horizontalLayout_13.addLayout(self.verticalLayout_3)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem9)
        self.verticalLayout_8.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_9 = QtWidgets.QLabel(self.tab2)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_8.addWidget(self.label_9)
        self.spinBox_ospiti = QtWidgets.QSpinBox(self.tab2)
        self.spinBox_ospiti.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_ospiti.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.spinBox_ospiti.setMinimum(1)
        self.spinBox_ospiti.setMaximum(5)
        self.spinBox_ospiti.setObjectName("spinBox_ospiti")
        self.horizontalLayout_8.addWidget(self.spinBox_ospiti)
        self.horizontalLayout_14.addLayout(self.horizontalLayout_8)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem10)
        self.verticalLayout_8.addLayout(self.horizontalLayout_14)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_10 = QtWidgets.QLabel(self.tab2)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_9.addWidget(self.label_10)
        self.spinBox_bambini = QtWidgets.QSpinBox(self.tab2)
        self.spinBox_bambini.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_bambini.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.spinBox_bambini.setObjectName("spinBox_bambini")
        self.horizontalLayout_9.addWidget(self.spinBox_bambini)
        self.horizontalLayout_15.addLayout(self.horizontalLayout_9)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_15.addItem(spacerItem11)
        self.verticalLayout_8.addLayout(self.horizontalLayout_15)
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.radio_colazione = QtWidgets.QRadioButton(self.tab2)
        self.radio_colazione.setObjectName("radio_colazione")
        self.horizontalLayout_10.addWidget(self.radio_colazione)
        self.horizontalLayout_16.addLayout(self.horizontalLayout_10)
        self.pushButton_3 = QtWidgets.QPushButton(self.tab2)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_16.addWidget(self.pushButton_3)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_16.addItem(spacerItem12)
        self.verticalLayout_8.addLayout(self.horizontalLayout_16)
        self.horizontalLayout_24.addLayout(self.verticalLayout_8)
        self.horizontalLayout_23 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_23.setObjectName("horizontalLayout_23")
        self.label = QtWidgets.QLabel(self.tab2)
        self.label.setObjectName("label")
        self.horizontalLayout_23.addWidget(self.label)
        self.spinBox_importo = QtWidgets.QSpinBox(self.tab2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_importo.sizePolicy().hasHeightForWidth())
        self.spinBox_importo.setSizePolicy(sizePolicy)
        self.spinBox_importo.setMinimumSize(QtCore.QSize(48, 0))
        self.spinBox_importo.setMaximumSize(QtCore.QSize(48, 16777215))
        self.spinBox_importo.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_importo.setProperty("value", 40)
        self.spinBox_importo.setObjectName("spinBox_importo")
        self.horizontalLayout_23.addWidget(self.spinBox_importo)
        self.horizontalLayout_24.addLayout(self.horizontalLayout_23)
        self.verticalLayout_9.addLayout(self.horizontalLayout_24)
        spacerItem13 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_9.addItem(spacerItem13)
        self.horizontalLayout_25 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_25.setObjectName("horizontalLayout_25")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_11 = QtWidgets.QLabel(self.tab2)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_11.addWidget(self.label_11)
        self.lineEdit_lordo = QtWidgets.QLineEdit(self.tab2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_lordo.sizePolicy().hasHeightForWidth())
        self.lineEdit_lordo.setSizePolicy(sizePolicy)
        self.lineEdit_lordo.setMinimumSize(QtCore.QSize(83, 21))
        self.lineEdit_lordo.setMaximumSize(QtCore.QSize(83, 21))
        self.lineEdit_lordo.setReadOnly(True)
        self.lineEdit_lordo.setObjectName("lineEdit_lordo")
        self.horizontalLayout_11.addWidget(self.lineEdit_lordo)
        self.horizontalLayout_25.addLayout(self.horizontalLayout_11)
        spacerItem14 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_25.addItem(spacerItem14)
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.label_13 = QtWidgets.QLabel(self.tab2)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_17.addWidget(self.label_13)
        self.lineEdit_tax = QtWidgets.QLineEdit(self.tab2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_tax.sizePolicy().hasHeightForWidth())
        self.lineEdit_tax.setSizePolicy(sizePolicy)
        self.lineEdit_tax.setMinimumSize(QtCore.QSize(83, 21))
        self.lineEdit_tax.setMaximumSize(QtCore.QSize(83, 21))
        self.lineEdit_tax.setReadOnly(True)
        self.lineEdit_tax.setObjectName("lineEdit_tax")
        self.horizontalLayout_17.addWidget(self.lineEdit_tax)
        self.horizontalLayout_25.addLayout(self.horizontalLayout_17)
        spacerItem15 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_25.addItem(spacerItem15)
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        self.label_14 = QtWidgets.QLabel(self.tab2)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_20.addWidget(self.label_14)
        self.lineEdit_netto = QtWidgets.QLineEdit(self.tab2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_netto.sizePolicy().hasHeightForWidth())
        self.lineEdit_netto.setSizePolicy(sizePolicy)
        self.lineEdit_netto.setMinimumSize(QtCore.QSize(83, 21))
        self.lineEdit_netto.setMaximumSize(QtCore.QSize(83, 21))
        self.lineEdit_netto.setReadOnly(True)
        self.lineEdit_netto.setObjectName("lineEdit_netto")
        self.horizontalLayout_20.addWidget(self.lineEdit_netto)
        self.horizontalLayout_25.addLayout(self.horizontalLayout_20)
        spacerItem16 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_25.addItem(spacerItem16)
        self.verticalLayout_9.addLayout(self.horizontalLayout_25)
        self.line_4 = QtWidgets.QFrame(self.tab2)
        self.line_4.setMinimumSize(QtCore.QSize(641, 0))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout_9.addWidget(self.line_4)
        self.gridLayout_2.addLayout(self.verticalLayout_9, 1, 0, 3, 3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        spacerItem17 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem17)
        self.label_12 = QtWidgets.QLabel(self.tab2)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_12.addWidget(self.label_12)
        spacerItem18 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem18)
        self.verticalLayout_4.addLayout(self.horizontalLayout_12)
        self.plainTextEdit_note = QtWidgets.QPlainTextEdit(self.tab2)
        self.plainTextEdit_note.setObjectName("plainTextEdit_note")
        self.verticalLayout_4.addWidget(self.plainTextEdit_note)
        self.gridLayout_2.addLayout(self.verticalLayout_4, 4, 0, 1, 1)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        spacerItem19 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem19)
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.bot_salva = QtWidgets.QPushButton(self.tab2)
        self.bot_salva.setObjectName("bot_salva")
        self.horizontalLayout_21.addWidget(self.bot_salva)
        self.bot_annulla = QtWidgets.QPushButton(self.tab2)
        self.bot_annulla.setObjectName("bot_annulla")
        self.horizontalLayout_21.addWidget(self.bot_annulla)
        self.bot_checkDisp = QtWidgets.QPushButton(self.tab2)
        self.bot_checkDisp.setObjectName("bot_checkDisp")
        self.horizontalLayout_21.addWidget(self.bot_checkDisp)
        self.verticalLayout_5.addLayout(self.horizontalLayout_21)
        self.gridLayout_2.addLayout(self.verticalLayout_5, 4, 1, 1, 2)
        spacerItem20 = QtWidgets.QSpacerItem(401, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem20, 2, 2, 2, 1)
        self.tabWidget.addTab(self.tab2, "")
        self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 862, 21))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuMenu.menuAction())
        self.label_nome.setBuddy(self.lineEdit_nome)
        self.label_3.setBuddy(self.lineEdit_cognome)
        self.label_4.setBuddy(self.lineEdit_telefono)
        self.label_5.setBuddy(self.dateEdit_dal)
        self.label_6.setBuddy(self.dateEdit_al)
        self.label_9.setBuddy(self.spinBox_ospiti)
        self.label_10.setBuddy(self.spinBox_bambini)
        self.label.setBuddy(self.spinBox_importo)
        self.label_11.setBuddy(self.lineEdit_lordo)
        self.label_13.setBuddy(self.lineEdit_tax)
        self.label_14.setBuddy(self.lineEdit_netto)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        item = self.tableWidget_info_ospite.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "Nome"))
        item = self.tableWidget_info_ospite.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "Cognome"))
        item = self.tableWidget_info_ospite.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "#ospiti"))
        item = self.tableWidget_info_ospite.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "bambini"))
        item = self.tableWidget_info_ospite.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "privato"))
        item = self.tableWidget_info_ospite.verticalHeaderItem(5)
        item.setText(_translate("MainWindow", "In-->Out"))
        item = self.tableWidget_info_ospite.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.tableWidget_info_ospite.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "New Column"))
        self.bot_spese.setText(_translate("MainWindow", "Spese"))
        self.bot_foglio.setText(_translate("MainWindow", "foglio elettronico"))
        self.bot_cancella.setText(_translate("MainWindow", "Cancella Prenotazione"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab1), _translate("MainWindow", "Calendario"))
        self.label_referente.setText(_translate("MainWindow", "Referente"))
        self.label_nome.setText(_translate("MainWindow", "Nome:"))
        self.label_3.setText(_translate("MainWindow", "cognome:"))
        self.label_4.setText(_translate("MainWindow", "telefono:"))
        self.radio_privato.setText(_translate("MainWindow", "Privato"))
        self.radio_booking.setText(_translate("MainWindow", "Booking.com"))
        self.radio_air.setText(_translate("MainWindow", "AirB&B"))
        self.label_5.setText(_translate("MainWindow", "dal:"))
        self.label_6.setText(_translate("MainWindow", "al:"))
        self.label_8.setText(_translate("MainWindow", "Ospiti"))
        self.label_9.setText(_translate("MainWindow", "Numero:"))
        self.label_10.setText(_translate("MainWindow", "bambini:"))
        self.radio_colazione.setText(_translate("MainWindow", "colazione"))
        self.pushButton_3.setText(_translate("MainWindow", "aggiungi spesa"))
        self.label.setText(_translate("MainWindow", "Importo:"))
        self.label_11.setText(_translate("MainWindow", "Lordo"))
        self.label_13.setText(_translate("MainWindow", "Tax"))
        self.label_14.setText(_translate("MainWindow", "Netto"))
        self.label_12.setText(_translate("MainWindow", "NOTE:"))
        self.bot_salva.setText(_translate("MainWindow", "salva"))
        self.bot_annulla.setText(_translate("MainWindow", "annulla"))
        self.bot_checkDisp.setText(_translate("MainWindow", "disponnibilità"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab2), _translate("MainWindow", "Prenota"))
        self.menuMenu.setTitle(_translate("MainWindow", "Menu"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
