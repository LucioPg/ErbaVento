import pickle

_file = 'database.pkl'

with open(_file, 'rb') as f:
    dati = f.readlines()

a = 2019
m = 10
g = 2
for x, y in dati[a][m][g]['checkIn'].items():
    print(x, ' ', y)