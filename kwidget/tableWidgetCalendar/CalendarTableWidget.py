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
    selectionChanged = pyqtSignal()
    yearChanged = pyqtSignal()


    def __init__(self,prenotazioni=None,pulizie=None,colors=None,parent=None):
        super(CalendarTableWidget, self).__init__(parent)
        self.datePrenotazioni = prenotazioni
        self.datePulizie = pulizie
        self.colors = colors
        self.setAlphaColors()
        self.oggi = QDate().currentDate()
        self.setupUi(self)

    def createDates(self):
        """create dict for dates in the selected Year and selected Month"""
        pass

    def populateWithComplexLabels(self):
        """populate the table with the complexlabels"""
        pass

    def selectedDate(self) -> QDate:
        """:returns the date in the selected cell"""
        pass

    def setAlphaColors(self, alpha=150):
        """set the alpha of the color background as the value for all the colors"""
        for color in self.colors:
            color.setAlpha(150)

    def setCurrentPage(self):
        """set the current page shown as month for the selected year"""
        pass

    def setDates(self,prenotazioni, pulizie, colors):
        """mimic the old version of calendar"""
        print('this func is obsolete, please change it as it does nothing')

    def setListe(self, listaAsDict: dict = None) -> dict:
        """mimic the old version of calendar"""
        print('this func is obsolete, please change it')
        if listaAsDict is None:
            print('Attenzione la listaDizionario passata è nulla')
            return dict()
        listaDate = {}
        for i in listaAsDict.keys():
            for l in listaAsDict[i].keys():
                for data in listaAsDict[i][l]['date']:
                    if data not in listaDate:
                        listaDate[data] = l
        return listaDate

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