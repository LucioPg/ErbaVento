from PyQt5 import QtGui, QtCore, QtWidgets
from collections import OrderedDict as Od
from copy import deepcopy as deepc
from gui import Ui_MainWindow as mainwindow
# from kwidget.mycalendar.mycalend import MyCalend
from mongoengine import *
from kwidget.tableWidgetCalendar.CalendarTableWidget_secondo import CalendarTableWidget as MyCalend
from mongo.MongoConnection import MongoConnection, DateExc, OspiteExc, OspiteIllegalName, ConnectionDict, MultiMongoErrs
from pymongo import errors
from kwidget.dialog_info.dialog_info_main import DialogInfo
from kwidget.dialog_info.dialog_info_main import DialogInfoSpese as DialogSpese
from kwidget.dialog_opt.dialog_opt import DialogOption
# from kwidget.dialog_export.ExportMongo import *
from tools.ExpCsv import ExpCsv as excsv
from traceback import format_exc as fex
from pprint import pprint
import inspect
import os
import sys
import time

import kwidget.waiting_spinner.waitingspinnerwidget


# todo modificare il comportamento del tasto salva quando è già presente una prenotazione, usare il tasto modifica
# todo con la funzione di preservazione delle prenotazioni già presenti
# todo aggiungere sistema UNDO

class LifoStack:
    stack = []

    def push(self,operation):
        self.stack.append(operation)

    def pull(self):
        if self.stack:
            return self.stack[0]



class Main(QtCore.QObject):
    counter = 0
    def __init__(self):
        super(Main, self).__init__()
        self.all_connected = False
        self.thread_ui = QtCore.QThread()
        self.thread_ui.setObjectName('thread ui')
        self.ui = EvInterface()
        self.ui.moveToThread(self.thread_ui)
        # self.thread_ui.started.connect(self.ui.turn_on)
        self.counter += 1
        self.wait_thread = QtCore.QThread()

        self.thread_mongo = QtCore.QThread()
        self.thread_mongo.setObjectName('thread mongo')
        self.Mongo_th = MongoTh()
        self.Mongo_th.moveToThread(self.thread_mongo)
        self.Mongo_th.finished_.connect(self.thread_mongo.quit)
        self.thread_mongo.started.connect(self.Mongo_th.run)

        # self.Mongo_th.finished_.connect(self.thread_mongo.finished)
        # self.Mongo_th.finished_.connect(self.thread_ui.start)
        self.Mongo_th.CONNECTED_segnale.connect(self.ui.turn_on)
        print(self.Mongo_th.receivers(self.Mongo_th.finished_))
        self.thread_mongo.start()
        self.thread_ui.started.connect(lambda: self.Mongo_th.disconnect())
        self.thread_mongo.finished.connect(lambda: print('kkkkk',self.Mongo_th.receivers(self.Mongo_th.finished_)))

    def set_all_connected(self, status):
        self.all_connected = status



