import pickle
from PyQt5 import QtCore
import sys

# fil,data_2 = sys.argv[1],sys.argv[2]
fil = 'database.pkl'
with open(fil,"rb") as f:
    dati = pickle.load(f)


try:
    for k in dati[2019][10].keys():
        for kk, vv in dati[2019][10][k].items():
            print(kk,"\t",vv)
        print("*"*10)
    # print("file completo:\n", dati[sa][sm])
except KeyError:
    print("file completo:\n",dati)