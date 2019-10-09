import pickle
from PyQt5 import QtCore, QtWidgets, QtGui
from collections import OrderedDict as Od


class DbMaker(object):
    """ classe che si occupa di creare il file serializzato con pickle come base per il database
        ha un template infomodel per il checkIn e uno infoModelRedux per il checkOut
        la classe fornisce anche un metodo per salvare il database, così come per richiamarlo in modalità
        incapsulata, in modo da non sovrascriverlo per sbaglio"""
    def __init__(self,data,info=None):
        self.infoModel = {"nome": "", "cognome": "", "telefono": None, "platform": "", "data arrivo": None,
                          "data partenza": None,
                          "numero ospiti": 1, "bambini": 0, "spese": {}, "colazione": False, "importo": 0, "lordo": 0,
                          "tasse": 0, "netto": 0, "note": ""}
        self.infoModelRedux = {"nome":'',"cognome":'',"data partenza":''}
        self.infoModel = Od(self.infoModel)
        self.info = info
        self.data = data
        self.anno = data.toString('yyyy')
        # print("anno: ",self.anno)
        self.bisestile = bool
        self.bisestileCheck(self.anno)
        self.dataBase = Od()

    def bisestileCheck(self,anno):
        """controlla che l'anno sia bisestile,
            retorna il dizionario dei mesi corrispondenti"""
        anno = int(anno)
        if anno % 4 == 0 or anno % 100 == 0:
            self.bisestile = True
            numeriGiorni = {"gen": 31, "feb": 29, "mar": 31, "apr": 30, "mag": 31, "giu": 30,
                            "lug": 31, "ago": 31, "set": 30, "ott": 31, "nov": 30, "dic": 31}
        else:
            self.bisestile = False
            numeriGiorni = {"gen": 31, "feb": 28, "mar": 31, "apr": 30, "mag": 31, "giu": 30,
                            "lug": 31, "ago": 31, "set": 30, "ott": 31, "nov": 30, "dic": 31}
        return numeriGiorni

    def setData(self,d):
        """setta la data in formato Pqt5.QtCore.QDate"""
        self.data = d
        return self.data

    def stampa(self):
        """funzione che stampa la data"""
        print("data: ", self.data)

    def makeDataBase(self,anno=None,info=None):
        """ crea il database da zero"""
        if  anno is None:
            if type(self.anno) is not int:
                nome = self.anno
                nomeFile = self.anno + ".pkl"
                database = Od()
                database[nome] = Od()
                anno = int(self.anno)
            else:
                nome = str(self.anno)
                nomeFile = str(self.anno) + ".pkl"
                database = Od()
                database[nome] = Od()

            numeroGiorni = self.bisestileCheck(self.anno)
            for k in numeroGiorni.keys():
                database[nome][k] = Od()
                for v in range(1,numeroGiorni[k]+1):
                    # database[nome][k][v] = Od()
                    database[nome][k][v] = Od()
                    if info is None:

                        database[nome][k][v]['checkIn'] = self.infoModel
                        database[nome][k][v]['checkOut'] = self.infoModelRedux
                    else:
                        database[nome][k][v]['checkIn'] = info
                        database[nome][k][v]['checkOut'] = self.infoModelRedux
        else:
            if type(anno) is not int:
                nome = anno
                nomeFile = anno + ".pkl"
                database = Od()
                database[nome] = Od()
                anno = int(anno)
            else:
                nome = str(anno)
                nomeFile = str(anno) + ".pkl"
                database = Od()
                database[nome] = Od()

            numeroGiorni = self.bisestileCheck(anno)
            for k in numeroGiorni.keys():
                database[nome][k] = Od()
                for v in range(1, numeroGiorni[k] + 1):
                    database[nome][k][v] = Od()
                    if info is None:
                        database[nome][k][v]['checkIn'] = self.infoModel
                        database[nome][k][v]['checkOut'] = self.infoModelRedux
                    else:

                        c = info.copy()
                        database[nome][k][v]['checkOut'] = Od()
                        database[nome][k][v]['checkOut']['nome'] = database[nome][k][v]['checkIn']['nome']
                        database[nome][k][v]['checkOut']['cognome'] = database[nome][k][v]['checkIn']['cognome']
                        database[nome][k][v]['checkOut']['data partenza'] = database[nome][k][v]['checkIn']['data partenza']

        return database


        # for m,n in numeroGiorni.items():
        #     print(m, " ", n)

    def checkFile(self,anno,info=None):
        """ controlla che il file del database esista per l'anno indicato come arg"""
        if type(anno) is not int:
            nome=anno+".pkl"
        else:
            nome =str(anno) +".pkl"
        try:
            with open(nome,"rb") as f:
                fileDb = pickle.load(f)
        except FileNotFoundError:
            print("creo il database")
            fileDb = self.makeDataBase(anno)
            with open(nome, "wb") as f:
                pickle.dump(fileDb,f)
        return fileDb



    def salvaDatabase(self,anno,fileDb):
        """ salva il database per l'anno indicato"""
        if type(anno) is not str:
            anno = str(anno)
        nome = anno + ".pkl"
        with open(nome, "wb") as f:
            pickle.dump(fileDb, f)
        print("salvataggio effettuato in: ",nome)

