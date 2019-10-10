"""
modulo che implementa la cancellazione delle prenotazioni
prodotte dal primo script, ricercando le date occupate e
aggiornando i files
"""
from PyQt5 import QtGui, QtCore, QtWidgets
from tools.databaseMaker import DbMaker as dbm
from collections import OrderedDict as Od
import pickle


class ManagePreno(object):
    """
    classe per la cancellazione delle prenotazioni fatte dal primo
    scrip, ricercando le date occupate e
    aggiornando i files
    """

    def __init__(self, dataIn=QtCore.QDate, nome=None, cognome=None, info=None):

        self._dataIn = dataIn
        self._domani = dataIn.addDays(1)
        self._nome = nome
        self._cognome = cognome
        self._info = info
        self.occupate = []
        self.DataBase = Od()

    def canc(self):
        """
        cancella la prenotazione dal database virtuale
        :return:
        """
        if (self._nome or self._cognome) is not None:
            self.DataBase = self.getDb(self._dataIn)
            # self.findDate(self.DataBase,self._dataIn)
            self.freethem()
        else:
            raise Exception("sono necessari il nome e il cognome")

    def controlloNome(self):
        presente = False
        for m in self.DataBase[2019].keys():
            for g in self.DataBase[2019][m].keys():
                try:
                    if self.DataBase[2019][m][g]['checkIn']['nome'] == self._nome:
                        presente = True
                        print(g)
                except:
                    print("ecco n", g)
                # print("ecci g",g)
                # for n in self.DataBase[2019][m][g]['checkIn'].keys():

        if presente:
            print("NOME ANCORA PRESENTE ", self._nome)
        else:
            print("NOME non trovato ", self._nome)
        print("hai controllato il nome e la data di checkin??")

    def freethem(self):

        try:
            self.controlloNome()
            print()
            data = self.getData()
            flag = True
            while flag:
                checkIn, checkOut, nome, cognome = self.findDate(self.DataBase, data)
                if (checkIn['nome'] == self._nome or checkIn['cognome'] == self._cognome) and checkIn[
                    'data arrivo'] == self._dataIn:
                    checkIn = dbm.INFOMODEL.copy()
                    checkOut = dbm.INFOMODELREDUX.copy()
                    a, m, g = self.amg(data)
                    self.DataBase[a][m][g]['checkIn'] = checkIn
                    self.DataBase[a][m][g]['checkOut'] = checkOut
                    print("checkin copiato")
                    data = data.addDays(1)
                else:
                    print("*@#! ", checkIn['nome'])
                    flag = False
                    break
            self.controlloNome()
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
        self.info = self._info
        return self.info

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
        a, m, g = self.amg(self._dataIn)
        database = dbm(data).checkFile(a, shortcut='1')
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
    fadfa = QtCore.QDate(2019, 10, 11)
    app = ManagePreno(dataIn=fadfa, nome='peppea')
    app.canc()
