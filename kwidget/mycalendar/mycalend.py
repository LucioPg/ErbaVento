from PyQt5 import QtCore, QtWidgets, QtGui


class MyCalend(QtWidgets.QCalendarWidget):
    YEARCHANGED = QtCore.pyqtSignal(str)

    def __init__(
            # self, dateListAir:dict, dateListBooking, dateListPrivati, pulizieList, parent=None
            self, datePrenotazioni, pulizieList, colors: dict, parent=None
    ):
        super(MyCalend, self).__init__(parent)
        self.setGridVisible(True)
        self.setObjectName('Calendario')
        # self.color = QtGui.QColor(self.palette().color(QtGui.QPalette.Highlight))
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
            # for plat in self.datePrenotazioni['platforms']:
            #     if date in self.datePrenotazioni['platforms'][plat]['date']:
            #         # painter.fillRect(rect, QtGui.QColor(QtCore.Qt.cyan))
            #         colore = self.colors[plat]
            #         # if 'green' in colore.__dict__:
            #         print(colore)
            #         for attr, value in QtCore.Qt.__dict__.items():
            #             if attr != 'red':
            #                 if value == colore:
            #                     if QtGui.QColor(attr).isValid():
            #                         trueColor = QtCore.Qt.GlobalColor(value)
            #                         print('valido ', trueColor)
            #                         # trueColor = QtCore.Qt.red
            #                         break
            #                 # painter.fillRect(rect, QtGui.QColor(QtCore.Qt.red))
            #             else:
            #                 trueColor = QtCore.Qt.red
            #
            #         # painter.fillRect(rect, QtGui.QColor(self.colors[plat]))
            #         painter.fillRect(rect, trueColor)
            #         # print('colore: ', self.datePrenotazioni['platforms'][plat]['colore'].name())
            #
            #     if date in self.pulizieList:
            #         painter.drawRect(rect.adjusted(0, 0, -1, -1))
            if date in self.listeDate:
                plat = self.listeDate[date]
                colore = self.colors[plat]
                painter.fillRect(rect, QtGui.QColor(colore))
            if date in self.pulizieList:
                painter.drawRect(rect.adjusted(0, 0, -1, -1))

        except:
            # print(self.colors[plat])
            import traceback
            print(traceback.format_exc())
        #         painter.drawRect(rect.adjusted(0, 0, -1, -1))
        # for giorno in self.datePrenotazioni['platforms'][plat].value():
        #     if date in :
        #         painter.fillRect(rect, self.listeColori[plat])
        #     if date in self.pulizieList:
        #         painter.drawRect(rect.adjusted(0, 0, -1, -1))

        # if date in self.dateList_booking:
        #     painter.fillRect(rect, self.booking)
        # elif date in self.dateList_air:
        #     painter.fillRect(rect, self.airbb)
        # elif date in self.dateList_privati:
        #     painter.fillRect(rect, self.privato)


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
