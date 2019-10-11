from copy import deepcopy as deepc
from PyQt5 import QtGui, QtCore, QtWidgets
from gui import Ui_MainWindow as mainwindow
from tools.databaseMaker import DbMaker as dbm
from tools.managerprenotazioni import ManagerPreno as Manager
from collections import OrderedDict as Od
from traceback import format_exc as fex

import sys


class EvInterface(mainwindow, QtWidgets.QMainWindow):
    """Classe per la creazione gui del gestionale per case vacanze"""
    MAXOSPITI = 5
    def __init__(self, parent=None):
        super(EvInterface, self).__init__(parent)


        self.dateBooking = []
        self.dateAirbb = []
        self.datePrivati = []
        self.datePulizie = []
        self.listeImporti = {'Booking.com': [72, 74, 92, 111, 130],
                             'AirB&B': [60, 70, 85, 100, 110],
                             'Privati': [40, 45, 75, 90, 110]}
        self.listeProvvigioni = {'Booking.com': 0.18,
                                 'AirB&B': 0.3,
                                 'Privati': 0}
        self.listeTasse = {'Booking.com': True,
                           'AirB&B': True,
                           'Privati': False}
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
        self.calendario = MyCalend(
            self.dateAirbb,
            self.dateBooking,
            self.datePrivati,
            self.datePulizie,
            parent=self.frame_calendar,
        )
        self.initDatabase()
        cal_layout = QtWidgets.QGridLayout(self.frame_calendar)
        cal_layout.addWidget(self.calendario)
        self.frame_calendar.setLayout(cal_layout)

        self.calendario.clicked.connect(self.getInfoFromCalendar)
        self.calendario.selectionChanged.connect(self.setDateEdit_dal)
        self.tabWidget.currentChanged.connect(self.riempi_campi_prenotazioni)
        # self.calendario.currentPageChanged.connect(self.riportapagina)
        self.lastMonth = None
        self.current_date = None
        self.giornoCorrente = self.calendario.selectedDate()
        self.setDateEdit_dal()
        self.spinBox_importo.setMaximum(9999)
        self.dateEdit_dal.dateChanged.connect(self.correggiPartenza)
        self.bot_salva.clicked.connect(self.salvaInfo)
        self.bot_checkDisp.clicked.connect(self.botFuncCheckAval)
        self.bot_cancella.clicked.connect(self.cancellaprenot)
        self.spinBox_ospiti.valueChanged.connect(self.totOspitiAdj)
        self.spinBox_bambini.valueChanged.connect(self.totOspitiAdj)
        self.spinBox_importo.valueChanged.connect(self.calcLordoNetto)
        self.radio_booking.toggled.connect(self.importAdj)
        self.radio_air.toggled.connect(self.importAdj)
        self.radio_privato.toggled.connect(self.importAdj)
        self.radioCorrente = self.radio_booking
        self.dateEdit_al.dateChanged.connect(self.calcLordoNetto)
        self.dateEdit_dal.dateChanged.connect(self.calcLordoNetto)

        # STATUS BAR
        # self.statusbar.setT

    def calcTax(self):
        """
        prende il numero di ospiti, la data "dal" e la data "al"
        dalle spinbox
        la tassa è di 2 euro al mese per un massimo di 3 giorni,
        dal quarto è gratis per il mese corrente
        compara i mesi per ricominciare il conto dei giorni
        da pagare
        :return:
        """
        try:
            dal = self.dateEdit_dal.date()
            mese_dal = dal.month()
            al = self.dateEdit_al.date()
            mese_al = al.month()
            permanenza = dal.daysTo(al)
            ospiti = self.spinBox_ospiti.value()
            topay = 3
            fee = 2
            oggi = self.dateEdit_dal.date()
            listaDate = []
            flag = oggi != al
            while flag:
                mese = oggi.month()
                print('mese: ', mese)
                if mese != mese_dal:
                    topay = 3
                    mese_dal = mese
                if oggi not in listaDate and topay > 0:
                    listaDate.append(oggi)
                topay -= 1
                oggi = oggi.addDays(1)
                flag = oggi != al
            if permanenza != len(listaDate):
                print("qualcosa non va nel conteggio delle tasse")
            tot = len(listaDate) * ospiti * fee
            print("tassa da pagare: ", tot)
            return tot
        except:
            print(fex())

    def calcLordoNetto(self):
        """
        calcola l'ammontare del lordo e al netto delle tasse
        e delle provvigioni
        :return:
        """
        try:
            importo = self.spinBox_importo.value()
            chiave = self.getPlatformKey()
            ospiti = self.spinBox_ospiti.value() + self.spinBox_bambini.value()
            giorni = self.dateEdit_dal.date().daysTo(self.dateEdit_al.date())
            tassa = 0
            if self.listeTasse[chiave]:
                tassa = 0
            else:
                tassa = self.calcTax()
                # tassa = 0

            lordo = ospiti * importo * giorni
            print("lordo: ", lordo)
            netto = (lordo * (1 - self.listeProvvigioni[chiave])) - tassa
            print("netto: ", netto)
            self.lineEdit_lordo.setText(str(lordo))
            self.lineEdit_netto.setText(str(round(netto)))
            self.lineEdit_tax.setText(str(tassa))
        except:
            print(fex())

    def getPlatformKey(self):
        """
        restituisce la chiave per i dizionari con le liste
        self.listaProvvigioni
        self.listaImporti
        :return: chiave -> str
        """
        if self.radio_privato.isChecked():
            chiave = 'Privati'
        elif self.radio_air.isChecked():
            chiave = 'AirB&B'
        elif self.radio_booking.isChecked():
            chiave = 'Booking.com'
        return chiave

    def totOspitiAdj(self, p):
        sender = self.sender()
        widget = sender.objectName()
        widgetItself = None
        print("valore ", p)
        if widget == 'spinBox_ospiti':
            print("sender spinBox_ospiti")
            other = self.spinBox_bambini.value()
            widgetItself = self.spinBox_ospiti
        else:
            print("sender spinBox_bambini")
            other = self.spinBox_ospiti.value()
            widgetItself = self.spinBox_bambini
        tot = p + other
        if tot == EvInterface.MAXOSPITI + 1:
            print(tot)
            widgetItself.blockSignals(True)
            widgetItself.setValue(p - 1)
            widgetItself.blockSignals(False)
            tot = 5
        self.importAdj(tot)

    def importAdj(self, p):
        if type(p) is not int:
            p = int(p)
        chiave = self.getPlatformKey()
        try:

            sender = self.sender()
            if sender == self.radioCorrente:
                return
            print("sender importAdj", sender.objectName())
            if sender.objectName().startswith('radio'):
                self.radioCorrente = sender
                p = self.spinBox_bambini.value() + self.spinBox_ospiti.value()
                if p >= 5:
                    p = 5
        except:
            print(fex())
        indice = p - 1
        print("listaImporti: ", self.listeImporti[chiave][indice])
        self.spinBox_importo.setValue(self.listeImporti[chiave][indice])

    def riempi_campi_prenotazioni(self):
        """ prende le info da inserire nei campi
            della prenotazione a partire dalle info
            nel box nella pagina
            del calendario"""
        info = deepc(self.infoTemp)
        self.lineEdit_nome.setText(info['nome'])
        self.lineEdit_cognome.setText(info['cognome'])
        self.lineEdit_telefono.setText(info['telefono'])
        self.spinBox_ospiti.setValue(int(info['numero ospiti']))
        self.spinBox_bambini.setValue(int(info['bambini']))
        platform = info['platform']
        if platform == 'privato':
            self.radio_privato.setChecked(True)
        elif platform == 'booking':
            self.radio_booking.setChecked(True)
        elif platform == 'airBB':
            self.radio_air.setChecked(True)
        else:
            print(platform)
        self.plainTextEdit_note.clear()
        self.plainTextEdit_note.insertPlainText(info['note'])
        self.radio_colazione.setChecked(info['colazione'] == 'True')
        self.importAdj(self.spinBox_bambini.value() + self.spinBox_ospiti.value())
        self.dateEdit_dal.setDate(info['data arrivo'])
        self.dateEdit_al.setDate(info['data partenza'])
        # todo aggiungere funzione di calcolo importo

    def set_status_msg(self, st=""):
        self.statusbar.showMessage(st)
        return

    def cancellaprenot(self):
        """cancella la prenotazione nella data
            selezionata nel calendario"""
        manager = Manager(info=self.infoTemp)
        manager.canc()
        database = self.getDatabase(self.infoTemp['data arrivo'].year())
        # self.leggiDatabase(manager.DataBase)
        self.leggiDatabase(database)
        self.calendario.updateCells()
        self.set_status_msg('Cancellazione effettuata')

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
        """
        legge il database per restituire gli elenchi delle piattaforme
        (booking, airbb, privati, pulizie)
        per stilizzare il calendario
        :param database:
        :return:
        """
        self.dateBooking.clear()
        self.dateAirbb.clear()
        self.datePrivati.clear()
        self.datePulizie.clear()
        db = Manager(self.infoTemp)
        self.dateBooking, self.dateAirbb, self.datePrivati, self.datePulizie = db.platformPulizie()
        self.calendario.setDates(self.dateBooking, self.dateAirbb, self.datePrivati, self.datePulizie)
        # return  self.dateBooking, self.dateAirbb, self.datePrivati, self.datePulizie

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

    def checkAval(self, dal, al):
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
