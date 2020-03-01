from PyQt5 import QtCore, QtGui, QtWidgets
from kwidget.mydateedit.my_dateedit_3 import Ui_My_dateedit_3

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