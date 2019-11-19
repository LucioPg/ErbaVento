from PyQt5 import QtCore, QtWidgets, QtGui

images_dir = QtCore.QFileInfo(__file__).absolutePath() + '/images'
class MyCalend(QtWidgets.QCalendarWidget):
    YEARCHANGED = QtCore.pyqtSignal(str)

    def __init__(
            # self, dateListAir:dict, dateListBooking, dateListPrivati, pulizieList, parent=None
            self, datePrenotazioni, pulizieList, colors: dict, parent=None
    ):
        super(MyCalend, self).__init__(parent)
        self.setGridVisible(True)
        self.setObjectName('Calendario')
        self.setVerticalHeaderFormat(0)
        self.datePrenotazioni = datePrenotazioni
        # self.listeColori = {p:col for p,col in zip(self.datePrenotazioni.keys(), )}
        # self.booking = QtGui.QColor(QtCore.Qt.cyan)
        # self.privato = QtGui.QColor(QtCore.Qt.darkRed)
        # self.airbb = QtGui.QColor(QtCore.Qt.darkGreen)
        self.pulizie = QtGui.QColor(QtCore.Qt.magenta)
        self.colors = colors
        self.listeDate = {}
        for color in self.colors:
            color.setAlpha(150)
        # self.selectionChanged.connect(self.updateCells)
        # self.dateList_booking = dateListBooking
        # self.dateList_air = dateListAir
        # self.dateList_privati = dateListPrivati
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

    def setListe(self, fe):
        listaDate = {}
        for i in fe.keys():
            for l in fe[i].keys():
                for data in fe[i][l]['date']:
                    if data not in listaDate:
                        listaDate[data] = l
        return listaDate


    def paintCell(self, painter, rect, date):
        # calling original paintCell to draw the actual calendar
        QtWidgets.QCalendarWidget.paintCell(self, painter, rect, date)
        painter.setPen(self.pen)
        #                                       self.datePrenotazioni['platforms'][plat]['date']
        # highlight a particular date
        platKeys = [k for k in self.datePrenotazioni['platforms']]
        try:
            if date in self.listeDate:
                plat = self.listeDate[date]
                colore = QtGui.QColor(self.colors[plat])
                colore.setAlpha(150)
                painter.fillRect(rect, colore)
            if date in self.pulizieList:
                painter.drawRect(rect.adjusted(0, 0, -1, -1))

        except:
            # print(self.colors[plat])
            import traceback
            print(traceback.format_exc())

    def setDatePulizie(self, pl):
        self.pulizieList = pl
        # self.updateCells()

    def setColors(self, colorText):
        def insider(func, val):
            return QtCore.Qt.func(val)

        for attr, value in QtCore.Qt.__dict__.items():
            if colorText == attr:
                return QtCore.Qt.__dict__[attr]

    def setDates(self, prenotazioni, pulizie, colors: dict):
        # for plat, color in colors.items():
        #     self.colors[plat] = self.setColors(color)
        self.colors = colors
        self.datePrenotazioni = prenotazioni
        self.listeDate = self.setListe(prenotazioni)
        self.setDatePulizie(pulizie)
        self.updateCells()


class Model(QtCore.QAbstractItemModel):
    def __init__(self, rows, columns, parent=None):
        super(Model, self).__init__(parent)
        self.services = QtGui.QIcon(images_dir + '/services.png')
