"""
modulo che implementa la cancellazione delle prenotazioni
prodotte dal primo script, ricercando le date occupate e
aggiornando i files
"""
from PyQt5 import QtGui, QtCore, QtWidgets
from tools.databaseMaker import DbMaker as dbm
from copy import deepcopy as deepc
from collections import OrderedDict as Od
import pickle


class ManagerPreno(object):
    """
    classe per la cancellazione delle prenotazioni fatte dal primo
    scrip, ricercando le date occupate e
    aggiornando i files
    """

    def __init__(self, info=None, shortcut=0):

        # self._dataIn = dataIn
        # self._domani = dataIn.addDays(1)
        # self._nome = nome
        # self._cognome = cognome

        # opzione per correggere il percorso durante i tests
        self.shortcut = shortcut
        self._info = info
        # if self._info is not None:
        try:
            self.info = self.getInfo
            self._dataIn = self.info['data arrivo']
            self._dataOut = self.info['data partenza']
            self._domani = self._dataIn.addDays(1)
            self._nome = self.info['nome']
            self._cognome = self.info['cognome']
        except AttributeError or TypeError:
            # else:
            self._dataIn = QtCore.QDate().currentDate()
            self._domani = self._dataIn.addDays(1)
            self._dataOut = self._domani
            self._nome = None
            self._cognome = None
        self.occupate = []
        self.DataBase = deepc(self.getDb(self._dataIn))
        print("cosa è DataBAse ", type(self.DataBase))
        self.counter = 0
        # self.DataBase = Od()
        self.dateBooking = []
        self.dateAirbb = []
        self.datePrivati = []
        self.datePulizie = []
        self.platformDict = {
            'booking': self.dateBooking,
            'airbb': self.dateAirbb,
            'privati': self.datePrivati,
            'pulizie': self.datePulizie
        }
        # self.platformDict = Od(platformDict)

    def checkAval(self, dal, al):
        """
        controlla la disponibilità delle prenotazioni
        nell'intervallo delle date fornite
        :param dal:
        :param al:
        :return: list
        """
        giorniPermanenza = dal.daysTo(al)
        print("giorni di permanenza: ", giorniPermanenza)
        arrivo = dal
        partenza = al
        database = deepc(self.DataBase)
        aval = True
        listaDisponibili = []
        oggi = arrivo
        while oggi < partenza:
            a, m, g = self.amg(oggi)
            nome = database[a][m][g]['checkIn']['nome']
            if nome != '':
                aval = False
                print(
                    "spiacente, casa non disponibile in questa data",
                    oggi.toString("dd MMM yyyy"),
                )
            else:
                listaDisponibili.append(oggi)
            oggi = oggi.addDays(1)

        if giorniPermanenza == len(listaDisponibili):
            print("casa libera  tutti i giorni disponibili")
        else:
            print(" casa libera nei giorni:\n")
            # todo ripristinare la funzionalità qui sotto
            # if len(listaDisponibili) > 0:
            #     self.dateEdit_dal.setDate(listaDisponibili[0])
            #     self.dateEdit_dal.update()
            #     for d in listaDisponibili:
            #         print(d)
            # cancellare quella qui sotto
            if len(listaDisponibili) > 0:
                for d in listaDisponibili:
                    print(d.toString("dd MMM yyyy"))
            else:
                print("nessuna data disponibile")

        return listaDisponibili

    def setPlatformDict(self):
        self.platformDict

    def platformPulizie(self):
        # todo evitare di caricare le date passate?
        self.dateBooking.clear()
        self.dateAirbb.clear()
        self.datePrivati.clear()
        self.datePulizie.clear()
        a, m, g = self.amg(self._dataIn)
        partenza = self.DataBase[a][m][g]["checkIn"]['data partenza']
        for anno in self.DataBase.keys():
            for mese in self.DataBase[anno].keys():
                for giorno in self.DataBase[anno][mese].keys():
                    data = QtCore.QDate(anno, mese, giorno)
                    plat = self.DataBase[anno][mese][giorno]["checkIn"]["platform"]
                    pulizie = self.DataBase[anno][mese][giorno]["checkOut"]['data partenza']
                    if plat == "Booking.com":
                        if data not in self.dateBooking:
                            self.dateBooking.append(data)
                    elif plat == "airBB":
                        if data not in self.dateAirbb:
                            self.dateAirbb.append(data)
                    elif plat == 'privato':
                        if data not in self.datePrivati:
                            self.datePrivati.append(data)
                    if pulizie != '':
                        if pulizie not in self.datePulizie:
                            self.datePulizie.append(pulizie)

        return self.dateBooking, self.dateAirbb, self.datePrivati, self.datePulizie

    def canc(self):
        """
        cancella la prenotazione dal database virtuale
        :return:
        """
        if self._dataIn is not None:
            self.freethem()
        else:
            print("fornire un info model")

    def controlloNome(self, nome='nome'):
        """ funzione di verifica e debug
        controlla che il nome passato sia ancora presente nel database
        """
        nomepresente = False
        cognomepresente = False
        for m in self.DataBase[2019].keys():
            for g in self.DataBase[2019][m].keys():
                try:
                    if nome == 'nome':
                        if self.DataBase[2019][m][g]['checkIn']['nome'] == self._nome:
                            nomepresente = True
                    else:
                        if self.DataBase[2019][m][g]['checkOut']['nome'] == self._nome:
                            cognomepresente = True
                except:
                    print("eccezione controllo nome giorno :", g)
                # print("ecci g",g)
                # for n in self.DataBase[2019][m][g]['checkIn'].keys():

        if nomepresente or cognomepresente:
            print("NOME ANCORA PRESENTE ", self._nome)
            return False
        else:
            print("NOME non trovato ", self._nome)
        print("hai controllato il nome e la data di checkin??")
        return True

    def buildInfoRed(self):

        info = {'nome': self._nome, 'cognome': self._cognome, 'data partenza': self._dataOut}
        return info

    def setThem(self):
        """
        crea una prenotazione e la salva su disco
        :return:
        """
        database = deepc(self.DataBase)
        data = self.getData()
        if data is None:
            print("fornire un info model - freethem")
            return
        while data < self._dataOut:
            a, m, g = self.amg(data)
            database[a][m][g]['checkIn'] = self._info
            data = data.addDays(1)
            if data == self._dataOut:
                print("giorno stabilito")
                infoRedux = self.buildInfoRed()
                a1, m2, g3 = self.amg(data)
                database[a1][m2][g3]['checkOut'] = deepc(infoRedux)
                break
        self.DataBase = deepc(database)
        self.salvaDatabase()

    def salvaDatabase(self):
        """"salva il database su disco
        """
        database = dbm(self._dataIn)
        if self.shortcut:
            database.salvaDatabase(self._dataIn.year(), self.DataBase, shortcut=1)
        else:
            database.salvaDatabase(self._dataIn.year(), self.DataBase)

    def freethem(self):
        """
        cancella di fatto la prenotazione posta in info
        :return:
        """
        try:
            self.controlloNome()
            data = self.getData()
            if data is None:
                print("fornire un info model - freethem")
                return
            flag = True
            while flag:
                checkIn, checkOut, nome, cognome = self.findDate(self.DataBase, data)
                if (checkIn['nome'] == self._nome or checkIn['cognome'] == self._cognome) and checkIn[
                    'data arrivo'] == self._dataIn:
                    checkIn = dbm.INFOMODEL.copy()
                    checkOut = dbm.INFOMODELREDUX.copy()
                    a, m, g = self.amg(data)
                    self.DataBase[a][m][g]['checkIn'] = checkIn
                    # if self.DataBase[a][m][g]['checkOut']['data partenza'] != '':
                    #     self.DataBase[a][m][g]['checkOut'] = checkOut
                    print("checkin copiato")
                    data = data.addDays(1)
                    a, m, g = self.amg(data)
                    if self.DataBase[a][m][g]['checkOut']['data partenza'] != '':
                        self.DataBase[a][m][g]['checkOut'] = checkOut
                    else:
                        print(self.DataBase[a][m][g]['checkOut']['data partenza'] + ' ', g)
                else:
                    flag = False
                    break

            self.salvaDatabase()
        except:
            import traceback
            print(traceback.format_exc())

    def findDate(self, db, datacheckin):
        a, m, g = self.amg(datacheckin)
        checkIn, checkOut = self.getCheckInOut(db, a, m, g)
        nome = self.getDbNominativo(db, datacheckin, 'nome')
        cognome = self.getDbNominativo(db, datacheckin, 'cognome')
        return checkIn, checkOut, nome, cognome

    def getCheckInOut(self, database, a, m, g):
        """
                restituisce chiave check in e out
                dal database
                :return:
                """
        checkIn = database[a][m][g]['checkIn']
        checkOut = database[a][m][g]['checkOut']

        return checkIn, checkOut

    @property
    def getInfo(self):
        """
        ritorna le informazioni
        :return:
        """
        i = self._info
        return i

    @property
    def getName(self):
        """
        ritorna il nome di chi ha prenotato
        :return:
        """
        self.nome = self._nome
        return self.nome

    @property
    def getSurname(self):
        """
        ritorna il cognome di chi ha prenotato
        :return:
        """
        self.cognome = self._cognome
        return self.cognome

    def getData(self):
        data = self._dataIn
        return data

    def getDbNominativo(self, db, data, modo=None):

        a, m, g = self.amg(data)
        # print("controllo amg ",a, m, g)
        try:
            if modo == 'nome':
                # print("controllo db[a][m][g]['checkIn']['nome'] ",

                _nome = db[a][m][g]['checkIn']['nome']
                return _nome
            elif modo == 'cognome':
                _cognome = db[a][m][g]['checkIn']['cognome']
                return _cognome
        except:
            import traceback
            print(traceback.format_exc())

    def getDb(self, data):
        """
        accede al database
        :param anno:
        :return: database
        """
        if data is None:
            print("fornire un info model ---- getDb")
            return
        a, m, g = self.amg(self._dataIn)
        if self.shortcut:
            database = dbm(data).checkFile(a, shortcut='1')
        else:
            database = dbm(data).checkFile(a)
        # print("prova ",database.anno)
        return database

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


if __name__ == '__main__':
    dal = QtCore.QDate(2019, 10, 21)
    # al = dal.addDays(3)
    al = QtCore.QDate(2019, 10, 27)
    d = {
        "nome": "franco",
        "cognome": "franchi",
        "telefono": None,
        "platform": "",
        "data arrivo": dal,
        "data partenza": al,
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
    app = ManagerPreno(info=d, shortcut=1)
    app.checkAval(dal, al)
    app.canc()