class MongoTh(QtCore.QObject):
    connected = bool
    CONNECTED_segnale = QtCore.pyqtSignal(bool)
    finished_segnale = QtCore.pyqtSignal(bool)
    finished_ = QtCore.pyqtSignal()
    completed = bool
    def __init__(self, connection_dict: ConnectionDict=ConnectionDict(nome_db='test_db',
                                              host='localhost',
                                              port=27017,
                                              user='admin',
                                              password='admin',
                                              time_out=1000,
                                              tentativi=5,
                                              sleep=1), flag=True):
        super(MongoTh, self).__init__()
        self.connection_dict = connection_dict
        self.connected = False
        self.flag = flag
        self.setObjectName('MongoThreaObj')

    def run(self):
        """Creates a test connection for to check if the host is on-line
            :returns True if connection has been established, False otherwise"""
        # while self.flag:
        print('Thread')
        try:
            print(self.sender().objectName())
        except Exception as e:
            print(e)
        for tentativo in range(self.connection_dict.tentativi):
            try:
                self.completed = False
                host = self.connection_dict.host
                port = int(self.connection_dict.port)
                name = self.connection_dict.user
                password = self.connection_dict.password
                nome_db = self.connection_dict.nome_db
                _connection = connect(nome_db,
                                      host=host,
                                      port=port,
                                      serverSelectionTimeoutMS=1000,
                                      alias='another')
                self.connection = _connection[self.connection_dict.nome_db]
                # print(self.connection.authenticate(name=name,
                #                              password=password))
                # try:
                #     print('ping', self.connection.command('ping'))
                #     self.connected = bool(self.connection.command('ping'))
                # except Exception as e:
                #     print('-------------------', e)
                # self.connection.authenticate(name=name, password=password)
                self.connection.command('ping')
                self.CONNECTED_segnale.emit(True)
                self.connected = True
            except errors.OperationFailure as e:
                self.CONNECTED_segnale.emit(False)
                self.connected = False
                time.sleep(self.connection_dict.sleep)
                print(e)
                # raise MultiMongoErrs(e)
            except errors.ServerSelectionTimeoutError as e:
                self.connected = False
                self.CONNECTED_segnale.emit(False)
                print('ServerSelectionTimeoutError', e)
                # raise MultiMongoErrs(e)
            except OperationError as e:
                print('OperationError', e)
                self.connected = False
                self.CONNECTED_segnale.emit(False)
                time.sleep(self.connection_dict.sleep)
                # raise MultiMongoErrs()
            except ValueError as e:
                self.connected = False
                self.CONNECTED_segnale.emit(False)
                time.sleep(self.connection_dict.sleep)
                print(e)
            except errors.NotMasterError as e:
                self.connected = False
                self.CONNECTED_segnale.emit(False)
                time.sleep(self.connection_dict.sleep)
                print(e)
        # raise MultiMongoErrs(e)
        self.finished_segnale.emit(self.connected)
        self.finished_.emit()
        self.completed = True
        # time.sleep(5)
        print('end')
        return True

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
        self.initialated = False
        self.setupUi(self)
        self.calendario = MyCalend(
            parent=self.frame_calendar
        )
        cal_layout = QtWidgets.QGridLayout(self.frame_calendar)
        cal_layout.addWidget(self.calendario)
        self.frame_calendar.setLayout(cal_layout)
        self.statusbar.showMessage('Waiting for connection...')
        self.show()

    def go_ahead(self):
        self.stackedWidget.setCurrentIndex(1)

    def go_back_waiting(self):
        self.stackedWidget.setCurrentIndex(0)

    def turn_on(self, status):
        if not self.initialated:
            self.go_ahead()
            self.settingsIcon = './Icons/settingsIcon.png'
            self.colors = {}
            self.dateBooking = []
            self.dateAirbb = []
            self.datePrivati = []
            self.datePulizie = []
            # self.dateSpese = []
            self.dateSpese = []
            self.dateNote = []
            self.listeImporti = {}
            self.listeProvvigioni = {}
            self.listeTasse = {}
            self.tassa = 0
            self.prenotazione_corrente = None
            iconaMainWindow = QtGui.QIcon('./Icons/erbavento.ico')
            datePren = {'platforms': {}}
            self.datePrenotazioni = Od(datePren)
            # d = {
            #     "nome": "",
            #     "cognome": "",
            #     "telefono": None,
            #     "email": '',
            #     "platform": "",
            #     "data arrivo": None,
            #     "data partenza": None,
            #     'totale notti': 0,
            #     "numero ospiti": 1,
            #     "bambini": 0,
            #     "spese": '',
            #     "colazione": 'No',
            #     "stagione": '',
            #     "importo": 0,
            #     "lordo": 0,
            #     "tasse": 0,
            #     "netto": 0,
            #     "note": "",
            # }
            self.infoModel = Od({
                "nome": "",
                "cognome": "",
                "telefono": None,
                "email": '',
                "platform": "",
                "data arrivo": None,
                "data partenza": None,
                'totale notti': '',
                "numero ospiti": '',
                "bambini": '',
                "spese": '',
                "colazione": 'No',
                "stagione": '',
                "importo": 0,
                "lordo": 0,
                "tasse": 0,
                "netto": 0,
                "note": "",
                "prenotazione": None,
            })
            self.infoTemp = deepc(self.infoModel)
            # r = {"nome": "", "cognome": "", "data partenza": ""}
            self.infoModelRedux = Od({"nome": "", "cognome": "", "data partenza": ""})
            # self.info_cache = {}
            #  init gui

            self.setWindowModality(QtCore.Qt.WindowModal)
            self.setWindowTitle('Gestionale ErbaVento')
            self.setWindowIcon(iconaMainWindow)
            self.bot_note.setTipo('note')
            self.statusbar.showMessage("Ready!!!!")

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
            # self.database = self.initDatabase()
            self.calendario.currentPageChanged.connect(self.mese_calendario_cambiato)
            # self.spese = self.initSpeseDb()
            self.spese = ''
            self.config = self.initConfig()
            self.mongo = MongoConnection(self, self.connection_dict)
            self.infoSta = None
            # self.infoSta = self.initStatDb()
            self.setMenuMain()
            self.loadConfig()
            # cal_layout = QtWidgets.QGridLayout(self.frame_calendar)
            # cal_layout.addWidget(self.calendario)
            # self.frame_calendar.setLayout(cal_layout)

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
            self.initialated = True
            # self.show()
            #             # STATUS BAR
            #             # self.statusbar.setT


    @QtCore.pyqtSlot()
    def addNote(self):
        try:
            data = self.calendario.currentDate
            note_doc = self.mongo.get_note(data,_create=1)
            text = note_doc.note if note_doc else ''
            dialog = DialogInfo(testo=text, showBool=True)
            icona = QtGui.QIcon('./Icons/iconaNote.ico')
            dialog.setWindowIcon(icona)
            dialog.guiText.textBrowser_dialog_info.setText(text)
            if dialog.exec_():
                nuovoTesto = dialog.guiText.textBrowser_dialog_info.toPlainText()
                if nuovoTesto != text:
                    # if not nuovoTesto and text:
                    prenotazione = self.mongo.get_prenotazione_from_date(data)
                    note_doc.note = nuovoTesto
                    self.bot_note.setState(True)
                    if nuovoTesto == '':
                        self.bot_note.setState(False)
                        if data in self.calendario.dateNote:
                            self.calendario.dateNote.remove(data)
                            self.calendario.updateIconsAndBooked()
                        else:
                            print('la data della nota non è nella lista del calendario')
                        note_doc.delete()

                        if prenotazione:
                            prenotazione.note = None
                            prenotazione.save()
                    else:
                        note_doc.save()
                        if prenotazione:
                            prenotazione.note = note_doc
                            prenotazione.save()
                        if data not in self.calendario.dateNote:
                            self.calendario.dateNote = list(set(self.calendario.dateNote))
                            self.calendario.dateNote.append(data)
                    self.calendario.updateIconsAndBooked()
                elif text == '':
                    note_doc.delete()
                    if data in self.calendario.dateNote:
                        self.calendario.dateNote.remove(data)
                        self.calendario.updateIconsAndBooked()
                    else:
                        print('la data della nota non è nella lista del calendario')
        except:
            print(fex())

    @QtCore.pyqtSlot()
    def addSpese(self):
        try:
            data = self.calendario.currentDate
            spesa_mensile = self.mongo.get_spesa_mensile(self.mongo.make_data_ref(data))
            spesa_giornaliera = self.mongo.get_spesa_giornaliera(data, spesa_mensile)

            if not spesa_giornaliera and not spesa_mensile:
                return
            statistiche = self.mongo.get_stat(data=data, data_doc=None, spese_mensili=spesa_mensile, _create=1)
            # spesa_mensile = self.mongo.creat

            spese_dict = spesa_giornaliera.spese
            dialog = DialogSpese(spese_dict)
            dialog.setWindowIcon(QtGui.QIcon('./Icons/iconaSpese.png'))

            # dialog.SPESEPRONTE.connect(lambda x: print('spese pronte', x))
            # dialog.setModal(True)
            if dialog.exec_():
                spese_dict_dialog = dialog.ottieniSpese()
                status_bot = False
                if spese_dict != spese_dict_dialog:
                    if spese_dict_dialog:
                        if spesa_giornaliera:
                            spesa_giornaliera.set_spese(spese_dict_dialog)
                            spesa_mensile.save()
                            status_bot = True
                            statistiche.save()
                        else:
                            print('dfafadfafadfaddddddddddddd')
                            status_bot = False
                    else:
                        if spesa_giornaliera in spesa_mensile.spese_giornaliere:
                            spesa_mensile.spese_giornaliere.remove(spesa_giornaliera)
                            spesa_mensile.save()
                        if not spesa_mensile.spese_giornaliere:
                            spesa_mensile.delete()
                            statistiche.spese_mensili_obj = None
                        statistiche.save()
                else:
                    if not spese_dict:
                        if spesa_giornaliera in spesa_mensile.spese_giornaliere:
                            spesa_mensile.spese_giornaliere.remove(spesa_giornaliera)
                            spesa_mensile.save()
                        if not spesa_mensile.spese_giornaliere:
                            spesa_mensile.delete()
                            statistiche.spese_mensili_obj = None
                        statistiche.save()
                        status_bot = False
                    else:
                        status_bot = True

                self.bot_spese.setState(status_bot)
                if status_bot:
                    if data not in self.calendario.dateSpese:
                        self.calendario.dateSpese.append(data)
                else:
                    if data in self.calendario.dateSpese:
                        self.calendario.dateSpese.remove(data)
                self.calendario.updateIconsAndBooked()
                self.initStatDb()
        except:
            print(fex())

    @QtCore.pyqtSlot()
    def addSpese_old(self):
        try:
            data = self.calendario.currentDate
            spesa_giornaliera = self.mongo.get_spesa_giornaliera(data)
            if spesa_giornaliera:
                spese_dict = {spesa[0]: spesa[1] for spesa in spesa_giornaliera.spese}
            else:
                spese_dict = {}
            dialog = DialogSpese(spese_dict)
            dialog.setWindowIcon(QtGui.QIcon('./Icons/iconaSpese.png'))

            # dialog.SPESEPRONTE.connect(lambda x: print('spese pronte', x))
                # dialog.setModal(True)
            if dialog.exec_():
                spese_dict_dialog = dialog.ottieniSpese()
                status_bot = False
                if spese_dict != spese_dict_dialog:
                    if spesa_giornaliera:
                        status_bot = self.mongo.update_spesa_giornaliera(spesa_giornaliera, spese_dict_dialog)
                    else:
                        status_bot = self.mongo.create_spesa_giornaliera(data, spese_dict_dialog)

                else:
                    if spese_dict:
                        status_bot = True
                self.bot_spese.setState(status_bot)
                if status_bot:
                    if data not in self.calendario.dateSpese:
                        self.calendario.dateSpese.append(data)
                else:
                    if not spese_dict:
                        if data in self.calendario.dateSpese:
                            self.calendario.dateSpese.remove(data)
                self.calendario.updateIconsAndBooked()
        except:
            print(fex())

    def aggiornaInfoData(self):
        data = self.calendario.currentDate
        self.setInfoTemp(self.getInfoFromDate(data))
        if self.infoTemp['data arrivo'] is None:
            self.bot_cancella.setEnabled(False)
        else:
            self.bot_cancella.setEnabled(True)
        self.setDateEdit_dal()

    def botFuncCheckAval(self):
        dal = self.dateEdit_dal.date()
        al = self.dateEdit_al.date()
        # print(self.checkAval(dal, al))

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

    def cancellaprenot(self, wrnMode=True, preserve=False):
        """cancella la prenotazione nella data
            selezionata nel calendario"""
        data = self.calendario.currentDate
        print('cancella prenotazione')
        info = self.infoTemp
        if self.prenotazione_corrente:
        # if not info:
        #     info = self.mongo.info_from_date(data)
        # if info:
        #     print(info == self.infoTemp)
        #     prenotazione = info['prenotazione']
            prenotazione = self.prenotazione_corrente
            # if prenotazione.note:
            #     note_doc = prenotazione.note
            #     note = note_doc
            giorni = prenotazione.giorni.giorni
            if wrnMode:
                if self.warnMsg():
                    note_doc = self.mongo.un_book(prenotazione)
                    self.prenotazione_corrente = None
                else:
                    return
            else:
                note_doc = self.mongo.un_book(prenotazione)
                self.prenotazione_corrente = None
            for giorno in giorni:
                if giorno in self.datePrenotazioni:
                    del self.datePrenotazioni[giorno]
            if note_doc:
                note = note_doc.note
            else:
                note = ''
                if data in self.calendario.dateNote:
                    self.calendario.dateNote.remove(data)
            self.datePulizie.remove(prenotazione.giorno_pulizie)
            info = deepc(self.infoModel)
            info['note'] = note
            self.riempiTabellaPrenotazioni(info)
            self.calendario.setDatesIndicators(self.datePrenotazioni,
                                               self.datePulizie,
                                               self.config['colori settati'], '', '')
            self.calendario.updateIconsAndBooked()
            self.set_status_msg('Cancellazione effettuata')
            self.bot_cancella.setEnabled(False)
            # info = self.mongo.info_from_date(data)
            # self.setInfoTemp(info)
            self.setInfoTemp(self.infoModel)
            if not preserve:
                self.riempi_campi_prenotazioni()
            self.initStatDb()

            return True
        return False

    def checkInfo_line_edit(self):
        # print(type(self.listaWGen))
        listaW = [self.lineEdit_nome, self.lineEdit_cognome, self.lineEdit_telefono]
        for w in listaW:
            if w.text() == '':
                w.setFocus()
                w.selectAll()
                return False

        return True

    def check_note(self, note=None):
        if note:
            # _note_mongo = self.mongo.get_note(self.calendario.currentDate)
            if type(note) is str:
                _note_mongo = note
            else:
                _note_mongo = note.note
            note_mongo =  _note_mongo if _note_mongo else ''
            note_status = True if len(note_mongo) else False
        else:
            note_status = False
        self.bot_note.setState(note_status)
        return note_status

    def check_spese(self, data):
        self.bot_spese.setState(self.mongo.check_spesa(data))

    def cleardisplay(self):
        return os.system('cls')

    def compilaInfo_mongo(self):
        """
        compila il modello (riga  csv ) da salvare a partire dai campi compilati
        :return:
        """
        nome = self.lineEdit_nome.text()
        cognome = self.lineEdit_cognome.text()
        telefono = self.lineEdit_telefono.text()
        email = self.lineEdit_email.text()
        platform = self.combo_platformPrenotazioni.currentText()
        giorni = []
        giorno = self.dateEdit_dal.date()
        while giorno < self.dateEdit_al.date():
            giorni.append(giorno)
            giorno = giorno.addDays(1)
        totale_notti = str(self.dateEdit_dal.date().daysTo(self.dateEdit_al.date()))
        totale_ospiti = self.spinBox_ospiti.value()
        totale_bambini = self.spinBox_bambini.value()

        if self.radio_colazione.isChecked():
            colazione = True
        else:
            colazione = False
        stagione = self.combo_stagionePrenotazioni.currentText()
        importo = float(self.spinBox_importo.value())
        lordo = float(self.lineEdit_lordo.text())
        netto = float(self.lineEdit_netto.text())
        tasse = float(self.lineEdit_tax.text())
        # if self.plainTextEdit_note.toPlainText():
        #         note = 'Note Prenotazione:\n'+self.plainTextEdit_note.toPlainText()
        #         note_doc = self.mongo.create_notes(self.dateEdit_dal.date(), note)
        # else:
        #         note_doc = None
        note_doc = self.mongo.get_note(self.dateEdit_dal.date())
        filtro = 'Note Prenotazione:\n'
        nuove_note = self.plainTextEdit_note.toPlainText()
        if nuove_note:
            note = filtro + nuove_note
            if note_doc:
                if note_doc.note:
                    if filtro not in note_doc.note:
                        note_doc.note += '\n' +note
                    else:
                        note_split = note_doc.note.split(filtro)
                        note_doc.note = note_split[0] + f'\n{note}'
                else:
                    note_doc.note += note
                note_doc.save()
            else:

                note_doc = self.mongo.create_notes(self.dateEdit_dal.date(), note)
            # else:
            #     note_doc = self.mongo.get_note(self.dateEdit_dal.date())
        # else:
        #         note_doc = None
        spese = 0.0
        return nome, cognome, telefono, email, giorni, platform,\
                stagione, totale_ospiti, totale_bambini, colazione, note_doc,\
                importo, lordo, netto, tasse

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

    def get_date(self, d):
        # a = self.calendarWidget.dateTextFormat()
        # self.calendario.set
        # self.setLabel_stagione(d)
        # print('get_date current date ',d)
        # self.current_date = d
        # self.calendario.currentDate = d
        self.current_date = d
        if self.lastMonth != self.current_date.month():
            self.lastMonth = self.current_date.month()
        # print(d.month(),'<<<<',self.calendario.month())
        # print("selection changed", self.current_date_label)

        return self.current_date

    def getInfoFromCalendar(self, data):
        # self.cleardisplay()
        # if self.sender() is not None:
        #     sender = self.sender().objectName()
        #     print(f"{inspect.stack()[0][3]} mandato da {self.sender().objectName()}")
        self.calendario.currentDate = data
        info = self.getInfoFromDate(data)
        if info is None:
            print('info is None from getInfoFromCalendar')
        self.setInfoFromDate(info)
        self.setInfoTemp(info)
        return info
    def set_prenotazione_corrente(self, corrente):
        self.prenotazione_corrente = corrente

    def getInfoFromDate(self, data):
        # self.cleardisplay()
        # print("controllo ", inspect.stack()[0][3])
        if data:
            self.get_date(data)
            # print("data ",self.current_date)
            info = self.mongo.info_from_date(data)
            if info is None:
                info = deepc(self.infoModel)
            self.toggle_button_prenota(info)
            self.toggle_button_cancella(info)
            note = self.mongo.get_note(data)
            if note:
                info['note'] = note.note
            return info
        else:
            return deepc(self.infoModel)

    def importAdj(self):
        totOspiti = self.spinBox_bambini.value() + self.spinBox_ospiti.value()
        maxOspiti = self.config['numero letti']
        if totOspiti >= maxOspiti:
            totOspiti = maxOspiti
        self.spinBox_ospiti.setMaximum(maxOspiti)
        self.spinBox_bambini.setMaximum(maxOspiti - self.spinBox_ospiti.value())
        self.tassa = self.config['tasse']
        self.calcLordoNetto()
        indice = totOspiti - 1 if totOspiti > 0 else 0
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

    def initStatDb(self):
        data = QtCore.QDate(self.calendario.currentYear, self.calendario.currentMonth, 1)
        stat = self.mongo.get_stat(data=data)
        if stat:
            spese = stat['spese_mensili'] + stat['tasse_mensili']
            self.infoSta = Od({'3 Notti': stat['notti_3'],
                               '2 Notti': stat['notti_2'],
                               '1 Notte': stat['notte_1'],
                               'Totale Ospiti': stat['totale_ospiti'],
                               'Netto mensile': stat['netto_mensile'],
                               'Spese mensili': spese})
        else:
            self.infoSta = {}
        self.riempiTabellaStat()

    def initConfig(self):
        # d = DialogOption()
        config = DialogOption.checkConfigFile()
        self.connection_dict = ConnectionDict(host=config['connessione']['host'],
                                                port=config['connessione']['port'],
                                                user=config['connessione']['user'],
                                                password=config['connessione']['password'],
                                                nome_db=config['connessione']['nome_db'])
        return config

    @QtCore.pyqtSlot()
    def lineEditVerifica(self):
        # print('Hola ',self.bot.text())
        # print('ciao ', self.sender().text())
        listaInfo = [self.infoModel['nome'], self.infoModel['cognome'], self.infoModel['telefono']]
        testo = self.sender().text()
        if testo not in listaInfo:
            self.toggle_modificaOsalva(modifica=False)
        else:
            self.toggle_modificaOsalva(modifica=True)
        if not self.sender().selector(testo):
            self.sender().clear()
        else:
            self.sender().nextInFocusChain().setFocus()

    def loadConfig(self):
        self.prepare_tab_prenotazioni()
        self.calendario.setSelectedDate(QtCore.QDate().currentDate())
        self.calendario.dateNote += [nota.data for nota in self.mongo.get_all_note()]
        self.datePrenotazioni, self.datePulizie = self.mongo.get_prenotazioni_pulizie()
        self.dateSpese = self.mongo.get_spese_date()
        self.initStatDb()
        oggi = QtCore.QDate().currentDate()
        info = self.mongo.info_from_date(oggi)
        self.toggle_button_cancella(info)
        if info and info['nome'] != '':
            # self.info_cache[oggi] = deepc(info)
            self.riempiTabellaPrenotazioni(info)
        else:
            if info:
                self.check_note(note=info["prenotazione"].note)
            else:
                self.check_note()
        self.calendario.setDatesIndicators(self.datePrenotazioni, self.datePulizie, self.config['colori settati'],self.dateSpese,'')
        # self.info_cache = deepc(self.datePrenotazioni)
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

    def make_datePrenotazioni_template(self, platforms):
        self.datePrenotazioni =  {plat: {} for plat in platforms}

    def mese_calendario_cambiato(self):
        """seleziona il primo del mese se si cambia la pagina del calendario"""
        self.initStatDb()

    def modificaESalva(self):
        # print({**self.compilaInfo_mongo()})
        if self.prenotazione_corrente:
            if self.cancellaprenot(preserve=True):
                self.salvaInfo()
                self.bot_modifica.setEnabled(False)

            # self.mongo.un_book(self.prenotazione_corrente)
            # nome, cognome, telefono, email, giorni, platform, \
            # stagione, totale_ospiti, totale_bambini, colazione, note_doc, \
            # importo, lordo, netto, tasse = self.compilaInfo_mongo()
            # self.prenotazione_corrente = self.mongo.book(nome=nome,cognome=cognome,telefono=telefono,dates=giorni,platform=platform, stagione=stagione,
            #            totale_ospiti=totale_ospiti, totale_bambini=totale_bambini,colazione=colazione,
            #            importo=importo, lordo=lordo, netto=netto, tasse=tasse, note=note_doc)

    def periodoCambiato(self, p):
        d = self.dateEdit_dal.date()
        a = self.dateEdit_al.date()
        giorni = d.daysTo(a)
        self.lineEdit_numeroGiorni.setText(str(giorni))
        self.calcLordoNetto()

    def riempi_campi_prenotazioni(self):
        """ prende le info da inserire nei campi
            della prenotazione a partire dalle info
            nel box nella pagina
            del calendario"""
        # todo aggiungere segnale alle mylineEdit perché si sblocchi il tasto salva o modifica
        try:
            info = deepc(self.infoTemp)
            if (info['nome'] and info['cognome'] and info['telefono']) == '':
                self.toggle_modificaOsalva()
            else:
                self.toggle_modificaOsalva(modifica=True)
            self.lineEdit_nome.setText(info['nome'])
            self.lineEdit_cognome.setText(info['cognome'])
            self.lineEdit_telefono.setText(info['telefono'])
            self.lineEdit_email.setText(info['email'])
            # numero_ospiti = int(info['numero ospiti']) if info['numero ospiti'] != '' else 0
            self.spinBox_ospiti.setValue(int(info['numero ospiti']) if info['numero ospiti'] != '' else 0)
            self.spinBox_bambini.setValue(int(info['bambini']) if info['bambini'] != '' else 0)
            platform = info['platform']
            if platform != '':
                indiceCombo = self.combo_platformPrenotazioni.findText(platform)
            else:
                indiceCombo = 0
            self.combo_platformPrenotazioni.setCurrentIndex(indiceCombo)
            # try:
            #
            # except:
            #     print(fex())
            self.plainTextEdit_note.clear()
            # try:
            #     infoNote = self.getInfoFromDate(info['data arrivo'])
            # except AttributeError:
            #     infoNote = info
            # self.plainTextEdit_note.insertPlainText(infoNote['note'])
            note = info['note']
            filtro = 'Note Prenotazione:\n'
            if note and filtro in note:
                note = note.split(filtro)[1]
            else:
                note = ''

            self.plainTextEdit_note.insertPlainText(note)
            self.radio_colazione.setChecked(info['colazione'] == 'Si')
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
                self.lineEdit_numeroGiorni.setText(str(info['totale notti']))
            else:
                self.setDateEdit_dal()
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
        nome = info["nome"]
        # if nome == '':
        #     print('nome vuoto')
        #     info = deepc(self.infoModel)
            # for k in info.keys():
            #     info[k] = ''
        cognome = info["cognome"]
        telefono = info["telefono"]
        platform = info["platform"]
        numero_ospiti = info["numero ospiti"]
        bambini = info["bambini"]
        checkIn = info["data arrivo"]
        numeroNotti = info['totale notti']
        note = info['note']
        if type(checkIn) is QtCore.QDate:
            checkIn = info["data arrivo"].toString("ddd dd/MM/yyyy")
        checkOut = info["data partenza"]
        if type(checkOut) is QtCore.QDate:
            checkOut = info["data partenza"].toString("ddd dd/MM/yyyy")

        item = self.tableWidget_info_ospite.item(0, 0)
        item.setText(nome)
        item = self.tableWidget_info_ospite.item(1, 0)
        item.setText(cognome)
        item = self.tableWidget_info_ospite.item(2, 0)
        item.setText(str(numero_ospiti))
        item = self.tableWidget_info_ospite.item(3, 0)
        item.setText(str(bambini))
        item = self.tableWidget_info_ospite.item(4,0)
        item.setText(str(numeroNotti))
        # self.tableWidget_info_ospite.setItem(4, 0, item)
        item = self.tableWidget_info_ospite.item(4, 1)
        item.setText(platform)
        item = self.tableWidget_info_ospite.item(5, 0)
        item.setText(checkIn)
        item = self.tableWidget_info_ospite.item(5, 1)
        item.setText(checkOut)
        self.tableWidget_info_ospite.update()
        # print(f'note --------- {self.mongo.get_note(info["data arrivo"]).note}')
        self.check_note(note)
        self.check_spese(self.calendario.currentDate)
        self.set_prenotazione_corrente(info['prenotazione'])
        # self.modificaESalva()
        return statusBot

    def riempiTabellaStat(self):
        try:

            for row in range(self.tableWidget_stat.rowCount()):
                item_name = self.tableWidget_stat.verticalHeaderItem(row).text()
                text = str(self.infoSta.get(item_name, ''))
                item = self.tableWidget_stat.item(row,0)
                if not item:
                    item = QtWidgets.QTableWidgetItem()
                    self.tableWidget_stat.setItem(row,0,item)
                item.setText(text)
            self.tableWidget_stat.update()
        except KeyError:
            print('riempi stat key err ')

    def prepare_tab_prenotazioni(self):
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_info_ospite.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_info_ospite.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_info_ospite.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_info_ospite.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_info_ospite.setItem(4, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_info_ospite.setItem(4, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_info_ospite.setItem(5, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_info_ospite.setItem(5, 1, item)

    def salvaInfo(self, flag=None):
        if not flag:
            flag = self.checkInfo_line_edit()
        if flag:
            nome, cognome, telefono, email, giorni, platform, \
            stagione, totale_ospiti, totale_bambini, colazione, note, \
            importo, lordo, netto, tasse = self.compilaInfo_mongo()
            try:
                prenotazione = self.mongo.book(nome=nome,cognome=cognome,telefono=telefono,dates=giorni,platform=platform, stagione=stagione,
                       totale_ospiti=totale_ospiti, totale_bambini=totale_bambini,colazione=colazione,
                       importo=importo, lordo=lordo, netto=netto, tasse=tasse, note=note)
                self.datePrenotazioni, self.datePulizie = self.mongo.get_prenotazioni_pulizie()
            except DateExc as e:
                self.set_status_msg(f'Prenotazione non andata a buon fine, {e.message}')
            except OspiteExc as e:
                self.set_status_msg(f'Prenotazione non andata a buon fine, {e.message}')
            except OspiteIllegalName as e:
                self.set_status_msg(f'Prenotazione non andata a buon fine, {e.message}')
            except Exception as e:
                print('Exception', e)
                self.set_status_msg(f'Errore generale, {e}')
                return
            else:
                self.set_status_msg(f'Prenotazione eseguita')
                try:
                    date_note = self.calendario.dateNote
                    if prenotazione.note:
                        # date_note += [self.calendario.currentDate]
                        date_note += [giorni[0]]
                    self.calendario.setDatesIndicators(self.datePrenotazioni, self.datePulizie, self.config['colori settati'],'', date_note)
                    line_edits = [self.lineEdit_nome, self.lineEdit_cognome, self.lineEdit_lordo,
                         self.lineEdit_netto, self.lineEdit_tax, self.lineEdit_telefono,
                         self.plainTextEdit_note]
                    for line_edit in line_edits:
                        line_edit.clear()
                    # self.riempiTabellaPrenotazioni(self.mongo.info_from_date(self.calendario.currentDate))
                    self.riempiTabellaPrenotazioni(self.mongo.get_info_from_prenotazione(prenotazione))
                    self.spinBox_ospiti.setValue(1)
                    self.spinBox_bambini.setValue(0)
                    self.tabWidget.setCurrentIndex(0)
                    self.bot_cancella.setEnabled(True)
                    self.initStatDb()
                    self.set_prenotazione_corrente(prenotazione)
                except :
                    print(fex())

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

    def setInfoFromDate(self, info):
        """compila la tabella dal modello infoTemp"""
        # self.updateInfoStat()
        # self.riempiTabellaStat()
        statusBot = self.riempiTabellaPrenotazioni(info)

    def setInfoTemp(self, info):

        if info is None:
            self.infoTemp = deepc(self.infoModel)
        else:
            self.infoTemp = deepc(info)
        return self.infoTemp

    def setLabel_stagione(self, prenotazione):
        self.label_stagione.setText(prenotazione.stagione)

    def setMenuMain(self):
        optionMenuAction = QtWidgets.QAction(QtGui.QIcon(self.settingsIcon), 'opzioni', self)
        optionMenuAction.setShortcut('Ctrl+O')
        optionMenuAction.setStatusTip('Apre le impostazioni')
        optionMenuAction.triggered.connect(self.dialogOpt)
        self.menuMenu.addAction(optionMenuAction)

    def setProgressbutton(self, bot, status):
        try:
            bot.setActive(status)
        except:
            print(fex)

    def toggle_button_prenota(self, info):
        self.bot_prenota.setText('Prenota')
        if info:
            prenotazione = info.get('prenotazione', None)
            if prenotazione:
                self.bot_prenota.setText('Modifica')

    def toggle_button_cancella(self, info=None):
        self.bot_cancella.setEnabled(False)
        if info:
            prenotazione = info.get('prenotazione', None)
            if prenotazione:
                self.bot_cancella.setEnabled(True)

    def toggle_modificaOsalva(self, modifica=False):
        flagMod = modifica
        flagSalva = not modifica
        self.bot_salva.setEnabled(flagSalva)
        self.bot_modifica.setEnabled(flagMod)

    def totOspitiAdj(self, p):
        self.importAdj()

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
    main = Main()
    # ui = EvInterface()
    # ui.show()
    sys.exit(app.exec_())