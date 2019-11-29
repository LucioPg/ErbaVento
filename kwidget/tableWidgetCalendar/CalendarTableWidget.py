from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import (QTableWidget, QComboBox, QPushButton, QWidget, QTableWidgetItem, QMainWindow,
                             QHeaderView, QAbstractItemView)
from PyQt5.QtCore import (QDate, pyqtSignal, pyqtSlot, Qt, QSize, QRect, QModelIndex, QItemSelectionModel)
from PyQt5.QtGui import (QPen, QBrush, QPainter, QColor, QIcon)
from kwidget.tableWidgetCalendar.gui_calendar import Ui_CalendarTableWid as Calendar
from kwidget.complexlabel.complexLabels import ComplexLabel
from tools.meseGiorniDictGen import MeseGiorniDictGen
import sys

# todo la selezione della cella deve essere connessa alla data e non alla posizione della cella, di conseguenza cambiando
# todo pagina al calendario la data selezionata deve rimanere la stessa
# TODO SISTEMARE IL SEGNALE selectionChanged

class CalendarTableWidget(Calendar, QWidget):
    #Signals:
    currentPageChanged = pyqtSignal(int) #indice per il mese
    selectionChanged = pyqtSignal(QDate)
    clicked = pyqtSignal(QDate)
    yearChanged = pyqtSignal() #anno corrente
    listaGiorniDellAnnoChanged = pyqtSignal(int)
    headerStyleSheet = "QHeaderView::section { background-color:gray; font-size:20px; border:0px;}"
    def __init__(self, prenotazioni=None, pulizie=None, colors=None, parent=None):
        super(CalendarTableWidget, self).__init__(parent)
        self.setupUi(self)
        self.cellSelectedList = [None]
        self.datePrenotazioni = prenotazioni
        self.datePulizie = pulizie
        self.colors = colors
        self.setAlphaColors()
        self.oggi = QDate().currentDate()
        self.currentYear = self.oggi.year()
        self.setLabelAnno(self.currentYear)
        self.currentMonth = self.oggi.month()
        self.currentRowCol = None
        self.indexMonth = self.oggi.month() - 1
        # self.baseDate = self.oggi
        self.setBaseDate(self.oggi)
        self.setListaGiorniDellAnno(self.createDates())
        self.daysInTheMonth = [] #serve a evidenziare i giorni del mese corrente
        self.formatTable()
        print('selectCEll from init')
        self.selectCell(self.oggi)
        self.signalsConnections()

    def changeDisplayedMonth(self):
        """ changes the month displayed in the calendar"""
        #ho bisogno di sapere qual è il mese mostrato
        currentMonth = self.indexMonth
        currentYear = self.currentYear

        sender = self.sender().objectName()
        if sender == 'bot_next':
            # if currentMonth < 11:
            if self.indexMonth < 11:
                self.indexMonth += 1
                self.setBaseDate(self.baseDate.addMonths(1))
            else:
                self.indexMonth = 0
                self.setCurrentYear(currentYear+1)
                self.setBaseDate(self.baseDate.addMonths(1))
                # print('new Year: ', self.currentYear)

        elif sender == 'bot_prev':
            # if currentMonth > 0:
            if self.indexMonth > 0:
                self.indexMonth -= 1
                self.setBaseDate(self.baseDate.addMonths(-1))
            else:
                self.indexMonth = 11
                self.setCurrentYear(currentYear-1)
                self.setBaseDate(self.baseDate.addMonths(-1))
                # print('new Year: ', self.currentYear)
        if currentMonth != self.indexMonth:
            self.currentPageChanged.emit(self.indexMonth)
            self.combo_mesi.setCurrentIndex(self.indexMonth)
        if currentYear != self.currentYear:
            self.setListaGiorniDellAnno(self.createDates(self.baseDate), self.indexMonth)

    def changeDisplayedMonthCombo(self, index):
        """changes the current month displayed in the combo"""
        self.combo_mesi.setCurrentIndex(index)

    def clickedCell(self, row, col) ->QDate:
        """if clicked returns the QDate setted into
        :return data"""
        data = self.table.cellWidget(row, col).data
        dataMonth = data.month() - 1
        dataYear = data.year()
        if data not in self.daysInTheMonth:
            if dataYear > self.currentYear:
                self.bot_next.click()
            elif dataYear < self.currentYear:
                self.bot_prev.click()
            elif dataMonth > self.indexMonth:
                self.bot_next.click()
            else:
                self.bot_prev.click()
        #todo presente per debug
        # self.yearShown()
        self.currentDate = data
        print('clicked ', data)
        return data


    def createDates(self, data: QDate=None):
        """create dict for dates in the selected Year, divided for row (6) and colums (7)
            """
        if data is None:
            data = self.oggi
        dateList = MeseGiorniDictGen.bigList(data)
        return dateList

    def formatHeaderNames(self):
        """set the header as days of the week"""
        listaNomiGiorniSettimana = ['Lun',
                                'Mar',
                                'Mer',
                                'Gio',
                                'Ven',
                                'Sab',
                                'Dom']

        for colonna, giorno in enumerate(listaNomiGiorniSettimana):
            item = QTableWidgetItem()
            item.setText(giorno)
            if colonna > 4:
                brush = QBrush(Qt.red)
                item.setForeground(brush)
            self.table.setHorizontalHeaderItem(colonna, item)

        # self.table.setHorizontalHeaderLabels(listaGiorniSettimana)

    def formatTable(self):
        """generic func for to format the table"""
        # self.table.horizontalHeader().setResizeMode(QHeaderView.ResizeToContents)
        self.populateWithComplexLabels()

        # self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setStyleSheet(self.headerStyleSheet)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.combo_mesi.setCurrentIndex(self.indexMonth)

    def getThisMonthDaysList(self) -> tuple:
        """find and returns the rows and columns into self.listaGiorniDellAnno as tuple"""
        # todo Obsoleta ---> cancellare
        for row in self.listaGiorniDellAnno:
            indexRow = self.listaGiorniDellAnno.index(row)
            for col in row:
                indexCol = self.listaGiorniDellAnno[indexRow].index(col)
                if self.baseDate in col:
                    pass
                    # return (indexRow, indexCol)
        else:
            print('CalendarTableWidget: getThisMonthDaysList: il giorno attuale non è presente nella lista dell\'anno')

    def monthShown(self):
        print('currentDate: ',self.currentDate)
        print('currentMonth: ',self.currentMonth)
        return self.currentMonth

    def populateWithComplexLabels(self):
        """populate the table with the complexlabels"""

        #ottengo la lista dei giorni di questo mese
        # indexTuple = self.getThisMonthDaysList()
        # listaDaInserire = self.listaGiorniDellAnno[indexTuple[0]]
        listaDaInserire = self.listaGiorniDellAnno[self.indexMonth]
        # setting righe e colonne
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        rows = self.table.rowCount()
        cols = self.table.columnCount()
        if rows != 6:
            self.table.setRowCount(6)
        if cols != 7:
            self.table.setColumnCount(7)
        for row in range(6):
            for col in range(7):
                itemWidget = ComplexLabel(self.table)
                self.table.setCellWidget(row, col, itemWidget)
        self.setTextComplexLabels(self.indexMonth)
        self.formatHeaderNames()

    def selectedDate(self) -> QDate:
        """:returns the date in the selected cell"""
        if self.sender() is not None:
            nome = self.sender().objectName()
            print('selectedDate sender ', None)

        # row = self.table.currentRow()
        # col = self.table.currentColumn()
        row = self.cellSelectedList[0].row()
        col = self.cellSelectedList[0].column()
        itemWidget = self.table.cellWidget(row, col)
        print('selectedDate data ', itemWidget.data)
        self.currentDate = itemWidget.data
        return itemWidget.data
        pass

    def selectCell(self, data=None):
        """ select the cell with the passed date setted into"""
        # print('clicked')
        # data = QDate().currentDate()
        # if data is None:
        #     data = self.oggi

        for row in range(6):
            for col in range(7):
                itemWidget = self.table.cellWidget(row, col)
                _data = itemWidget.data
                if data == _data:
                    self.table.setCurrentCell(row, col, QItemSelectionModel.Select)
                    self.cellSelectedList[0] = self.table.selectedIndexes()[0]
                    print('cell selected')
                    self.selectedDate()
                    #todo sto lavorando qui per selezionare automaticamente il giorno corrente
                    return

    def setAlphaColors(self, alpha=150):
        """set the alpha of the color background as the value for all the colors"""
        if self.colors is None:
            return
        for color in self.colors:
            color.setAlpha(alpha)

    def setBaseDate(self, date=None):
        """sets the base date to calculate the list for populating the current page"""
        if date is None:
            date = self.oggi
        print('setBaseDate ', date)
        self.baseDate = QDate(date.year(),date.month(),1)
        # print('setting baseDate', self.baseDate)
        if date.year() != self.currentYear:
            self.setCurrentYear(date.year())
            self.setListaGiorniDellAnno(self.createDates(date))

    def setCurrentMonth(self,month):
        self.currentMonth = month
        print('setcurrentMonth ',month)

    def setCurrentPage(self):
        """set the current page shown as month for the selected year"""
        pass

    def setCurrentYear(self,year):
        if self.sender() is not None:
            print('setCurrentYear sender ', self.sender().objectName())
        else: print('setCurrentYear sender ',self.sender())
        self.currentYear = year
        self.setLabelAnno(str(year))
        # self.yearChanged.emit()

    def setDates(self,prenotazioni, pulizie, colors):
        """mimic the old version of calendar"""
        # print('this func is obsolete, please change it as it does nothing')
        print('this func (setDates)  is going to be reimplemented, please be patient')
        #todo bisogna verificare che le date presenti nelle liste passate possano essere attivate
        # come la selezione delle date
        print('prenotazioni :',prenotazioni)
        print('pulizie :',pulizie)
        print('colori :', colors)

    def setIndexMonth(self,index):
        """change the index for self.listaGiorniDellAnno for the month to display"""
        self.indexMonth = index

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

    def setLabelAnno(self,anno):
        if self.sender() is not None:
            print(' setLabelAnno sender', self.sender().objectName())
        else: print(' setLabelAnno sender is None')
        print('anno: ',anno)
        self.label_anno.setText(f'Anno: {anno}')

    def setListaGiorniDellAnno(self, lista: list=None, index=None):
        if lista is not None:
            self.listaGiorniDellAnno = lista
            if index is not None:
                self.listaGiorniDellAnnoChanged.emit(index)

    def setSelectedDate(self, data):
        """set the date passed as the currentDate"""
        if self.sender() is not None:
            print('sender:',self.sender().objectName())
        print('setSelectedDate ', data)
        self.currentDate = data
        #todo selezionare la currentDate

    def setTextComplexLabels(self, indexMonth):
        """cambia il giorno nelle celle"""
        # indexTuple = self.getThisMonthDaysList()
        listaDaInserire = self.listaGiorniDellAnno[indexMonth]
        _data = QDate(self.baseDate.year(), indexMonth+1, 1)
        self.setBaseDate(_data)
        baseDate = self.baseDate
        print('setTextComplex baseDate', baseDate)
        self.daysInTheMonth = MeseGiorniDictGen.giorniDelMese(QDate(baseDate.year(), indexMonth+1, 1))
        self.currentMonth = indexMonth +1
        self.indexMonth = indexMonth
        # print('len(self.daysInTheMonth)', len(self.daysInTheMonth))
        # print('setTextComplexLabels',self.sender().objectName())
        # self.setBaseDate()
        dateEscluse = []
        for row in range(6):
            for col in range(7):
                data = listaDaInserire[row][col]
                itemWidget = self.table.cellWidget(row, col)
                numeroGiorno = str(data.day())
                itemWidget.setText(numeroGiorno)
                itemWidget.setData(data)
                if data not in self.daysInTheMonth:
                    itemWidget.setEnabled(False)
                    dateEscluse.append(data)
                else:
                    # print(data, ' in ', self.daysInTheMonth)
                    itemWidget.setEnabled(True)
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
        # todo selezionare la data di oggi e scrollare fino alla pagina corretta
        pass

    def signalsConnections(self):
        """provides connections to relative signals"""
        # self.yearChanged.connect()
        self.bot_next.clicked.connect(self.changeDisplayedMonth)
        self.bot_prev.clicked.connect(self.changeDisplayedMonth)
        self.currentPageChanged.connect(self.changeDisplayedMonthCombo)
        self.currentPageChanged.connect(self.setTextComplexLabels)
        self.currentPageChanged.connect(self.removeSelection)
        self.listaGiorniDellAnnoChanged.connect(self.setTextComplexLabels)
        self.combo_mesi.currentIndexChanged.connect(self.setTextComplexLabels)
        self.combo_mesi.currentIndexChanged.connect(self.removeSelection)
        self.table.cellClicked.connect(self.clickedCell)
        # self.table.doubleClicked.connect(lambda : print('double click needs to be forworded'))
        self.clicked.connect(self.clickedCell)

    def yearShown(self):
        """shows the year of the current date"""
        print('current date', self.currentDate)
        print('current year', self.currentYear)

        return self.currentYear

    def removeSelection(self):
        """removes the selection on the cell if the date is not the currentDate"""
        try:
            row = self.table.selectedIndexes()[0].row()
            col = self.table.selectedIndexes()[0].column()
        except IndexError:
            self.selectCell(self.currentDate)
            return
        data = self.currentDate
        _data = self.table.cellWidget(row, col).data
        if data != _data:
            self.table.setCurrentCell(row, col, QItemSelectionModel.Deselect)
        else:
            pass
            # print('data is the same', data)
            # self.selectCell(self.currentDate)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # dialog = QtWidgets.QMainWindow()
    dialog = QtWidgets.QWidget()
    # dialog.setFixedSize(QSize(800, 500))
    hbox = QtWidgets.QHBoxLayout()
    simpleWidget = CalendarTableWidget(dialog)
    # dialog.setCentralWidget(simpleWidget)
    hbox.addWidget(simpleWidget)
    dialog.setLayout(hbox)
    dialog.show()
    # bt = QPushButton('click')
    # bt.clicked.connect(simpleWidget.removeSelection)
    # bt.show()
    sys.exit(app.exec_())
