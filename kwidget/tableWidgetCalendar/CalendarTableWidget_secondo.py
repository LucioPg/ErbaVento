from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import (QTableWidget, QComboBox, QPushButton, QWidget, QTableWidgetItem, QMainWindow,
                             QHeaderView, QAbstractItemView)
from PyQt5.QtCore import (QDate, pyqtSignal, pyqtSlot, Qt, QSize, QRect, QModelIndex, QItemSelectionModel)
from PyQt5.QtGui import (QPen, QBrush, QPainter, QColor, QIcon)
from kwidget.tableWidgetCalendar.gui_calendar import Ui_CalendarTableWid as Calendar
from kwidget.complexlabel.complexLabels import ComplexLabel
from tools.meseGiorniDictGen import MeseGiorniDictGen
from copy import deepcopy as deepc
import sys

# todo la selezione della cella deve essere connessa alla data e non alla posizione della cella, di conseguenza cambiando
# todo pagina al calendario la data selezionata deve rimanere la stessa
# TODO SISTEMARE IL SEGNALE selectionChanged

class CalendarTableWidget(Calendar, QWidget):
    #Signals:
    currentPageChanged = pyqtSignal(int) #indice per il mese
    datesIndicatorsChanged = pyqtSignal()
    listaGiorniDellAnnoChanged = pyqtSignal(int)
    selectionChanged = pyqtSignal(QDate)
    singleClicked = pyqtSignal(QDate)
    yearChanged = pyqtSignal() #anno corrente
    headerStyleSheet = "QHeaderView::section { background-color:gray; font-size:20px; border:0px;}"
    def __init__(self, parent=None, spese=None):
        super(CalendarTableWidget, self).__init__(parent)
        self.setupUi(self)
        self.cellSelectedList = [None]
        self.datePrenotazioni = {}
        self.datePulizie = []
        self.colors = []
        self.dateSpese = []
        # self.dateSpese = {}
        self.dateNote = []
        # self.setAlphaColors()
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
        # print('selectCEll from init')
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
                # print('baseDate before', self.baseDate)
                self.setBaseDate(self.baseDate.addMonths(1))
                # print('baseDate after', self.baseDate)
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
            # print(f'currentPageChanged.emit({self.indexMonth})')
            self.currentPageChanged.emit(self.indexMonth)
            self.combo_mesi.setCurrentIndex(self.indexMonth)
        if currentYear != self.currentYear:
            # print('current year changed')
            self.setListaGiorniDellAnno(self.createDates(self.baseDate), self.indexMonth)

    def changeDisplayedMonthCombo(self, index):
        """changes the current month displayed in the combo"""
        self.combo_mesi.setCurrentIndex(index)

    def clickedCell(self, row, col) ->QDate:
        """if clicked returns the QDate setted into
        :return data"""
        itemWidget = self.table.cellWidget(row, col)
        data = itemWidget.data
        dataMonth = data.month() - 1
        dataYear = data.year()
        self.currentDate = data
        # print('cell clicked flags: ', itemWidget.dictFlags)
        # print('cell clicked flags currentDate: ', data)
        # print('cell clicked flags item date: ', itemWidget.data)
        if data not in self.daysInTheMonth:
            if dataYear > self.currentYear:
                self.bot_next.click()
            elif dataYear < self.currentYear:
                self.bot_prev.click()
            elif dataMonth > self.indexMonth:
                self.bot_next.click()
            else:
                self.bot_prev.click()
        self.singleClicked.emit(data)
        return data

    def createDates(self, data: QDate=None):
        """create dict for dates in the selected Year, divided for row (6) and colums (7)
            """
        if data is None:
            data = self.oggi
        # print('CREATEDATES DATA', data)
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

    def forwardData(self,data):
        self._dataToSet = data
        return self._dataToSet

    def findItemWidgetFromDate(self, data):
        """return the itemWidget from the passed data"""
        for row in range(6):
            for col in range(7):
                itemWidget = self.table.cellWidget(row, col)
                _data = itemWidget.data
                if data == _data:
                    return itemWidget

    def formatTable(self):
        """generic func for to format the table"""
        # self.table.horizontalHeader().setResizeMode(QHeaderView.ResizeToContents)
        self.populateWithComplexLabels()

        # self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setStyleSheet(self.headerStyleSheet)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.combo_mesi.setCurrentIndex(self.indexMonth)

    def monthShown(self):
        return self.currentMonth

    def populateWithComplexLabels(self):
        """populate the table with the complexlabels"""
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
        self.setComplexLabels(self.indexMonth)
        self.formatHeaderNames()

    def reformatColor(self, colorStr):
        """return hex color in decimal format"""
        if type(colorStr) is str:
            if colorStr.startswith('#'):
                colorStr = colorStr.replace('#', '')
            else:
                raise Exception('color is not hex format')
            r = int(colorStr[:2], 16)
            g = int(colorStr[2:4], 16)
            b = int(colorStr[4:6], 16)
            return r, g, b

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

    def selectedDate(self) -> QDate:
        """:returns the date in the selected cell"""
        row = self.cellSelectedList[0].row()
        col = self.cellSelectedList[0].column()
        itemWidget = self.table.cellWidget(row, col)
        # print('selectedDate data ', itemWidget.data)
        self.currentDate = itemWidget.data
        return itemWidget.data

    def selectCell(self, data=None):
        """ select the cell with the passed date setted into"""
        for row in range(6):
            for col in range(7):
                itemWidget = self.table.cellWidget(row, col)
                _data = itemWidget.data
                if data == _data:
                    self.table.setCurrentCell(row, col, QItemSelectionModel.Select)
                    self.cellSelectedList[0] = self.table.selectedIndexes()[0]
                    # print('cell selected', itemWidget.dictFlags)
                    self.selectedDate()
                    return

    def setAlphaColors(self, color, alpha=150):
        """set the alpha of the color background as the value for all the colors"""
        color.setAlpha(alpha)

    def setBaseDate(self, date=None):
        """sets the base date to calculate the list for populating the current page"""
        if date is None:
            date = self.oggi
        self.baseDate = QDate(date.year(), date.month(), 1)

    def setBooked(self, data, itemWidget):
        """"changes the background for the date passed"""
        # itemWidget = self.findItemWidgetFromDate(data)
        styleSheet = ""
        # try:
        # for giorno in self.datePrenotazioni.keys():
        if data in self.datePrenotazioni:
            color = self.colors[self.datePrenotazioni[data]]
            r, g, b = self.reformatColor(color)
            styleSheet = f"background-color: rgba({r},{g},{b},150)"

        # for plat in self.datePrenotazioni['platforms'].keys():
        #         if data in self.datePrenotazioni['platforms'][plat]['date']:
        #             color = self.colors[plat]
        #             r, g, b = self.reformatColor(color)
        #             styleSheet = f"background-color: rgba({r},{g},{b},150)"
        #             break
        # except KeyError:
        #     print('remove try/exc')
        # print('setbooked ' + styleSheet)
        itemWidget.lab_num.setStyleSheet(styleSheet)

    def setComplexLabels(self, indexMonth):
        """cambia il giorno nelle celle"""
        listaDaInserire = self.listaGiorniDellAnno[indexMonth]
        _data = QDate(self.baseDate.year(), indexMonth+1, 1)
        self.setBaseDate(_data)
        baseDate = self.baseDate
        self.daysInTheMonth = MeseGiorniDictGen.giorniDelMese(QDate(baseDate.year(), indexMonth + 1, 1))
        self.currentMonth = indexMonth + 1
        self.indexMonth = indexMonth
        dateEscluse = []
        for row in range(6):
            for col in range(7):
                data = listaDaInserire[row][col]
                itemWidget = self.table.cellWidget(row, col)
                numeroGiorno = str(data.day())
                itemWidget.setText(numeroGiorno)
                itemWidget.setData(data)
                # self.setIconsAndBooked(data, itemWidget)
                if data not in self.daysInTheMonth:
                    itemWidget.setEnabled(False)
                    dateEscluse.append(data)
                else:
                    itemWidget.setEnabled(True)

    def setCurrentMonth(self,month):
        self.currentMonth = month
        # print('setcurrentMonth ', month)

    def setCurrentPage(self):
        """set the current page shown as month for the selected year"""
        pass

    def setCurrentYear(self, year):
        self.currentYear = year
        self.setLabelAnno(str(year))

    def setDatesIndicators(self, prenotazioni, pulizie, colors, spese, note):
        """sets the object datePrenotazioni, datePulizie and colors"""
        if len(colors) != 0:
            self.colors = colors
        self.datePrenotazioni = deepc(prenotazioni)
        # if len(prenotazioni) != 0:
        #     self.datePrenotazioni = deepc(prenotazioni)
            # print('prenotazioni setted')
        if len(pulizie) != 0:
            self.datePulizie = pulizie
            # print('pulizie setted')
        if len(spese) > 0:
            # print('spese setted ')
            self.dateSpese = spese
            # self.dateSpese = deepc(spese)
            # print('spese setted ')
        if len(note) > 0:
            # print('note setted')
            self.dateNote = list(set(note))
        self.datesIndicatorsChanged.emit()

    def setIconsAndBooked(self, data=None):
        """provides icons for the displayed page ( not current month) """
        # itemWidget = self.findItemWidgetFromDate(data)
        # print('setIconsAndBooked')
        data = self._dataToSet
        # print('data to set iconsAndBooked', data)
        itemWidget = self.findItemWidgetFromDate(data)
        self.setIconNote(data, itemWidget)
        self.setIconPulizie(data, itemWidget)
        self.setIconSpese(data, itemWidget)
        self.setBooked(data, itemWidget)

    def setIconPulizie(self, data, itemWidget):
        """sets the pulizie icon if a displayed month has a date in self.datePulizie list"""
        # itemWidget = self.findItemWidgetFromDate(data)
        # print('data passed', data)
        # print('datePulizie', self.datePulizie)
        # print('setting icon pulizie: ',itemWidget.dictFlags['pulizie'])
        # itemWidget = self.findItemWidgetFromDate(data)
        if data in self.datePulizie:
            itemWidget.dictFlags['pulizie'] = 1
        else:
            itemWidget.dictFlags['pulizie'] = 0
        itemWidget.setActive()

    def setIconSpese(self, data, itemWidget):
        """ sets the spese icon """
        if not len(self.dateSpese):
            itemWidget.dictFlags['spese'] = 0
        else:
        # itemWidget = self.findItemWidgetFromDate(data)
            if data in self.dateSpese:
                if data == itemWidget.data:
                    itemWidget.dictFlags['spese'] = 1
                else:
                    itemWidget.dictFlags['spese'] = 0
                    # print('dateSpese',self.dateSpese)
            else:
                itemWidget.dictFlags['spese'] = 0
        itemWidget.setActive()

    def setIconNote(self, data, itemWidget):
        """ sets the note icon """
        if data in self.dateNote:
            itemWidget.dictFlags['note'] = 1
        else:
            itemWidget.dictFlags['note'] = 0
        itemWidget.setActive()

    def setIndexMonth(self,index):
        """change the index for self.listaGiorniDellAnno for the month to display"""
        self.indexMonth = index

    def setLabelAnno(self,anno):
        """ sets text into the label for the year above the widget"""
        self.label_anno.setText(f'Anno: {anno}')

    def setListaGiorniDellAnno(self, lista: list=None, index=None):
        """ sets the list for the 12 months of the current year with all the days that belong to"""
        if lista is not None:
            self.listaGiorniDellAnno = lista
            if index is not None:
                self.listaGiorniDellAnnoChanged.emit(index)

    def setSelectedDate(self, data):
        """set the date passed as the currentDate"""
        # print('setSelectedDate ', data)
        self.currentDate = data

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

    def signalsConnections(self):
        """provides connections to relative signals"""
        # self.yearChanged.connect()
        self.bot_next.clicked.connect(self.changeDisplayedMonth)
        self.bot_prev.clicked.connect(self.changeDisplayedMonth)
        self.currentPageChanged.connect(self.changeDisplayedMonthCombo)
        self.currentPageChanged.connect(self.setComplexLabels)
        self.currentPageChanged.connect(self.removeSelection)
        self.currentPageChanged.connect(self.updateIconsAndBooked)
        self.listaGiorniDellAnnoChanged.connect(self.setComplexLabels)
        self.listaGiorniDellAnnoChanged.connect(self.updateIconsAndBooked)
        self.combo_mesi.currentIndexChanged.connect(self.setComplexLabels)
        self.combo_mesi.currentIndexChanged.connect(self.removeSelection)
        self.table.cellClicked.connect(self.clickedCell)
        self.datesIndicatorsChanged.connect(self.updateIconsAndBooked)

    def updateIconsAndBooked(self):
        for row in range(6):
            for col in range(7):
                itemWidget = self.table.cellWidget(row, col)
                data = itemWidget.data
                self.forwardData(data)
                self.setIconsAndBooked(data=None)

    def yearShown(self):
        """shows the year of the current date"""
        return self.currentYear


if __name__ == '__main__':
    import pickle


    # with open('C:\\Users\\Lucio\\PycharmProjects\\ErbaVento\\speseDb.pkl', 'rb') as f:
    #     spese = pickle.load(f)
    app = QtWidgets.QApplication(sys.argv)
    # dialog = QtWidgets.QMainWindow()
    dialog = QtWidgets.QWidget()
    # dialog.setFixedSize(QSize(800, 500))
    hbox = QtWidgets.QHBoxLayout()
    # simpleWidget = CalendarTableWidget(dialog, spese=spese)
    simpleWidget = CalendarTableWidget(dialog)
    # dialog.setCentralWidget(simpleWidget)
    hbox.addWidget(simpleWidget)
    dialog.setLayout(hbox)

    simpleWidget.setDatesIndicators({}, [QtCore.QDate(2019, 11, 30)], [], {}, [])
    # simpleWidget.dateSpese = spese
    dialog.show()
    # bt = QPushButton('click')
    # bt.clicked.connect(simpleWidget.removeSelection)
    # bt.clicked.connect(lambda :print(len(dir(simpleWidget))))
    # bt.show()
    sys.exit(app.exec_())
