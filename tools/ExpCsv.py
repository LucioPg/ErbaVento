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

    def __init__(self, database, anno, shortcut=0):

        # self.listaColonne = ['anno',
        #                      'mese',
        #                      'giorno',
        #                      'nome',
        #                      'cognome',
        #                      'telefono'
        #                      'arrivo',
        #                      'partenza',
        #                      'numero ospiti',
        #                      'bambini',
        #                      'lordo',
        #                      'netto',
        #                      'tasse',
        #                      'piattaforma']
        self._database = deepcopy(self.adjDb(database))

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

    def updateDiz(self):
        a = self.anno()
        db = deepcopy(self._database)
        form = QtCore.QDate
        listaDiz = []
        for anno in db.keys():
            for mese in db[anno]:
                dizzy = Od()
                for giorno in db[anno][mese]:
                    mese_data = form(anno, mese, giorno).toString("MMM")
                    giorno_data = form(anno, mese, giorno).toString("dd/MM/yyyy")
                    giorno_nome = form(anno, mese, giorno).toString("ddd dd")
                    dizzy[giorno_data] = Od()
                    diz = dizzy[giorno_data]
                    dizzy[giorno_data]['mese'] = mese_data
                    dizzy[giorno_data]['giorno'] = giorno_nome
                    for k in db[anno][mese][giorno].keys():
                        dizzy[giorno_data][k] = db[anno][mese][giorno][k]

                if diz not in listaDiz:
                    listaDiz.append(dizzy)
            lik = [x for x in diz.keys()]
            lik.insert(0, 'data')
            if self.listaColonne != lik:
                self.listaColonne = lik
        return listaDiz

    def getNomeCsv(self, anno, mese):
        nomeFile = './csv/' + str(anno) + mese + '.csv'
        return nomeFile

    def makeCsv(self):
        li = self.updateDiz()

        def form(mese):
            _form = QtCore.QDate(2019, mese + 1, 1).toString("MMM")
            return _form

        for m in range(len(li)):
            nomeFile = self.getNomeCsv(self.anno(), form(m))
            # nomeFile = str(self.anno()) + "_" + form(m) + ".csv"
            self.checkFile(nomeFile, li[m])

    def writeCsv(self, nomeFile, diz):
        newDict = Od()
        li = [x for x in diz.keys()]
        vi = []
        finale = li[:]
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
            print("££££££££££££££££££££")
            print(f"csv non presente {nomeFile}, procedo alla creazione")
            self.writeCsv(nomeFile, diz)
            self.checkFile(nomeFile, diz, temp=1)
        # else:
        #     print("**********************")
        #     print(traceback.format_exc())
        #     return False
        finally:
            try:
                os.remove(nomeTemporaneo)
            except FileNotFoundError:
                pass
            else:
                pass
                # print(traceback.format_exc())
            return True
