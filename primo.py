from copy import deepcopy as deepc
from PyQt5 import QtGui, QtCore, QtWidgets
from gui import Ui_MainWindow as mainwindow
from tools.databaseMaker import DbMaker as dbm
from tools.managerprenotazioni import ManagerPreno as Manager
from collections import OrderedDict as Od
import sys


class EvInterface(mainwindow, QtWidgets.QMainWindow):
    """Classe per la creazione gui del gestionale per case vacanze"""

    def __init__(self, parent=None):
        super(EvInterface, self).__init__(parent)

        self.dateBooking = []
        self.dateAirbb = []
        self.datePrivati = []
        self.datePulizie = []
        d = {
            "nome": "",
            "cognome": "",
            "telefono": None,
            "platform": "",
            "data arrivo": None,
            "data partenza": None,
            "numero ospiti": 1,
            "bambini": 0,
            "spese": {},
            "colazione": False,
            "importo": 0,
            "lordo": 0,
            "tasse": 0,
            "netto": 0,
            "note": "",
        }
        self.infoModel = Od(d)
        self.infoTemp = Od(d)
        r = {"nome": "", "cognome": "", "data partenza": ""}
        self.infoModelRedux = Od(r)
        #  init gui
        self.setupUi(self)
        self.statusbar.showMessage("Ready!!!!")
        self.initDatabase()
        self.calendario = MyCalend(
            self.dateAirbb,
            self.dateBooking,
            self.datePrivati,
            self.datePulizie,
            parent=self.frame_calendar,
        )
        cal_layout = QtWidgets.QGridLayout(self.frame_calendar)
        cal_layout.addWidget(self.calendario)
        self.frame_calendar.setLayout(cal_layout)

        self.calendario.clicked.connect(self.getInfoFromCalendar)
        self.calendario.selectionChanged.connect(self.setDateEdit_dal)
        self.tabWidget.currentChanged.connect(self.pulisci_campi_prenotazioni)
        # self.calendario.currentPageChanged.connect(self.riportapagina)
        self.lastMonth = None
        self.current_date = None
        self.giornoCorrente = self.calendario.selectedDate()
        self.setDateEdit_dal()

        self.dateEdit_dal.dateChanged.connect(self.correggiPartenza)
        self.bot_salva.clicked.connect(self.salvaInfo)
        self.bot_checkDisp.clicked.connect(self.botFuncCheckAval)
        self.bot_cancella.clicked.connect(self.cancellaprenot)

        # STATUS BAR
        # self.statusbar.setT

    def pulisci_campi_prenotazioni(self):
        """ prende le info da inserire nei campi
            della prenotazione a partire dalle info
            nel box nella pagina
            del calendario"""
        _nome = self.tableWidget_info_ospite.item(0, 0)
        if _nome is not None:
            nome = _nome.text()
        else:
            nome = None
        print(nome)
        pass

    def set_status_msg(self, st=""):
        self.statusbar.showMessage(st)
        return

    # def riportapagina(self, a, m):
    #     """fa in modo che non cambi la pagina
    #         se viene selzionato un giorno di un altro mese"""
    #     print("riporta la pagina ", self.calendario.selectedDate())

    def cancellaprenot(self):
        """cancella la prenotazione nella data
            selezionata nel calendario"""

        manager = Manager(info=self.infoTemp)
        manager.canc()
        self.leggiDatabase(manager.DataBase)
        self.calendario.updateCells()
        # data = self.current_date
        # print("giorno selezionato: ", data)
        # domani = data.addDays(1)
        # print("domani: ", domani)
        # print("giorno selezionato_after: ", data)
        # a, m, g = self.dataParser(data)
        # ad, md, gd = self.dataParser(domani)
        # info = self.getInfo(a, m, g)
        #
        # try:
        #     # print(info)
        #     if info["data arrivo"] is None:
        #         print("nessuna prenotazione presente")
        #     else:
        #         print("prenotazione in lista di cancellazione")
        #         Dtbm = dbm(data)
        #         dtb = self.getDatabase(a)
        #         dtb[a][m][g]["checkIn"] = self.infoModel.copy()
        #         print("checkOut", dtb[a][m][g]["checkOut"])
        #         dtb[ad][md][gd]["checkOut"] = self.infoModelRedux.copy()
        #         self.leggiDatabase(dtb)
        #         self.calendario.updateCells()
        #         Dtbm.salvaDatabase(a, dtb)
        #         self.set_status_msg("Cancellazione eseguita con successo")
        #
        # except BaseException:
        #     self.set_status_msg("Cancellazione non eseguita")
        #     print("non individuato")
        pass

    def correggiPartenza(self, d):
        """
        adegua la spinbox della partenza a quella dell'arrivo
        considerando almeno un giorno
        :param d:
        :return:
        """
        al = self.dateEdit_al.date()
        md = self.dateEdit_al.minimumDate()

        if al <= d:
            al = d.addDays(1)
            self.dateEdit_al.setDate(al)
            self.dateEdit_al.setMinimumDate(d.addDays(1))
            print("correzione in avanti effettuata")
        else:
            print("partenza ok")
        if md >= d:
            self.dateEdit_al.setMinimumDate(d.addDays(1))

    def getInfo(self, a, m, g):
        try:
            database = self.getDatabase(a)
            info = database[a][m][g]["checkIn"]
        except KeyError:
            print(database[2019][10])
            info = None
        return info

    def setInfoFromDate(self, info):
        nome = info["nome"]
        cognome = info["cognome"]
        telefono = info["telefono"]
        platform = info["platform"]
        ospiti = info["numero ospiti"]
        bambini = info["bambini"]
        checkIn = info["data arrivo"]
        if type(checkIn) is QtCore.QDate:
            checkIn = info["data arrivo"].toString("ddd dd/MM/yyyy")
        checkOut = info["data partenza"]
        if type(checkOut) is QtCore.QDate:
            checkOut = info["data partenza"].toString("ddd dd/MM/yyyy")
        item = QtWidgets.QTableWidgetItem(nome)
        self.tableWidget_info_ospite.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem(cognome)
        self.tableWidget_info_ospite.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem(ospiti)
        self.tableWidget_info_ospite.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem(bambini)
        self.tableWidget_info_ospite.setItem(3, 0, item)
        if platform == "privato":
            item = QtWidgets.QTableWidgetItem("Si")
        else:
            item = QtWidgets.QTableWidgetItem("No")
        self.tableWidget_info_ospite.setItem(4, 0, item)
        item = QtWidgets.QTableWidgetItem(checkIn)
        self.tableWidget_info_ospite.setItem(5, 0, item)
        item = QtWidgets.QTableWidgetItem(checkOut)
        self.tableWidget_info_ospite.setItem(5, 1, item)

        self.tableWidget_info_ospite.update()

    def getInfoFromDate(self, data):
        self.get_date(data)
        a, m, g = self.amg(data)
        info = self.getInfo(a, m, g)
        return info

    def getInfoFromCalendar(self, data):

        info = self.getInfoFromDate(data)
        self.setInfoFromDate(info)
        self.setInfoTemp(info)
        return info

    def setInfoTemp(self, info, data=None):
        self.infoTemp = deepc(info)
        return self.infoTemp

    def get_date(self, d):
        # a = self.calendarWidget.dateTextFormat()
        # self.calendario.set
        self.current_date_label = d.toString("ddd dd/MM/yyyy")
        self.current_date = d
        if self.lastMonth != self.current_date.month():
            self.lastMonth = self.current_date.month()
        # print(d.month(),'<<<<',self.calendario.month())
        print("selection changed", self.current_date_label)
        self.label_data.setText(self.current_date_label)
        return self.current_date

    def setDateEdit_dal(self):

        d = self.calendario.selectedDate()
        a = d.addDays(1)
        self.setInfoTemp(self.getInfoFromDate(d))
        if self.infoTemp['note'] != '':
            print(self.infoTemp['note'])
        # print("infoTemp:\n")
        # for k,v in self.infoTemp.items():
        #     print(k,v,end='\t\t')
        #     print('\n')
        # todo rimuovere il commento a:
        # self.dateEdit_dal.setMinimumDate(self.giornoCorrente)
        # self.dateEdit_al.setMinimumDate(self.giornoCorrente.addDays(1))
        self.dateEdit_al.setMinimumDate(a)
        self.dateEdit_dal.setDate(d)
        self.dateEdit_al.setDate(a)

    # def setDateEdit_al(self,a):
    #     d = a.addDays(1)
    #     self.dateEdit_al.setDate(a)

        # db.stampa()

    def compilaInfo(self):
        a = self.infoModel.copy()
        a["nome"] = self.lineEdit_nome.text()
        a["cognome"] = self.lineEdit_cognome.text()
        a["telefono"] = self.lineEdit_telefono.text()
        if self.radio_air.isChecked():
            a["platform"] = "airBB"
        elif self.radio_booking.isChecked():
            a["platform"] = "Booking.com"
        elif self.radio_privato.isChecked():
            a["platform"] = "privato"
        else:
            a["platform"] = "sconosciuta"
        # a["data arrivo"] = self.dateEdit_dal.date().toString("dd MMM yyyy")
        a["data arrivo"] = self.dateEdit_dal.date()
        # a["data partenza"] = self.dateEdit_al.date().toString("dd MMM yyyy")
        a["data partenza"] = self.dateEdit_al.date()
        a["numero ospiti"] = self.spinBox_ospiti.text()
        a["bambini"] = self.spinBox_bambini.text()
        a["spese"] = self.addSpese()
        if self.radio_colazione.isChecked():
            a["colazione"] = True
        else:
            a["colazione"] = False
        a["importo"] = self.spinBox_importo.text()
        a["lordo"] = self.lineEdit_lordo.text()
        a["netto"] = self.lineEdit_netto.text()
        a["tasse"] = self.lineEdit_tax.text()
        a["note"] = self.plainTextEdit_note.toPlainText()
        # print(a)
        return a

    def salvaInfo(self):
        # if mode is None:
        info = self.compilaInfo()
        dal = info['data arrivo']
        al = info['data partenza']
        anno = dal.year()
        giorniPermanenza = dal.daysTo(al)
        print("(salvaInfo NUOVA) anno: ", anno)
        manager = Manager(info)
        listaDisponibili = manager.checkAval(dal, al)
        if len(listaDisponibili) == giorniPermanenza:
            manager.setThem()
            print("prenotazione effettuata per tutte le date richieste")
            self.leggiDatabase(manager.DataBase)
            self.calendario.setDates(
                booking=self.dateBooking,
                air=self.dateAirbb,
                privati=self.datePrivati,
                pulizie=self.datePulizie,
            )
            self.set_status_msg("Prenotazione eseguita con successo")
            l = [self.lineEdit_nome, self.lineEdit_cognome, self.lineEdit_lordo,
                 self.lineEdit_netto, self.lineEdit_tax, self.lineEdit_telefono,
                 self.plainTextEdit_note]
            for w in l:
                w.clear()
            self.spinBox_ospiti.setValue(1)
            self.spinBox_bambini.setValue(0)
            self.tabWidget.setCurrentIndex(0)
        else:
            self.set_status_msg("Le date selezionate sono occupate")
            print("date non disponibili")

    def initDatabase(self, anno=None):
        # anno = self.calendario.yearShown()
        if anno is None:
            anno = QtCore.QDate().currentDate().year()
        database = self.getDatabase(anno)
        self.leggiDatabase(database)
        print("initDatabase ", anno)

    def getDatabase(self, anno):
        Dbm = dbm(self.dateEdit_dal.date())
        database = Dbm.checkFile(anno)

        return database

    def leggiDatabase(self, database):

        self.dateBooking.clear()
        self.dateAirbb.clear()
        self.datePrivati.clear()
        self.datePulizie.clear()
        db = Manager()
        self.dateBooking, self.dateAirbb, self.datePrivati, self.datePulizie = db.platformPulizie()

    def dataParser(self, data):
        anno = data.toString("yyyy")
        mese = data.toString("MMM")
        giorno = int(data.toString("dd"))
        return anno, mese, giorno

    def amg(self, data=QtCore.QDate):
        """
        anno mese giorno
        :param data: QtCore.QDate
        :return: a,m,g
        """
        a = data.year()
        m = data.month()
        g = data.day()

        return a, m, g

    def botFuncCheckAval(self):
        dal = self.dateEdit_dal.date()
        al = self.dateEdit_al.date()
        print(self.checkAval(dal, al))
        # if self.checkAval(dal,al):
        #     print("check ok")

    def checkAval(self, dal, al):
        # arrivo =  self.dateEdit_dal.date()
        # partenza = self.dateEdit_al.date()
        giorniPermanenza = dal.daysTo(al)
        print("giorni di permanenza: ", giorniPermanenza)
        arrivo = dal
        partenza = al
        arrivo_a, arrivo_m, arrivo_g = self.amg(arrivo)
        partenza_a, partenza_m, partenza_g = self.amg(partenza)
        database = None
        database_partenza = None
        aval = True
        listaDisponibili = []
        if arrivo_a == partenza_a:
            data = dal
            for i in range(1, giorniPermanenza + 1):
                # if aval:
                # a, m, g = self.dataParser(data)
                a, m, g = self.amg(data)
                database = self.getDatabase(a)
                info = database[a][m][g]["checkIn"].copy()
                if info["nome"] != "" or info["cognome"] != "":
                    finoAl = info["data partenza"]
                    if finoAl == data or finoAl is None:
                        listaDisponibili.append(data.toString("dd MMM yyyy"))
                        aval = True
                        data = data.addDays(1)
                    else:
                        nome = info["nome"]
                        cognome = info["cognome"]
                        # print("type data", type(data))
                        print(
                            "spiacente, casa non disponibile in questa data",
                            data.toString("dd MMM yyyy"),
                        )
                        print(nome, "\t", cognome, "\n", "fino al: ", finoAl)
                        aval = False
                else:
                    listaDisponibili.append(data)
                    aval = True
                data = data.addDays(1)
        # else:
        #     database = self.getDatabase(arrivo_a)
        #     database_partenza = self.getDatabase(partenza_a)
        #     print("inutile else checck aval")
        # if aval:
        if giorniPermanenza == len(listaDisponibili):
            print("casa libera  tutti i giorni disponibili")
        else:
            print(" casa libera nei giorni:\n")
            if len(listaDisponibili) > 0:
                self.dateEdit_dal.setDate(listaDisponibili[0])
                self.dateEdit_dal.update()
                for d in listaDisponibili:
                    print(d)

        return listaDisponibili

    def addSpese(self):
        return


class MyCalend(QtWidgets.QCalendarWidget):
    YEARCHANGED = QtCore.pyqtSignal(str)

    def __init__(
            self, dateListAir, dateListBooking, dateListPrivati, pulizieList, parent=None
    ):
        super(MyCalend, self).__init__(parent)
        self.setGridVisible(True)

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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = EvInterface()
    ui.show()
    sys.exit(app.exec_())
