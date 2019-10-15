from PyQt5 import QtCore, QtWidgets, QtGui


class MyCalend(QtWidgets.QCalendarWidget):
    YEARCHANGED = QtCore.pyqtSignal(str)

    def __init__(
            self, dateListAir, dateListBooking, dateListPrivati, pulizieList, parent=None
    ):
        super(MyCalend, self).__init__(parent)
        self.setGridVisible(True)
        self.setObjectName('Calendario')
        # self.color = QtGui.QColor(self.palette().color(QtGui.QPalette.Highlight))
        self.booking = QtGui.QColor(QtCore.Qt.cyan)
        self.privato = QtGui.QColor(QtCore.Qt.darkRed)
        self.airbb = QtGui.QColor(QtCore.Qt.darkGreen)
        self.pulizie = QtGui.QColor(QtCore.Qt.magenta)
        self.colors = [self.booking, self.privato, self.airbb]
        for color in self.colors:
            color.setAlpha(150)
        # self.selectionChanged.connect(self.updateCells)
        self.dateList_booking = dateListBooking
        self.dateList_air = dateListAir
        self.dateList_privati = dateListPrivati
        self.pulizieList = pulizieList
        # self.dateList = [QtCore.QDate(2019, 8, 13)]
        self.rightDate = None
        print("current: ", self.selectedDate())
        self.pen = QtGui.QPen()
        self.pen.setColor(self.pulizie)

    # def showPreviousMonth(self) -> None:
    #     pass
    # def showNextMonth(self) -> None:
    #     pass
    def paintCell(self, painter, rect, date):
        # calling original paintCell to draw the actual calendar
        QtWidgets.QCalendarWidget.paintCell(self, painter, rect, date)
        painter.setPen(self.pen)

        # highlight a particular date
        if date in self.dateList_booking:
            painter.fillRect(rect, self.booking)
        elif date in self.dateList_air:
            painter.fillRect(rect, self.airbb)
        elif date in self.dateList_privati:
            painter.fillRect(rect, self.privato)
        if date in self.pulizieList:
            painter.drawRect(rect.adjusted(0, 0, -1, -1))

    def setDateBooking(self, qdatesList):
        self.dateList_booking = qdatesList
        # this redraws the calendar with your updated date list
        # self.updateCells()

    def setDateAir(self, qdatelist):
        self.dateList_air = qdatelist
        # self.updateCells()

    def setDatePrivati(self, qdatelist):
        self.dateList_privati = qdatelist
        # self.updateCells()

    def setDatePulizie(self, pl):
        self.pulizieList = pl
        # self.updateCells()

    def setDates(self, booking, air, privati, pulizie):
        self.setDateBooking(booking)
        self.setDateAir(air)
        self.setDatePrivati(privati)
        self.setDatePulizie(pulizie)
        self.updateCells()
