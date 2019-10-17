import pickle
import os

from PyQt5 import QtCore, QtWidgets, QtGui
from collections import OrderedDict as Od


class DbMaker(object):
    """ classe che si occupa di creare il file serializzato con pickle come base
        per il database.
        ha un template infomodel per il checkIn e uno infoModelRedux per il checkOut
        la classe fornisce anche un metodo per salvare il database,
        così come per richiamarlo in modalità
        incapsulata, in modo da non sovrascriverlo per sbaglio"""
    INFOMODEL = {
            "nome": "",
            "cognome": "",
            "telefono": None,
        "email": '',
            "platform": "",
            "data arrivo": None,
            "data partenza": None,
        "totale notti": 0,
        "numero ospiti": 0,
            "bambini": 0,
        "spese": '',
        "colazione": 'No',
            "importo": 0,
            "lordo": 0,
            "tasse": 0,
            "netto": 0,
            "note": "",
        }
    INFOMODELREDUX = {"nome": "", "cognome": "", "data partenza": ""}

    def __init__(self, data=None, info=None):
        self.infoModel = self.INFOMODEL.copy()
        self.infoModelRedux = self.INFOMODELREDUX.copy()
        self.infoModel = Od(self.infoModel)
        self.info = info
        self.data = data
        if data is not None:
            self.anno = data.toString("yyyy")
        else:
            self.anno = 2019
        self.listaAnni = [x for x in range(2018, 2029)]
        # print("anno: ",self.anno)
        self.bisestile = bool
        self.bisestileCheck(self.anno)
        self.dataBase = Od()

    def __getitem__(self, item):
        return item

    def bisestileCheck_old(self, anno):
        """controlla che l'anno sia bisestile,
            retorna il dizionario dei mesi corrispondenti"""
        anno = int(anno)
        if anno % 4 == 0 or anno % 100 == 0:
            self.bisestile = True
            numeriGiorni = {
                "gen": 31,
                "feb": 29,
                "mar": 31,
                "apr": 30,
                "mag": 31,
                "giu": 30,
                "lug": 31,
                "ago": 31,
                "set": 30,
                "ott": 31,
                "nov": 30,
                "dic": 31,
            }
        else:
            self.bisestile = False
            numeriGiorni = {
                "gen": 31,
                "feb": 28,
                "mar": 31,
                "apr": 30,
                "mag": 31,
                "giu": 30,
                "lug": 31,
                "ago": 31,
                "set": 30,
                "ott": 31,
                "nov": 30,
                "dic": 31,
            }
        return numeriGiorni

    def bisestileCheck(self, anno):
        """
        controlla che l'anno sia bisestile,
                retorna il dizionario dei mesi corrispondenti
        :param anno:
        :return:
        """
        anno = int(anno)
        giorni = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if anno % 4 == 0 or anno % 100 == 0:
            self.bisestile = True
        else:
            self.bisestile = False
            giorni[1] = 28
        numeriGiorni = {x: v for x, v in zip(range(1, 13), giorni)}

        return numeriGiorni

    def setData(self, d):
        """setta la data in formato Pqt5.QtCore.QDate"""
        self.data = d
        return self.data

    def stampa(self):
        """funzione che stampa la data"""
        print("data: ", self.data)

    def makeDataBase(self, info=None):
        database = Od()
        for anno in self.listaAnni:
            database[anno] = Od()
            numeroGiorni = self.bisestileCheck(anno)
            for k in numeroGiorni.keys():
                database[anno][k] = Od()
                for v in range(1, numeroGiorni[k] + 1):
                    database[anno][k][v] = Od()
                    database[anno][k][v]["checkIn"] = self.infoModel
                    database[anno][k][v]["checkOut"] = self.infoModelRedux
        return database

    def makeDataBase_old(self, anno=None, info=None):
        """ crea il database da zero"""
        if anno is None:
            if type(self.anno) is int:
                anno = self.anno
            else:
                anno = int(self.anno)
            database = Od()
            database[anno] = Od()

            numeroGiorni = self.bisestileCheck(self.anno)
            for k in numeroGiorni.keys():
                database[anno][k] = Od()
                for v in range(1, numeroGiorni[k] + 1):
                    # database[nome][k][v] = Od()
                    database[anno][k][v] = Od()
                    if info is None:
                        database[anno][k][v]["checkIn"] = self.infoModel
                        database[anno][k][v]["checkOut"] = self.infoModelRedux
                    else:
                        database[anno][k][v]["checkIn"] = info
                        database[anno][k][v]["checkOut"] = self.infoModelRedux
        else:
            if type(anno) is not int:

                # nomeFile = anno + ".pkl"
                anno = int(anno)
                database = Od()
                database[anno] = Od()
            else:

                # nomeFile = str(anno) + ".pkl"
                database = Od()
                database[anno] = Od()

            numeroGiorni = self.bisestileCheck(anno)
            for k in numeroGiorni.keys():
                database[anno][k] = Od()
                for v in range(1, numeroGiorni[k] + 1):
                    database[anno][k][v] = Od()
                    if info is None:
                        database[anno][k][v]["checkIn"] = self.infoModel
                        database[anno][k][v]["checkOut"] = self.infoModelRedux
                    else:

                        # c = info.copy()
                        database[anno][k][v]["checkOut"] = Od()
                        database[anno][k][v]["checkOut"]["nome"] = database[anno][k][v][
                            "checkIn"
                        ]["nome"]
                        database[anno][k][v]["checkOut"]["cognome"] = database[anno][k][
                            v
                        ]["checkIn"]["cognome"]
                        database[anno][k][v]["checkOut"]["data partenza"] = database[
                            anno
                        ][k][v]["checkIn"]["data partenza"]
        # print("database creato",database)
        return database

    def checkFile(self, shortcut=''):

        nome = 'database.pkl'
        try:
            # print(os.getcwd())
            with open(nome, "rb") as f:
                fileDb = pickle.load(f)
        except FileNotFoundError:
            print("creo il database")
            fileDb = self.makeDataBase()
            with open(nome, "wb") as f:
                pickle.dump(fileDb, f)
        return fileDb

    def checkFile_old(self, anno, info=None, shortcut=''):
        """ controlla che il file del database
            esista per l'anno indicato come arg"""
        if shortcut != '':
            nome = '../' + str(anno) + ".pkl"
        else:
            if type(anno) is not str:
                nome = str(anno) + ".pkl"
            else:
                nome = anno + ".pkl"
        try:
            with open(nome, "rb") as f:
                fileDb = pickle.load(f)
        except FileNotFoundError:
            print("creo il database")
            fileDb = self.makeDataBase(anno)
            with open(nome, "wb") as f:
                pickle.dump(fileDb, f)
        return fileDb

    def salvaDatabase(self, fileDb, shortcut=''):
        """ salva il database per l'anno indicato"""
        print("sequenza di salvataggio iniziata")
        if shortcut != '':
            nome = '../database.pkl'
        else:
            nome = 'database.pkl'
        with open(nome, "wb") as f:
            pickle.dump(fileDb, f)
        print("salvataggio effettuato in: ", nome)

    def salvaDatabase_old(self, anno, fileDb, shortcut=0):
        """ salva il database per l'anno indicato"""
        print("sequenza di salvataggio iniziata")
        if type(anno) is not str:
            anno = str(anno)
        if shortcut:
            nome = '../' + anno + ".pkl"
        else:
            nome = anno + ".pkl"
        with open(nome, "wb") as f:
            pickle.dump(fileDb, f)
        print("salvataggio effettuato in: ", nome)
