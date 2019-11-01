import csv
import os
import traceback
import shutil
from copy import deepcopy
from PyQt5 import QtCore
from collections import OrderedDict as Od
import filecmp

class ExpCsv(object):
    """
    classe per esportare il dizionario di EvInterface
    """

    def __init__(self, database, anno=None, shortcut=0):
        self._database = deepcopy(self.adjDb(database))
        self.listak_esclusiRipetizione = ['nome', 'cognome', 'colazione', 'platform']
        # self.listaColonne = self.build_listaColonne_old()
        self.listaColonne = []
        self._anno = anno
        self.shortcut = shortcut
        if self.shortcut:
            self.prefix = '../'
        else:
            self.prefix = ''
        self._nomeFile = self.prefix + str(anno) + '.csv'

    def adjDb(self, _db):
        db = deepcopy(_db)
        for anno in db.keys():
            for mese in db[anno]:
                for giorno in db[anno][mese]:
                    chekIn = deepcopy(db[anno][mese][giorno]['checkIn'])
                    dataArrivo = db[anno][mese][giorno]['checkIn']['data arrivo']
                    dataPartenza = db[anno][mese][giorno]['checkIn']['data partenza']
                    if (dataArrivo or dataPartenza) is not None:
                        chekIn['data arrivo'] = dataArrivo.toString("dd MMM yyyy")
                        chekIn['data partenza'] = dataPartenza.toString("dd MMM yyyy")
                    db[anno][mese][giorno] = deepcopy(chekIn)
        return db

    def build_listaColonne(self, d):
        li = []
        for k in d.keys():
            if k not in li:
                li.append(k)
        return li

    def anno(self, a=None):
        if a is None:
            a = self._anno
        else:
            self._anno = a
        return a

    def setListaK(self, k):
        """
        metodo per fare in modo che il valore
        venga ripetuto nelle righe del csv
        :param k:
        :return:
        """
        if k not in self.listak_esclusiRipetizione:
            self.listak_esclusiRipetizione.append(k)

    def updateDiz(self):

        def getNames(a, m, g):
            form = QtCore.QDate
            mese_data = form(a, m, g).toString("MMM")
            giorno_data = form(a, m, g).toString("dd/MM/yyyy")
            giorno_nome = form(a, m, g).toString("ddd dd")
            return mese_data, giorno_data, giorno_nome

        def getItem(a, m, g, k, database):
            item = database[a][m][g][k]
            return item

        db = deepcopy(self._database)
        listaDiz = Od()
        updated = Od()
        vecchioNome = 'n'
        vecchioCognome = 'c'
        listaV = []
        nuovaPrenotazione = bool
        for anno in db.keys():
            listaV.clear()
            updated[anno] = Od()
            diz = Od()
            for mese in db[anno]:
                dizzy = Od()
                ieri = 1
                listaV.clear()
                for giorno in db[anno][mese]:

                    listaNomi_oggi = getNames(anno, mese, giorno)
                    giorno_data = listaNomi_oggi[1]
                    mese_data = listaNomi_oggi[0]
                    giorno_nome = listaNomi_oggi[2]
                    dizzy[giorno_data] = Od()
                    diz = dizzy[giorno_data]
                    dizzy[giorno_data]['mese'] = mese_data
                    dizzy[giorno_data]['giorno'] = giorno_nome
                    listak = [x for x in db[anno][mese][giorno].keys() if x not in self.listak_esclusiRipetizione]
                    nomeCheck = db[anno][mese][giorno]['nome']
                    cognomeCheck = db[anno][mese][giorno]['cognome']
                    nomeCognomecheck = nomeCheck + cognomeCheck
                    # if  nomeCheck != vecchioNome or cognomeCheck != vecchioCognome:
                    if nomeCognomecheck != (vecchioNome + vecchioNome):
                        nuovaPrenotazione = True
                    else:
                        listaV.clear()
                        nuovaPrenotazione = False
                    for k in db[anno][mese][giorno].keys():
                        item = getItem(anno, mese, giorno, k, db)
                        dato = db[anno][mese][giorno][k]
                        if k == 'nome':
                            if vecchioNome != item and (vecchioNome != '' or vecchioNome != '*'):
                                vecchioNome = item[:]
                        elif k == 'cognome':
                            if vecchioCognome != item and (vecchioCognome != '' or vecchioCognome != '*'):
                                vecchioCognome = item[:]
                        else:
                            if nuovaPrenotazione:
                                if k in listak:
                                    if ('nome' and 'cognome') in db[anno][mese][giorno]:

                                        nome = db[anno][mese][giorno]['nome']
                                        cognome = db[anno][mese][giorno]['cognome']
                                        nuovoItem = db[anno][mese][giorno][k]
                                        if (nome and cognome) not in ['', '*']:
                                            if vecchioNome == nome and vecchioCognome == cognome:
                                                # if vecchioItem != item
                                                if item not in listaV:
                                                    listaV.append(item)
                                                    dato = db[anno][mese][giorno][k]
                                                else:
                                                    dato = '*'
                                            else:
                                                listaV.clear()
                                                listaV.append(item)
                                                dato = db[anno][mese][giorno][k]
                                        else:
                                            dato = db[anno][mese][giorno][k]
                                    else:
                                        dato = db[anno][mese][giorno][k]
                                else:
                                    dato = db[anno][mese][giorno][k]
                            else:
                                nuovaPrenotazione = False
                        dizzy[giorno_data][k] = dato
                    if giorno_data not in listaDiz:
                        listaDiz[giorno_data] = dizzy
                    else:
                        print("diz già presente\n\t", diz.items())
                updated[anno][mese] = deepcopy(dizzy)
            lik = [x for x in diz.keys()]
            lik.insert(0, 'data')
            if self.listaColonne != lik:
                self.listaColonne = lik
        return updated

    def getNomeCsv(self, anno, mese):
        anno = str(anno)
        nomeFile = './csv/' + anno + '/' + mese + '.csv'
        return nomeFile

    def getNomeCsv_old(self, anno, mese):
        nomeFile = './csv/' + str(anno) + mese + '.csv'
        return nomeFile

    def makeCsv(self):
        li = self.updateDiz()
        db = deepcopy(self._database)

        def form(anno, mese):
            _form = QtCore.QDate(anno, mese, 1).toString("MMM")
            return _form

        for anno in li.keys():
            # print("li.keys: ",anno)
            # for anno in db:
            for mese in db[anno].keys():
                nomeFile = self.getNomeCsv(anno, form(anno, mese))
            # nomeFile = str(self.anno()) + "_" + form(m) + ".csv"
                self.checkFile(nomeFile, li[anno][mese])

    def writeCsv(self, nomeFile, diz):
        li = [x for x in diz.keys()]
        vi = []
        for k in li:
            val = [diz[k][p] for p in diz[k].keys()]
            val.insert(0, k)
            vi.append(val)
        with open(nomeFile, 'wt', newline='') as csv_db:
            w = csv.writer(csv_db, quoting=csv.QUOTE_NONNUMERIC)
            w.writerow(self.listaColonne)
            for k in vi:
                w.writerow(k)

    def checkFile(self, nomeFile, diz, temp=None):
        nomeTemporaneo = './csv/temp.csv'
        try:
            if temp is None:
                self.writeCsv(nomeTemporaneo, diz)
            if not filecmp.cmp(nomeTemporaneo, nomeFile):
                shutil.copyfile(nomeTemporaneo, nomeFile)
        except FileNotFoundError:
            self.writeCsv(nomeFile, diz)
            self.checkFile(nomeFile, diz, temp=1)
        finally:
            try:
                os.remove(nomeTemporaneo)
            except FileNotFoundError:
                pass
            return True
