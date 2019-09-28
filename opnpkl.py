import pickle
from PyQt5 import QtCore
import sys

fil,data_2 = sys.argv[1],sys.argv[2]
with open(fil,"rb") as f:
    dati = pickle.load(f)
dataLines = data_2.split("\\")
g,m,a = int(dataLines[0]),int(dataLines[1]),int(dataLines[2])
data = QtCore.QDate(a,m,g)
sg,sm,sa = data.toString('dd'),data.toString('MMM'),data.toString('yyyy')

print(data.toString('dd MMM yyyy'))

try:
    print(dati[sa][sm][g])
    for k in dati[sa][sm].keys():
        print(k)
        for kk,vv in dati[sa][sm][k].items():
            print(kk,"\t",vv)
        print("*"*10)
    # print("file completo:\n", dati[sa][sm])
except KeyError:
    print("file completo:\n",dati)
    print(dati[sa][sm][sg])