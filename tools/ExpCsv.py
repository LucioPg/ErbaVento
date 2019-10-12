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
        self.listak = ['nome', 'cognome', 'colazione']
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
        if k not in self.listak:
            self.listak.append(k)

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
                    # print("giorno data ",giorno_data)
                    dizzy[giorno_data]['mese'] = mese_data
                    dizzy[giorno_data]['giorno'] = giorno_nome
                    listak = [x for x in db[anno][mese][giorno].keys() if x not in self.listak]
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
                                                if nome == 'franco' and giorno == 3:
                                                    print("franco!", item)
                                                    print(listaV)
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
                        dizzy[giorno_data][k] = dato
                    if giorno_data not in listaDiz:
                        listaDiz[giorno_data] = dizzy
                    else:
                        print("diz già presente\n\t", diz.items())
                updated[anno][mese] = deepcopy(dizzy)
            lik = [x for x in diz.keys()]
            # listaCol = listak[:]
            # for x in range(len(self.listak)):
            #     item = self.listak[x]
            #     if item not in listaCol:
            #         listaCol.insert(x,item)
            # if lik == listaCol:
            #     print("listaK è come lik? si")
            # else:
            #     print(f"lik = {len(lik)}\t\t\tlistak= {len(listaCol)}")
            #
            #     def ottieni(lista,x):
            #         try:
            #             val = lista[x]
            #         except IndexError:
            #             val = None
            #         return val
            #     for x in range(max(len(lik),len(listaCol))):
            #         z = ottieni(lik,x)
            #         y = ottieni(listaCol,x)
            #         print(f"{x}#   lik= {z}\t\t\tlistak= {y}")
            #     for el in lik:
            #         if el not in listaCol:
            #             print(el)
            # clear = os.system('cls')
            # clear()
            #

            lik.insert(0, 'data')
            if self.listaColonne != lik:
                self.listaColonne = lik

        # for d in listaDiz:
        #     print(d.keys())
        print("len listaDiz", len(listaDiz))
        # print("dizzy \n\t\t",dizzy.items())
        # return listaDiz
        return updated

    def updateDiz_old(self):

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
        vecchioNome = 'n'
        vecchioCognome = 'c'
        listaV = []
        for anno in db.keys():
            listaV.clear()
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
                    # print("giorno data ",giorno_data)
                    dizzy[giorno_data]['mese'] = mese_data
                    dizzy[giorno_data]['giorno'] = giorno_nome
                    listak = [x for x in db[anno][mese][giorno].keys() if x not in self.listak]
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
                                                if nome == 'franco' and giorno == 3:
                                                    print("franco!", item)
                                                    print(listaV)
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
                        dizzy[giorno_data][k] = dato
                    if giorno_data not in listaDiz:
                        listaDiz[giorno_data] = dizzy
                    else:
                        print("diz già presente\n\t", diz.items())
            lik = [x for x in diz.keys()]
            lik.insert(0, 'data')
            if self.listaColonne != lik:
                self.listaColonne = lik
        # for d in listaDiz:
        #     print(d.keys())
        print("len listaDiz", len(listaDiz))
        print("dizzy \n\t\t", dizzy.items())
        return listaDiz

    def updateDiz_old_old(self):

        def getNames(a, m, g):
            form = QtCore.QDate
            mese_data = form(a, m, g).toString("MMM")
            giorno_data = form(a, m, g).toString("dd/MM/yyyy")
            giorno_nome = form(a, m, g).toString("ddd dd")
            return mese_data, giorno_data, giorno_nome

        def getItem(a, m, g, k, database):
            item = database[a][m][g][k]
            return item
        a = self.anno()
        db = deepcopy(self._database)

        listaDiz = []
        default = 'FFFFFF2121'
        # old = None
        vecchioNome = 'n'
        vecchioCognome = 'c'
        vecchioItem = 'i'
        listaV = []
        for anno in db.keys():
            listaV.clear()
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
                    listak = [x for x in db[anno][mese][giorno].keys() if x not in self.listak]

                    for k in db[anno][mese][giorno].keys():
                        item = getItem(anno, mese, giorno, k, db)
                        dato = db[anno][mese][giorno][k]

                        # if item == 'franco':
                        #     print("franco!")
                        # if k in listak:
                        #     pass
                        if k == 'nome':
                            if vecchioNome != item and (vecchioNome != '' or vecchioNome != '*'):
                                vecchioNome = item[:]
                                nome = vecchioNome

                                # dato = db[anno][mese][giorno][k]
                                # dato = '*'
                            #
                            # else:
                            #     # dato = '*'
                            #     # dato = db[anno][mese][giorno][k]
                            #     print("vecchio  ",vecchio)
                        elif k == 'cognome':
                            if vecchioCognome != item and (vecchioCognome != '' or vecchioCognome != '*'):
                                vecchioCognome = item[:]
                        #
                        # if vecchio != ('' or '*') and vecchio != item:
                        #     dato = '*'
                        # else:
                        #     print("ieri = giorno !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                        #     # ieri = giorno
                        #     dato = db[anno][mese][giorno][k]
                        else:
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
                                                if nome == 'franco' and giorno == 3:
                                                    print("franco!", item)
                                                    print(listaV)
                                                # listaV.clear()
                                                # listaV.append(item)
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

                            # dato = db[anno][mese][giorno][k]

                        # dato = db[anno][mese][giorno][k]
                        dizzy[giorno_data][k] = dato
                        # vecchio = item
                    ieri = giorno

                if diz not in listaDiz:
                    listaDiz.append(dizzy)
            lik = [x for x in diz.keys()]
            lik.insert(0, 'data')
            if self.listaColonne != lik:
                self.listaColonne = lik
        return listaDiz

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
            # print("££££££££££££££££££££")
            # print(f"csv non presente {nomeFile}, procedo alla creazione")
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
                # print("database virtuale aggiornato, pronto per csv")
                # print(traceback.format_exc())

            return True
