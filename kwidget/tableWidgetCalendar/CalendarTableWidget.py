from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import (QTableWidget, QComboBox, QPushButton)
from PyQt5.QtCore import (QDate, pyqtSignal, pyqtSlot)
from kwidget.tableWidgetCalendar.gui_calendar import Ui_CalendarTableWid as Calendar
from kwidget.complexlabel.complexLabels import ComplexLabel
from tools.meseGiorniDictGen import MeseGiorniDictGen
import sys


class CalendarTableWidget(Calendar,QtWidgets.QTableWidget):
    #Signals:
    currentPageChanged = pyqtSignal()


    def __init__(self,parent=None):
        super(CalendarTableWidget, self).__init__(parent)
        self.setupUi(self)

    def createDates(self):
        """create dict for dates in the selected Year and selected Month"""
        pass

    def populateWithComplexLabels(self):
        """populate the table with the complexlabels"""
        pass

    def setCurrentPage(self):
        """set the current page shown as month for the selected year"""
        pass

    def setDayNumInComplexLabel(self):
        """set the number of the day in the label of the complexlabel widget"""
        pass

    def setIconComplexLabel(self):
        """set the icon for the complexlabel in the right date"""
        pass

    def showNextMonth(self):
        """show the next month in the table"""
        pass

    def showNextYear(self):
        """show the next year in the table"""
        pass

    def showPreviousMonth(self):
        """show th previous month in the table"""
        pass

    def showPreviousYear(self):
        """show th previous year in the table"""
        pass

    def showSelectedDate(self):
        """show the selected date"""
        pass

    def showToday(self):
        """show today"""
        pass




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    hbox = QtWidgets.QHBoxLayout()
    simpleWidget = CalendarTableWidget(dialog)
    hbox.addWidget(simpleWidget)
    dialog.setLayout(hbox)
    dialog.show()
    sys.exit(app.exec_())