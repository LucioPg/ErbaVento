from PyQt5 import QtCore, QtGui, QtWidgets
from kwidget.mydateedit.my_dateedit_3 import Ui_My_dateedit_3

class My_dateedit_3(Ui_My_dateedit_3, QtWidgets.QWidget):
    def __init__(self, parent=None, daily=False):
        super(My_dateedit_3, self).__init__(parent)
        self.daily = daily
        self.setupUi(self)
        self.dateEdit.setDisplayFormat('MM/yyyy')
        self.bot_increase.clicked.connect(self.increase)
        self.bot_decrease.clicked.connect(self.decrease)

    def setDate(self,date:QtCore.QDate):
        return self.dateEdit.setDate(date)

    @property
    def date(self):
        return self.dateEdit.date()

    @date.setter
    def date(self, date):
        self.date = date

    def increase(self):
        if not self.daily:
            self.setDate(self.date.addMonths(1))
        else:
            self.setDate(self.date.addDays(1))

    def decrease(self):
        if not self.daily:
            self.setDate(self.date.addMonths(-1))
        else:
            self.setDate(self.date.addDays(-1))