from PyQt5 import QtGui, QtCore, QtWidgets
from collections import OrderedDict as Od
from copy import deepcopy as deepc
from gui import Ui_MainWindow as mainwindow
# from kwidget.mycalendar.mycalend import MyCalend
from kwidget.tableWidgetCalendar.CalendarTableWidget import CalendarTableWidget as MyCalend
from kwidget.dialog_info.dialog_info_main import DialogInfo
from kwidget.dialog_info.dialog_info_main import DialogInfoSpese as DialogSpese
from kwidget.dialog_opt.dialog_opt import DialogOption
from tools.ExpCsv import ExpCsv as excsv
from tools.databaseMaker import DbMaker as dbm
from tools.managerprenotazioni import ManagerPreno as Manager
from traceback import format_exc as fex
import inspect
import os
import sys



# todo modificare il comportamento del tasto salva quando è già presente una prenotazione, usare il tasto modifica
# todo con la funzione di preservazione delle prenotazioni già presenti
# todo aggiungere sistema UNDO

class EvInterface(mainwindow, QtWidgets.QMainWindow):
    """Classe per la creazione gui del gestionale per case vacanze

        print("controllo ", inspect.stack()[0][3])
        self.cleardisplay()
    """
    MAXOSPITI = 5
    noteCheck_signal = QtCore.pyqtSignal(bool)
    spesaCheck_signal = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None):
        super(EvInterface, self).__init__(parent)

        self.settingsIcon = './Icons/settingsIcon.png'
        self.colors = {}
        self.dateBooking = []
        self.dateAirbb = []
        self.datePrivati = []
        self.datePulizie = []
        # self.dateSpese = []
        self.dateSpese = {}
        self.dateNote = []
        self.listeImporti = {}
        self.listeProvvigioni = {}
        self.listeTasse = {}
        self.tassa = 0
        iconaMainWindow = QtGui.QIcon('./Icons/erbavento.ico')
        datePren = {'platforms': {}}
        self.datePrenotazioni = Od(datePren)
        d = {
            "nome": "",
            "cognome": "",
            "telefono": None,
            "email": '',
            "platform": "",
            "data arrivo": None,
            "data partenza": None,
            'totale notti': 0,
            "numero ospiti": 1,
            "bambini": 0,
            "spese": 0,
            "colazione": 'No',
            "stagione": '',
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
        self.setWindowTitle('Gestionale ErbaVento')
        self.setWindowIcon(iconaMainWindow)
        self.bot_note.setTipo('note')
        self.statusbar.showMessage("Ready!!!!")
        self.calendario = MyCalend(
            parent=self.frame_calendar
        )
        # self.calendario = MyCalend(
        #     self.dateAirbb,
        #     self.dateBooking,
        #     self.datePrivati,
        #     self.datePulizie,
        #     parent=self.frame_calendar,
        # )
        self.lastMonth = None
        self.current_date = None
        self.giornoCorrente = QtCore.QDate().currentDate()
        self.database = self.initDatabase()
        self.calendario.currentPageChanged.connect(self.correggiDataSelected)
        self.spese = self.initSpeseDb()

        self.infoSta = self.initStatDb()
        self.setMenuMain()
        self.loadConfig()
        cal_layout = QtWidgets.QGridLayout(self.frame_calendar)
        cal_layout.addWidget(self.calendario)
        self.frame_calendar.setLayout(cal_layout)

        # self.calendario.table.clicked.connect(self.getInfoFromCalendar)
        self.calendario.singleClicked.connect(self.getInfoFromCalendar)
        self.calendario.selectionChanged.connect(self.aggiornaInfoData)
        self.tabWidget.currentChanged.connect(self.riempi_campi_prenotazioni)
        # self.calendario.currentPageChanged.connect(self.riportapagina)

        self.setDateEdit_dal()
        self.spinBox_importo.setMaximum(9999)
        self.dateEdit_dal.dateChanged.connect(self.correggiPartenza)
        self.bot_salva.clicked.connect(self.salvaInfo)
        self.bot_checkDisp.clicked.connect(self.botFuncCheckAval)
        self.bot_cancella.clicked.connect(self.cancellaprenot)
        self.bot_modifica.clicked.connect(self.modificaESalva)
        self.spinBox_ospiti.valueChanged.connect(self.totOspitiAdj)
        self.spinBox_bambini.valueChanged.connect(self.totOspitiAdj)
        self.spinBox_importo.valueChanged.connect(self.calcLordoNetto)
        self.combo_platformPrenotazioni.currentTextChanged.connect(self.importAdj)
        self.combo_stagionePrenotazioni.currentTextChanged.connect(self.importAdj)
        # self.radio_booking.toggled.connect(self.importAdj)
        # self.radio_air.toggled.connect(self.importAdj)
        # self.radio_privato.toggled.connect(self.importAdj)
        # self.radioCorrente = self.radio_booking


        self.dateEdit_al.dateChanged.connect(self.periodoCambiato)
        self.dateEdit_dal.dateChanged.connect(self.periodoCambiato)
        self.bot_esporta.clicked.connect(self.exportaDb)
        self.bot_prenota.clicked.connect(self.vaiPrenotaTab)
        self.bot_annulla.clicked.connect(self.vaiCalendario)
        self.bot_spese.clicked.connect(self.addSpese)
        self.bot_note.clicked.connect(self.addNote)
        self.tabWidget.currentChanged.connect(self.retTab)
        self.lineEdit_nome.returnPressed.connect(self.lineEditVerifica)
        self.lineEdit_cognome.returnPressed.connect(self.lineEditVerifica)
        self.lineEdit_telefono.returnPressed.connect(self.lineEditVerifica)
        self.lineEdit_email.returnPressed.connect(self.lineEditVerifica)
        self.lineEdit_nome.TABPRESSED.connect(self.lineEditVerifica)
        self.lineEdit_cognome.TABPRESSED.connect(self.lineEditVerifica)
        self.lineEdit_telefono.TABPRESSED.connect(self.lineEditVerifica)
        self.lineEdit_email.TABPRESSED.connect(self.lineEditVerifica)
        self.calendario.table.doubleClicked.connect(self.bot_prenota.click)
        self.giornoprecedente = self.giornoCorrente.addDays(-1)
        self.calendario.updateIconsAndBooked()
        # STATUS BAR
        # self.statusbar.setT

    @QtCore.pyqtSlot()
    def addNote(self):
        try:
            # dialog = DialogInfo('Spese',table=True)
            # data = self.calendario.selectedDate()
            data = self.calendario.currentDate
            a, m, g = self.amg(data)
            text = self.database[a][m][g]['checkIn']['note']
            dialog = DialogInfo(testo=text, showBool=True)
            icona = QtGui.QIcon('./Icons/iconaNote.ico')
            dialog.setWindowIcon(icona)
            tempDict = deepc(self.database[a][m][g]['checkIn'])
            dialog.guiText.textBrowser_dialog_info.setText(text)
            if dialog.exec_():
                nuovoTesto = dialog.guiText.textBrowser_dialog_info.toPlainText()
                if nuovoTesto != text:
                    tempDict['note'] = nuovoTesto
                    self.database[a][m][g]['checkIn'] = tempDict
                    dbm.salvaDatabase(self.database)
                    self.bot_note.setState(True)
                    if nuovoTesto == '':
                        self.bot_note.setState(False)
                        if self.calendario.currentDate in self.calendario.dateNote:
                            self.calendario.dateNote.remove(self.calendario.currentDate)
                    else:
                        if self.calendario.currentDate not in self.calendario.dateNote:
                            self.calendario.dateNote.append(self.calendario.currentDate)
                    self.calendario.updateIconsAndBooked()
        except:
            print(fex())

    @QtCore.pyqtSlot()
    def addSpese(self):
        try:
            # dialog = DialogInfo('Spese',table=True)
            # data = self.calendario.selectedDate()
            data = self.calendario.currentDate
            a, m, g = self.amg(data)
            finale = self.gestisciSpese(data)
            spese = self.database[a][m][g]['checkIn']['spese']
            if spese != finale:
                copia = deepc(self.database[a][m][g]['checkIn'])
                copia['spese'] = finale
                for giorno in self.database[a][m].keys():
                    self.database[a][m][giorno]['checkIn'] = deepc(copia)

                dbm.salvaDatabase(self.database)
            self.updateInfoStat()
            self.riempiTabellaStat()
            # print(self.dateSpese)
        except:
            print(fex())

    def aggiornaInfoData(self):
        # data = self.calendario.selectedDate()
        data = self.calendario.currentDate
        domani = data.addDays(1)
        anno = data.year()
        if anno < 2018:
            print("anno troppo vecchio!")
            self.tabWidget.setCurrentIndex(0)
        elif anno > 2028:
            print("anno troppo avanti")
            self.tabWidget.setCurrentIndex(0)
        else:
            pass
        # if self.sender() is not None:
        #     sender = self.sender().objectName()
        #     print(f"{inspect.stack()[0][3]} mandato da {self.sender().objectName()}")

        self.setInfoTemp(self.getInfoFromDate(data))
        if self.infoTemp['data arrivo'] is None:
            self.bot_cancella.setEnabled(False)
        else:
            self.bot_cancella.setEnabled(True)
        self.setDateEdit_dal()

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

    def buildListeIPT(self):
        # self.listeImporti = {'Booking': [72, 74, 92, 111, 130],
        #                      'AirB&B': [64, 65, 85, 100, 117],
        #                      'Privati': [72, 74, 92, 111, 130]}
        # self.listeProvvigioni = {'Booking': 0.15,
        #                          'AirB&B': 0.03,
        #                          'Privati': 0}
        # self.listeTasse = {'Booking': False,
        #                    'AirB&B': False,
        #                    'Privati': False}
        platforms = [p for p in self.config['platforms']]
        stagione = self.combo_stagionePrenotazioni.currentText()
        importi = self.config['stagione'][stagione]
        self.listeImporti = {p: i for p, i in importi.items()}
        self.listeProvvigioni = {p: prov for p, prov in self.config['provvigioni'].items()}
        self.listeTasse = {p: t for p, t in self.config['tasse attive'].items()}
        self.tassa = self.config['tasse']

    def calcLordoNetto(self):
        """
        calcola l'ammontare del lordo e al netto delle tasse
        e delle provvigioni
        :return:
        """
        try:
            importo = self.spinBox_importo.value()
            chiave = self.combo_platformPrenotazioni.currentText()
            ospiti = self.spinBox_ospiti.value() + self.spinBox_bambini.value()
            giorni = self.dateEdit_dal.date().daysTo(self.dateEdit_al.date())
            tassa = 0
            if self.listeTasse[chiave]:
                tassa = 0
            else:
                tassa = self.calcTax()
                # tassa = 0

            lordo = importo * giorni + tassa
            # print("lordo: ", lordo)
            netto = (lordo * (1 - self.listeProvvigioni[chiave])) - tassa
            # print("netto: ", netto)
            self.lineEdit_lordo.setText(str(lordo))
            self.lineEdit_netto.setText(str(round(netto)))
            self.lineEdit_tax.setText(str(tassa))
        except:
            print("fallimento funz calcolo lordonetto")
            # print(fex())

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
            fee = self.tassa
            oggi = self.dateEdit_dal.date()
            listaDate = []
            flag = oggi != al
            while flag:
                mese = oggi.month()
                # print('mese: ', mese)
                if mese != mese_dal:
                    topay = 3
                    mese_dal = mese
                if oggi not in listaDate and topay > 0:
                    listaDate.append(oggi)
                topay -= 1
                oggi = oggi.addDays(1)
                flag = oggi != al
            if permanenza != len(listaDate):
                pass
                # print("qualcosa non va nel conteggio delle tasse")
            tot = len(listaDate) * ospiti * fee
            if tot == 0:
                tot = fee
            # print("tassa da pagare: ", tot)
            return tot
        except:
            print(fex())

    def cancellaprenot(self, wrnMode=False):
        """cancella la prenotazione nella data
            selezionata nel calendario"""
        print('cancella')
        if  wrnMode:
            if self.warnMsg():
                manager = Manager(info=self.infoTemp)
                manager.canc()
                # database = self.getDatabase(self.infoTemp['data arrivo'].year())
                database = self.getDatabase()
                # self.leggiDatabase(manager.DataBase)
                # self.leggiDatabase(database)
                self.leggiDatabase()
                print('cancellazione current date: ', self.calendario.currentDate)
                giornoPulizie = self.calendario.currentDate.addDays(1)
                if giornoPulizie in self.datePulizie:
                    self.datePulizie.remove(giornoPulizie)
                if giornoPulizie in self.calendario.datePulizie:
                    self.calendario.datePulizie.remove(giornoPulizie)
                    self.calendario.updateIconsAndBooked()
                # self.calendario.updateCells()
                self.set_status_msg('Cancellazione effettuata')
        else:
            manager = Manager(info=self.infoTemp)
            manager.canc()
            # database = self.getDatabase(self.infoTemp['data arrivo'].year())
            database = self.getDatabase()
            # self.leggiDatabase(manager.DataBase)
            # self.leggiDatabase(database)
            self.leggiDatabase()
            giornoPulizie = self.calendario.currentDate.addDays(1)
            if giornoPulizie in self.datePulizie:
                self.datePulizie.remove(giornoPulizie)
            if giornoPulizie in self.calendario.datePulizie:
                self.calendario.datePulizie.remove(giornoPulizie)
                self.calendario.updateIconsAndBooked()
            # self.calendario.updateCells()
            self.set_status_msg('Cancellazione effettuata without warnig')

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
                # if listaDisponibili[0] == QtCore.QDate(2019, 7, 14):
                #     print("presto!")
                # else:
                #     print("il primo disp: ", listaDisponibili[0])
                self.dateEdit_dal.update()
                for d in listaDisponibili:
                    print("date disponibili", d)

        return listaDisponibili

    def checkInfo(self):
        # print(type(self.listaWGen))
        listaW = [self.lineEdit_nome, self.lineEdit_cognome, self.lineEdit_telefono]
        for w in listaW:
            if w.text() == '':
                w.setFocus()
                w.selectAll()
                return False

        return True

    def cleardisplay(self):
        return os.system('cls')

    def compilaInfo(self):
        """
        compila il modello (riga  csv ) da salvare a partire dai campi compilati
        :return:
        """
        a = self.infoModel.copy()
        a["nome"] = self.lineEdit_nome.text()
        a["cognome"] = self.lineEdit_cognome.text()
        a["telefono"] = self.lineEdit_telefono.text()
        a['email'] = self.lineEdit_email.text()
        a["platform"] = self.combo_platformPrenotazioni.currentText()
        # a["data arrivo"] = self.dateEdit_dal.date().toString("dd MMM yyyy")
        a["data arrivo"] = self.dateEdit_dal.date()
        # a["data partenza"] = self.dateEdit_al.date().toString("dd MMM yyyy")
        a["data partenza"] = self.dateEdit_al.date()
        a['totale notti'] = str(self.dateEdit_dal.date().daysTo(self.dateEdit_al.date()))
        a["numero ospiti"] = str(self.spinBox_ospiti.text())
        a["bambini"] = self.spinBox_bambini.text()
        # a["spese"] = self.addSpese()
        if self.radio_colazione.isChecked():
            a["colazione"] = 'Si'
        else:
            a["colazione"] = 'No'
        a["stagione"] = self.combo_stagionePrenotazioni.currentText()
        a["importo"] = self.spinBox_importo.text()
        a["lordo"] = self.lineEdit_lordo.text()
        a["netto"] = self.lineEdit_netto.text()
        a["tasse"] = self.lineEdit_tax.text()
        a["note"] = self.plainTextEdit_note.toPlainText()
        try:
            spese = self.spese[self.dateEdit_dal.date()]
        except KeyError:
            data = self.dateEdit_dal.date()
            an, m, g = self.amg(data)
            spese = self.database[an][m][g]['checkIn']['spese']
        a['spese'] = spese
        return a

    def correggiDataSelected(self):
        """seleziona il primo del mese se si cambia la pagina del calendario"""
        # print('correggiDataSelected')
        # data = QtCore.QDate(self.calendario.yearShown(), self.calendario.monthShown(), 1)
        # print('correggiDataSelected', data)
        # self.calendario.setSelectedDate(data)
        self.riempiTabellaStat()

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
            self.giornoprecedente = al
            self.dateEdit_al.setDate(al)
            self.dateEdit_al.setMinimumDate(d.addDays(1))
            # print("correzione in avanti effettuata")
        else:
            pass
            # print("partenza ok")
        if md >= d:
            self.dateEdit_al.setMinimumDate(d.addDays(1))

    def dataParser(self, data):
        anno = data.toString("yyyy")
        mese = data.toString("MMM")
        giorno = int(data.toString("dd"))
        return anno, mese, giorno

    def dialogDisponibili(self, l):
        d = DialogInfo('Note', showBool=True)
        try:
            d.setWindowModality(QtCore.Qt.WindowModal)
            d.guiText.textBrowser_dialog_info.setReadOnly(True)
        except:
            print(fex())
        data = ''
        if len(l) > 0:
            for g in l:
                data += g.addDays(1).toString("dd/MM/yyyy") + '\n'
        else:
            data = 'Nessuna data disponibile'
        d.guiText.textBrowser_dialog_info.setText(data)
        d.exec_()

    def dialogOpt(self):
        try:
            dialog = DialogOption(self)
            if dialog.exec_():
                conf = dialog.config

            self.config = conf
            self.loadConfig()
            self.leggiDatabase()
            # todo copiare la variabile self.config
        except UnboundLocalError:
            pass
        except:
            print(fex())

    def exportaDb(self):
        anno = self.giornoCorrente.year()
        db = self.getDatabase()
        exdb = excsv(db)
        exdb.makeCsv()
        self.statusbar.showMessage('Esportazione eseguita con successo')
        # li = exdb.updateDiz()
        # print("lunghezza li ",len(li))
        # print("dal click: \n\t\t",li[9].items())
        # exdb.checkFile()

    def gestisciNote(self,info):
        try:
            # data = self.calendario.selectedDate()
            data = self.calendario.currentDate
            a, m, g = self.amg(data)
            nota = self.database[a][m][g]['checkIn']['note']
            dialog = DialogInfo(info, testo=nota, showBool=True)

            dialog.guiText.textBrowser_dialog_info.setText(nota)
            if dialog.exec_():
                nuovoTesto = dialog.guiText.textBrowser_dialog_info.toPlainText()
                if nuovoTesto != nota:
                    self.database[a][m][g]['checkIn']['spese'] = nuovoTesto
                    dbm.salvaDatabase(self.database)

        except:
            print(fex())

    def gestisciSpese(self, datat):
        try:
            # dialog = DialogInfo('Spese',table=True)
            a, m, g = self.amg(datat)
            spesetot = deepc(self.spese)
            spese = spesetot[a][m].get(datat, {})
            dialog = DialogSpese(spese)
            dialog.setWindowIcon(QtGui.QIcon('./Icons/iconaSpese.png'))
            dialog.SPESEPRONTE.connect(lambda x: print(x))
            if dialog.exec_():
                spese = dialog.ottieniSpese()
                if len(spese) != 0:
                    self.spese[a][m][datat] = spese
                    self.bot_spese.setState(True)
                    tot = self.totaleSpeseG(datat)
                    print('totale spese giornaliere: ', tot)
                    self.calendario.dateSpese.append(datat)
                    self.calendario.datesIndicatorsChanged.emit()
                else:
                    if datat in self.spese[a][m].keys():
                        del self.spese[a][m][datat]
                    if datat in self.calendario.dateSpese:
                        self.calendario.dateSpese.remove(datat)
                        self.calendario.datesIndicatorsChanged.emit()

                    self.bot_spese.setState(False)
                    tot = 0

                self.calendario.datesIndicatorsChanged.emit()
                self.calendario.updateIconsAndBooked()
                totSpeseMensili = 0
                try:
                    for giornoData in self.spese[a][m].keys():
                        for spesaperitem in self.spese[a][m][giornoData].values():
                            totSpeseMensili += spesaperitem
                    finale = float(totSpeseMensili)
                except TypeError:
                    print(' TYPEERR *****************', self.spese[a][m].values())
                dbm.salvaDatabase(self.spese, tipodatabase='spese')
                return finale
        except:
            print(fex())

    def get_date(self, d):
        # a = self.calendarWidget.dateTextFormat()
        # self.calendario.set
        self.setLabel_stagione(d)
        # print('get_date current date ',d)
        self.current_date = d
        if self.lastMonth != self.current_date.month():
            self.lastMonth = self.current_date.month()
        # print(d.month(),'<<<<',self.calendario.month())
        # print("selection changed", self.current_date_label)

        return self.current_date

    def getDatabase(self, anno=None, tipo='database'):
        Dbm = dbm()
        database = Dbm.checkFile(tipodatabase=tipo)
        return database

    def getInfo(self, a, m, g):
        try:
            database = self.getDatabase()
            # print("getinfo database keys:\n", database.keys())
            info = database[a][m][g]["checkIn"]
            # print('getInfo', info)
        except KeyError:
            print("keyerr getInfo evinterf")

            info = None
        return info

    def getInfoFromCalendar(self, data):
        # self.cleardisplay()
        # if self.sender() is not None:
        #     sender = self.sender().objectName()
        #     print(f"{inspect.stack()[0][3]} mandato da {self.sender().objectName()}")
        # print('getInfoFromCalendar ', data)
        info = self.getInfoFromDate(data)
        self.setInfoFromDate(info)
        self.setInfoTemp(info)
        return info

    def getInfoFromDate(self, data):
        # self.cleardisplay()
        # print("controllo ", inspect.stack()[0][3])
        self.get_date(data)
        # print("data ",self.current_date)
        a, m, g = self.amg(data)
        info = self.getInfo(a, m, g)
        if info is None:
            info = deepc(self.infoModel)
        return info

    def importAdj(self):
        if self.sender() is not None:
            print(self.sender().objectName())
        totOspiti = self.spinBox_bambini.value() + self.spinBox_ospiti.value()
        maxOspiti = self.config['numero letti']
        if totOspiti >= maxOspiti:
            totOspiti = maxOspiti
        self.spinBox_ospiti.setMaximum(maxOspiti)
        self.spinBox_bambini.setMaximum(maxOspiti - self.spinBox_ospiti.value())
        self.tassa = self.config['tasse']
        self.calcLordoNetto()
        indice = totOspiti - 1
        platform = self.combo_platformPrenotazioni.currentText()
        self.buildListeIPT()
        try:
            self.spinBox_importo.setValue(self.listeImporti['importi'][platform][indice])
            # print('value: ', self.listeImporti['importi'][platform][indice])
        except KeyError:
            print('self.listeImporti\n \t', self.listeImporti)
            for v in self.listeImporti.keys():
                print(len(v))
            print('err key: ', len(platform))

    def initConfig(self):
        d = DialogOption()
        config = d.checkConfigFile()
        return config

    def initDatabase(self, anno=None):
        # anno = self.calendario.yearShown()
        if anno is None:
            anno = QtCore.QDate().currentDate().year()
        self.database = self.getDatabase()
        self.spese = self.initSpeseDb()
        self.infoSta = self.initStatDb(self.database)
        self.config = self.initConfig()
        self.leggiDatabase(self.database)
        # self.leggiDatabase(database)
        print("initDatabase ")
        csvDir = './csv'
        if os.path.isdir(csvDir):
            # print("csv esiste")
            pass
        else:
            os.mkdir(csvDir)
        anni = self.database.keys()
        for a in anni:
            csvDir = f"./csv/{str(a)}"
            if os.path.isdir(csvDir):
                pass
                # print(f"./csv/{str(a)}"+'\tesiste')
            else:
                os.mkdir(csvDir)
        return self.database

    def initSpeseDb(self):
        spese = self.getDatabase(tipo='spese')
        return spese

    def initStatDb(self, database={}):
        if database is None or len(database) == 0:
            database = deepc(self.database)

        def formatStuff(li):
            form = {k: 0 for k in li}
            return Od(form)

        statG = deepc(database)
        stat = deepc(database)
        l = ['3 Notti', '2 Notti', '1 Notte', 'Tasse finora', 'Netto finora']
        formatStat = formatStuff(l)
        for anno in database.keys():
            for mese in database[anno].keys():
                stat[anno][mese] = {}
                formatStat = formatStuff(l)
                for giorno in database[anno][mese].keys():
                    statGiornaliere = statG[anno][mese][giorno]
                    chiave = database[anno][mese][giorno]['checkIn']
                    numeroNotti = int(chiave['totale notti'])
                    try:
                        formatStat['Spese finora'] = int(chiave['spese'])
                    except TypeError:
                        pass
                        # print(database[anno][mese][giorno])
                        # print(anno, mese, giorno)
                        # raise TypeError
                    if numeroNotti >= 3:
                        formatStat['3 Notti'] += 1
                    elif numeroNotti == 2:
                        formatStat['2 Notti'] += 1
                    elif numeroNotti == 1:
                        formatStat['1 Notte'] += 1
                    tasse = int(chiave['tasse'])
                    formatStat['Tasse finora'] += tasse
                    netto = int(chiave['netto'])
                    formatStat['Netto finora'] += netto
                stat[anno][mese] = deepc(formatStat)
                formatStat = formatStuff(l)
        return stat

    def leggiDatabase(self, database=None):
        """
        legge il database per restituire gli elenchi delle piattaforme
        (booking, airbb, privati, pulizie)
        per stilizzare il calendario
        :param database:
        :return:
        """
        try:
            db = Manager()
            # self.datePrenotazioni, self.datePulizie, self.dateSpese, self.dateNote = db.platformPulizie(database)
            self.datePrenotazioni, self.datePulizie, self.dateNote = db.platformPulizie(database)
            self.dateSpese = db.getDataSpese()
            # print(' spese passate per icone:: ', self.dateSpese)
            self.calendario.setDatesIndicators(self.datePrenotazioni,
                                               self.datePulizie,
                                               self.config['colori settati'],
                                               self.dateSpese,
                                               self.dateNote
                                               )
            # print('spese passate al calendario: ', self.calendario.dateSpese)
            # print('pulizie passate al calendario: ', self.calendario.datePulizie)
            #todo selectedDate restituice Qmodelindex invece che data
            # data = self.calendario.selectedDate()
            data = self.calendario.currentDate
            info = self.getInfoFromDate(data)
            self.setInfoFromDate(info)
            self.infoSta = self.initStatDb(db.DataBase)
            self.riempiTabellaStat()
            if database is None:
                self.database = db.DataBase
        except:
            print(fex())

    def lineEditVerifica(self):
        # print('Hola ',self.bot.text())
        # print('ciao ', self.sender().text())
        print("TABPRESSED")
        listaInfo = [self.infoModel['nome'], self.infoModel['cognome'], self.infoModel['telefono']]
        testo = self.sender().text()
        if testo not in listaInfo:
            self.modificaOsalva(modifica=False)
        else:
            self.modificaOsalva(modifica=True)
        if not self.sender().selector(testo):
            self.sender().clear()
        else:
            self.sender().nextInFocusChain().setFocus()

    def loadConfig(self):
        numeroOspiti = self.config['numero letti']
        self.spinBox_ospiti.setMaximum(numeroOspiti)
        self.spinBox_bambini.setMaximum(numeroOspiti - 1)
        self.buildListeIPT()
        self.colors = deepc(self.config['colori settati'])
        # database = self.getDatabase()
        # self.leggiDatabase(database)
        # self.infoModel
        plats = self.config['platforms']
        self.combo_platformPrenotazioni.clear()
        for platform in plats.keys():
            if platform != '' and self.combo_platformPrenotazioni.findText(platform, QtCore.Qt.MatchExactly) == -1:
                self.combo_platformPrenotazioni.addItem(platform)
        self.lineEdit_tax.setText(str(self.config['tasse']))

    def modificaESalva(self):
        try:
            info = self.compilaInfo()
            dal = self.dateEdit_dal.date()
            al = self.dateEdit_al.date()
            manager = Manager(info)
            listaDisponibili = manager.checkAval(dal, al, nomePassato=self.lineEdit_nome.text(),
                                                 cognomePassato=self.lineEdit_cognome.text())
            giorniPermanenza = dal.daysTo(al)
            if len(listaDisponibili) == giorniPermanenza:
                print('modifica ok')
                print('prima cancello')
                self.cancellaprenot(wrnMode=True)
                print('poi salvo...')
                self.salvaInfo(modo=False)
            else:
                self.dialogDisponibili(listaDisponibili)
        except:
            print(fex())

    def modificaOsalva(self, modifica=False):
        flagMod = modifica
        flagSalva = not modifica
        self.bot_salva.setEnabled(flagSalva)
        self.bot_modifica.setEnabled(flagMod)
        # self.bot_modifica.setEnabled(True)
        # self.bot_salva.setEnabled(True)

    def periodoCambiato(self, p):
        d = self.dateEdit_dal.date()
        a = self.dateEdit_al.date()
        giorni = d.daysTo(a)
        self.lineEdit_numeroGiorni.setText(str(giorni))
        self.calcLordoNetto()

    def retTab(self, c):
        # anno = self.calendario.selectedDate().year()
        anno = self.calendario.currentDate.year()
        if anno < 2018:
            print("anno troppo vecchio!")
            self.tabWidget.setCurrentIndex(0)
        elif anno > 2028:
            print("anno troppo avanti")
            self.tabWidget.setCurrentIndex(0)
        else:
            # self.setDateEdit_dal()
            pass
        # if self.sender() is not None:
        #     sender = self.sender().objectName()
        #     print(f"{inspect.stack()[0][3]} mandato da {self.sender().objectName()}")
        self.lineEdit_nome.setFocus()

    def riempi_campi_prenotazioni(self):
        """ prende le info da inserire nei campi
            della prenotazione a partire dalle info
            nel box nella pagina
            del calendario"""
        try:
            info = deepc(self.infoTemp)
            if (info['nome'] and info['cognome'] and info['telefono']) == '':
                self.modificaOsalva()
            else:
                self.modificaOsalva(modifica=True)
            self.lineEdit_nome.setText(info['nome'])
            self.lineEdit_cognome.setText(info['cognome'])
            self.lineEdit_telefono.setText(info['telefono'])
            self.lineEdit_email.setText(info['email'])
            self.spinBox_ospiti.setValue(int(info['numero ospiti']))
            self.spinBox_bambini.setValue(int(info['bambini']))
            platform = info['platform']
            if platform != '':
                indiceCombo = self.combo_platformPrenotazioni.findText(platform)
            else:
                indiceCombo = 0
            self.combo_platformPrenotazioni.setCurrentIndex(indiceCombo)
            print('indice Combo: ', indiceCombo)
            print('platform: ', platform)
            # try:
            #
            # except:
            #     print(fex())
            self.plainTextEdit_note.clear()
            self.plainTextEdit_note.insertPlainText(info['note'])
            self.radio_colazione.setChecked(info['colazione'] == 'Si')
            # self.importAdj(self.spinBox_bambini.value() + self.spinBox_ospiti.value())
            stagione = info['stagione']
            indiceComboStagione = self.combo_stagionePrenotazioni.findText(stagione)
            if indiceComboStagione == -1:
                indiceComboStagione = self.combo_stagionePrenotazioni.findText(self.config['stagione preferita'])
            self.combo_stagionePrenotazioni.setCurrentIndex(indiceComboStagione)
            self.importAdj()
            dataArrivo = info['data arrivo']
            dataPartenza = info['data partenza']
            if (dataArrivo or dataPartenza) is not None:
                self.dateEdit_dal.blockSignals(True)
                self.dateEdit_al.blockSignals(True)
                self.dateEdit_dal.setDate(dataArrivo)
                self.dateEdit_al.setMinimumDate(dataArrivo.addDays(1))
                self.dateEdit_al.setDate(dataPartenza)
                self.dateEdit_dal.blockSignals(False)
                self.dateEdit_al.blockSignals(False)
                self.lineEdit_numeroGiorni.setText(info['totale notti'])
            else:
                # print("else: setDateEdit_dal")
                self.setDateEdit_dal()
                # self.dateEdit_al.setDate(dataPartenza)
        except:
            print(fex())

    def riempiTabellaPrenotazioni(self, info):
        """
        compila la tabella dal modello infoTemp
        :param info: modello preso dal database
        :return: ritorna il dizionario con lo status
                 per i progressbutton
        """
        statusBot = {'note': False, 'spese': False}
        if len(info):
            for bot in statusBot.keys():
                try:
                    if len(info[bot]):
                        statusBot[bot] = True
                    else:
                        statusBot[bot] = False
                except TypeError:
                    pass
        nome = info["nome"]
        cognome = info["cognome"]
        telefono = info["telefono"]
        platform = info["platform"]
        ospiti = info["numero ospiti"]
        bambini = info["bambini"]
        checkIn = info["data arrivo"]
        numeroNotti = info['totale notti']
        note = info['note']
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
            pass
            # item = QtWidgets.QTableWidgetItem("Si")
        else:
            pass
            # item = QtWidgets.QTableWidgetItem("No")
        item = QtWidgets.QTableWidgetItem(numeroNotti)
        self.tableWidget_info_ospite.setItem(4, 0, item)
        item = QtWidgets.QTableWidgetItem(platform)
        self.tableWidget_info_ospite.setItem(4, 1, item)
        item = QtWidgets.QTableWidgetItem(checkIn)
        self.tableWidget_info_ospite.setItem(5, 0, item)
        item = QtWidgets.QTableWidgetItem(checkOut)
        self.tableWidget_info_ospite.setItem(5, 1, item)
        self.tableWidget_info_ospite.update()
        # data = self.calendario.selectedDate()
        data = self.calendario.currentDate
        # print('data for spese and notes ', data)
        if data in self.spese[data.year()][data.month()].keys():
            self.bot_spese.setState(True)
        else:
            self.bot_spese.setState(False)
        if note != '':
            # print('verifica note: ', note)
            self.bot_note.setState(True)
        else:
            self.bot_note.setState(False)
        return statusBot

    def riempiTabellaStat(self, info=None):
        if info is None:
            info = deepc(self.infoSta)
        # data = self.calendario.selectedDate()
        data = self.calendario.currentDate
        a, m, g = self.amg(data)
        dbStat = deepc(info)
        try:
            self.tableWidget_stat.setRowCount(0)
            row = 0
            for c0, c1 in dbStat[a][m].items():
                self.tableWidget_stat.insertRow(row)
                item0 = QtWidgets.QTableWidgetItem()
                item0.setText(c0)
                item1 = QtWidgets.QTableWidgetItem()
                item1.setText(str(c1))
                self.tableWidget_stat.setItem(row, 0, item0)
                self.tableWidget_stat.setItem(row, 1, item1)
                row += 1
            self.tableWidget_stat.update()
        except KeyError:
            print('riempi stat key err ')
            print(dbStat.keys())

    def salvaInfo(self, modo=True):
        """modo = False # 'senza controllo' # modo = True #'con controllo'
        :return:
        """
        flag = bool
        # modo = False  # 'senza controllo' # modo = True #'con controllo'
        flag = self.checkInfo()
        if flag:
            info = self.compilaInfo()
            for k, v in info.items():
                print(k, v, sep=' ', end='\n')
            print()
            dal = info['data arrivo']
            al = info['data partenza']
            anno = dal.year()
            giorniPermanenza = dal.daysTo(al)
            print("(salvaInfo NUOVA) anno: ", anno)
            manager = Manager(info)
            listaDisponibili = manager.checkAval(dal, al)
            if len(listaDisponibili) == giorniPermanenza:
                controllo = True
            else:
                controllo = False
            if not modo: controllo = True
            if controllo:
                manager.setThem()
                print("prenotazione effettuata per tutte le date richieste")
                self.leggiDatabase()
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
                self.dialogDisponibili(listaDisponibili)
        else:
            print('salvataggio fallito')
            self.statusbar.showMessage('salvataggio fallito')

    def set_status_msg(self, st=""):
        self.statusbar.showMessage(st)
        return

    def setDateEdit_dal(self):

        # todo rimuovere il commento a:
        # self.dateEdit_dal.setMinimumDate(self.giornoCorrente)
        # self.dateEdit_al.setMinimumDate(self.giornoCorrente.addDays(1))
        # if self.sender() is not None:
        #     sender = self.sender().objectName()
        # print(f"{inspect.stack()[0][3]} mandato da {self.sender().objectName()}")
        data = self.get_date(self.calendario.currentDate)
        domani = data.addDays(1)
        anno = data.year()
        if anno < 2018 or anno > 2028:
            return
        self.dateEdit_dal.setMinimumDate(QtCore.QDate(2018, 1, 1))
        self.dateEdit_dal.setDate(data)
        self.dateEdit_al.setDate(domani)
        self.dateEdit_al.setMinimumDate(domani)
        print(f"dal {data.toString('dd-MMM-yyyy')} al {domani.toString('dd-MMM-yyyy')}")

    def setIcons(self):
        """sets the righ icons"""
        pass

    def setInfoFromDate(self, info):
        """compila la tabella dal modello infoTemp"""
        self.riempiTabellaStat()
        statusBot = self.riempiTabellaPrenotazioni(info)

    def setInfoTemp(self, info, data=None):

        if info is None:
            self.infoTemp = deepc(self.infoModel)
        else:
            self.infoTemp = deepc(info)
        return self.infoTemp

    def setLabel_stagione(self, data):
        a, m, g = self.amg(data)
        stagione = self.database[a][m][g]['checkIn']['stagione']
        self.label_stagione.setText(stagione)

    def setMenuMain(self):
        optionMenuAction = QtWidgets.QAction(QtGui.QIcon(self.settingsIcon), 'opzioni', self)
        optionMenuAction.setShortcut('Ctrl+O')
        optionMenuAction.setStatusTip('Apre le impostazioni')
        optionMenuAction.triggered.connect(self.dialogOpt)
        self.menuMenu.addAction(optionMenuAction)

    def totaleSpeseG(self, data: QtCore.QDate):
        tot = 0
        a, m, g = self.amg(data)
        if data in self.spese[a][m].keys():
            for spesa in self.spese[a][m][data].values():
                tot += spesa
        return tot

    def totOspitiAdj(self, p):
        # sender = self.sender()
        # widget = sender.objectName()
        # widgetItself = None
        # # print("valore ", p)
        # if widget == 'spinBox_ospiti':
        #     # print("sender spinBox_ospiti")
        #     other = self.spinBox_bambini.value()
        #     widgetItself = self.spinBox_ospiti
        # else:
        #     # print("sender spinBox_bambini")
        #     other = self.spinBox_ospiti.value()
        #     widgetItself = self.spinBox_bambini
        # tot = p + other
        # if tot == EvInterface.MAXOSPITI + 1:
        #     # print(tot)
        #     widgetItself.blockSignals(True)
        #     widgetItself.setValue(p - 1)
        #     widgetItself.blockSignals(False)
        #     tot = 5
        self.importAdj()

    def updateInfoStat(self):
        self.infoSta = self.initStatDb()

    def vaiCalendario(self):
        self.tabWidget.setCurrentIndex(0)

    def vaiPrenotaTab(self):
        self.tabWidget.setCurrentIndex(1)

    def warnMsg(self, default=0):
        """ Finestra di avviso, nome + 'ciò che è scritto sul bottone' + già esistente"""
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setWindowTitle("Attenzione!")
        msg.setText("Vuoi davvero cancellare la prenotazione?")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        # questo di sotto serve se voglio fare qualcosa dopo che è stato premuto ok
        # msg.buttonClicked.connect(msgbtn)
        # questo di sotto serve a far apparire la finestra
        result = msg.exec_()
        if result == QtWidgets.QMessageBox.Ok:
            return True
        else:
            return False


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    ui = EvInterface()

    ui.show()
    sys.exit(app.exec_())