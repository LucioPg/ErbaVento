
from collections import OrderedDict
from pyexcel_ods import save_data
data = OrderedDict()
data.update({"agosto 2019": [["nome", "peppe", 3], [4, 5, 6]]})

save_data("your_file.ods", data)


def bisestileCheck(anno):
    anno = int(anno)
    if anno % 4 == 0 or anno % 100 == 0:
        # self.bisestile = True
        numeriGiorni = {"gennaio": 31, "febbraio": 29, "marzo": 31, "aprile": 30, "maggio": 31, "giugno": 30,
                        "luglio": 31, "agosto": 31, "settembre": 30, "ottobre": 31, "novembre": 30, "dicembre": 31}
    else:
        # self.bisestile = False
        numeriGiorni = {"gennaio": 31, "febbraio": 28, "marzo": 31, "aprile": 30, "maggio": 31, "giugno": 30,
                        "luglio": 31, "agosto": 31, "settembre": 30, "ottobre": 31, "novembre": 30, "dicembre": 31}
def setNomeCognome(nome,cognome):
    data