# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'my_dateedit_3.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets




class Ui_My_dateedit_3(object):
    def setupUi(self, my_dateedit_3):
        my_dateedit_3.setObjectName("my_dateedit_3")
        my_dateedit_3.resize(106, 52)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(my_dateedit_3.sizePolicy().hasHeightForWidth())
        my_dateedit_3.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(my_dateedit_3)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter = QtWidgets.QSplitter(my_dateedit_3)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.dateEdit = QtWidgets.QDateEdit(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dateEdit.sizePolicy().hasHeightForWidth())
        self.dateEdit.setSizePolicy(sizePolicy)
        self.dateEdit.setMinimumSize(QtCore.QSize(65, 34))
        self.dateEdit.setMaximumSize(QtCore.QSize(65, 34))
        self.dateEdit.setFrame(True)
        self.dateEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.dateEdit.setReadOnly(True)
        self.dateEdit.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.dateEdit.setObjectName("dateEdit")
        self.widget = QtWidgets.QWidget(self.splitter)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.bot_increase = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bot_increase.sizePolicy().hasHeightForWidth())
        self.bot_increase.setSizePolicy(sizePolicy)
        self.bot_increase.setMinimumSize(QtCore.QSize(16, 12))
        self.bot_increase.setMaximumSize(QtCore.QSize(16, 14))
        self.bot_increase.setIconSize(QtCore.QSize(4, 4))
        self.bot_increase.setObjectName("bot_increase")
        self.verticalLayout.addWidget(self.bot_increase)
        self.bot_decrease = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bot_decrease.sizePolicy().hasHeightForWidth())
        self.bot_decrease.setSizePolicy(sizePolicy)
        self.bot_decrease.setMinimumSize(QtCore.QSize(16, 12))
        self.bot_decrease.setMaximumSize(QtCore.QSize(16, 14))
        self.bot_decrease.setIconSize(QtCore.QSize(4, 4))
        self.bot_decrease.setObjectName("bot_decrease")
        self.verticalLayout.addWidget(self.bot_decrease)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)

        self.retranslateUi(my_dateedit_3)
        QtCore.QMetaObject.connectSlotsByName(my_dateedit_3)

    def retranslateUi(self, my_dateedit_3):
        _translate = QtCore.QCoreApplication.translate
        my_dateedit_3.setWindowTitle(_translate("my_dateedit_3", "Form"))
        self.bot_increase.setText(_translate("my_dateedit_3", "+"))
        self.bot_decrease.setText(_translate("my_dateedit_3", "-"))

class My_dateedit_3(Ui_My_dateedit_3, QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(My_dateedit_3, self).__init__(parent)
        self.setupUi(self)
        self.dateEdit.setDisplayFormat('MM/yyyy')
        self.bot_increase.clicked.connect(self.increase_month)
        self.bot_decrease.clicked.connect(self.decrease_month)

    def setDate(self,date:QtCore.QDate):
        return self.dateEdit.setDate(date)

    @property
    def date(self):
        return self.dateEdit.date()

    @date.setter
    def date(self, date):
        self.date = date

    def increase_month(self):
        self.setDate(self.date.addMonths(1))

    def decrease_month(self):
        self.setDate(self.date.addMonths(-1))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    my_dateedit_3 = QtWidgets.QWidget()
    ui = My_dateedit_3()
    ui.setupUi(my_dateedit_3)
    my_dateedit_3.show()
    sys.exit(app.exec_())
