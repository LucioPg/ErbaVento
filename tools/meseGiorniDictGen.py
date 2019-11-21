from PyQt5.QtCore import QDate, QObject
from PyQt5.QtWidgets import QApplication
from traceback import format_exc as fex
from collections import OrderedDict as Od
import sys

class GiorniDelMese(QObject):
    def __init__(self,data:QDate):
        super(GiorniDelMese, self).__init__()
        self.dataDaLavorare = data

    @staticmethod
    def sendList(dataDaLavorare) -> list:
        """ la lista deve essere [ [] ]
            la tabella sempre piena, quindi rows = 6 ; cols = 7
            il primo giorno deve essere un lunedì"""
        rows = 7
        cols = 6
        primoDelMese = QDate(dataDaLavorare.year(), dataDaLavorare.month(), 1)
        lun = GiorniDelMese.iLunedi(primoDelMese)[0]
        corrente = lun
        listaGiorni = []
        for c in range(cols):
            listaGiorni.append([])
            for r in range(rows):
                listaGiorni[c].append(corrente)
                corrente = corrente.addDays(1)
        print(listaGiorni)
        return listaGiorni

    @staticmethod
    def sendDict_old(dataDaLavorare) -> dict:
        tot = dataDaLavorare.daysInMonth()
        giorniLista = [d for d in range(1,tot+1)]
        def colDict(lista=[]):
            """deve ritornare un dizionario"""
            listaCopiata = lista.copy()
            listaTemp = []
            diz = {}
            while len(listaCopiata):
                try:
                    listaTroncata = listaCopiata[:7]
                    for x in listaTroncata:
                        ind = listaCopiata.index(x)
                        if x not in listaTemp:
                            estratto = listaCopiata.pop(ind)
                            chiave = estratto % 7
                            if chiave == 0:
                                chiave = 7
                            if chiave not in diz.keys():
                                diz[chiave] = []
                            listaTemp.append(estratto)
                            diz[chiave].append(estratto)
                except:
                    print(fex())
            return diz
        return colDict(giorniLista)

    @staticmethod
    def sendDict(dataDaLavorare) -> dict:
        def getQDate(giorno):
            return QDate(dataDaLavorare.year(), dataDaLavorare.month(), giorno)
        tot = dataDaLavorare.daysInMonth()
        giorniLista = [getQDate(d) for d in range(1, tot + 1)]

        def colDict(lista=[]):
            """deve ritornare un dizionario"""
            listaCopiata = lista.copy()
            listaTemp = []
            diz = {}
            while len(listaCopiata):
                try:
                    listaTroncata = listaCopiata[:7]
                    for x in listaTroncata:
                        ind = listaCopiata.index(x)
                        if x not in listaTemp:
                            estratto = listaCopiata.pop(ind)
                            estrattoInt = estratto.day()
                            chiave = estrattoInt % 7
                            if chiave == 0:
                                chiave = 7
                            if chiave not in diz.keys():
                                diz[chiave] = []
                            listaTemp.append(estratto)
                            diz[chiave].append(estratto)

                except:
                    print(fex())
            return diz

        return colDict(giorniLista)

    @staticmethod
    def iLunedi(oggi):
        dayWeek = oggi.dayOfWeek()
        if dayWeek > 1:
            indietro = dayWeek - 1
            lunediPrec = oggi.addDays(-indietro)
        else:
            lunediPrec = oggi
        lunediSucc = lunediPrec.addDays(7)

        return (lunediPrec, lunediSucc,)





class MeseGiorniDictGen(QObject):
    listaMesi = ['Gennaio',
                 'Febbraio',
                 'Marzo',
                 'Aprile',
                 'Maggio',
                 'Giugno',
                 'Luglio',
                 'Agosto',
                 'Settembre',
                 'Ottobre',
                 'Novembre',
                 'Dicembre']
    def __init__(self, oggi: QDate):
        super(MeseGiorniDictGen, self).__init__()
        self._oggi = oggi

    @staticmethod
    def genDict(oggi: QDate = ...,num=False) -> dict:
        dizAnno = {}
        for m in range(1, 13):
            primoDellAnno = QDate(oggi.year(), m, 1)
            lista = MeseGiorniDictGen.sendList(primoDellAnno)
            if not num:
                dizAnno[MeseGiorniDictGen.listaMesi[m-1]] = lista
            else:
                dizAnno[m-1] = lista
        return dizAnno
    @staticmethod
    def bigList(oggi: QDate = ...) -> list:
        bigList = []
        for m in range(1, 13):
            primoDellAnno = QDate(oggi.year(), m, 1)
            bigList.append(MeseGiorniDictGen.sendList(primoDellAnno))
        return bigList

    @staticmethod
    def iLunedi(oggi):
        dayWeek = oggi.dayOfWeek()
        if dayWeek > 1:
            indietro = dayWeek - 1
            lunediPrec = oggi.addDays(-indietro)
        else:
            lunediPrec = oggi
        lunediSucc = lunediPrec.addDays(7)

        return (lunediPrec, lunediSucc,)
    @staticmethod
    def sendList(dataDaLavorare) -> list:
        """ la lista deve essere [ [] ]
            la tabella sempre piena, quindi rows = 6 ; cols = 7
            il primo giorno deve essere un lunedì"""
        rows = 7
        cols = 6
        primoDelMese = QDate(dataDaLavorare.year(), dataDaLavorare.month(), 1)
        lun = MeseGiorniDictGen.iLunedi(primoDelMese)[0]
        corrente = lun
        listaGiorni = []
        for c in range(cols):
            listaGiorni.append([])
            for r in range(rows):
                listaGiorni[c].append(corrente)
                corrente = corrente.addDays(1)
        # print(listaGiorni)
        return listaGiorni


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # gen = MeseGiorniDictGen(QDate().currentDate())
    gen = MeseGiorniDictGen.genDict(QDate().currentDate())

    for k,v in gen.items():
        print(k,v)