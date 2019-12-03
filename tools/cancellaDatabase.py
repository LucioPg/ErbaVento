from subprocess import check_call
import os
from traceback import format_exc as fex

database = '..\database.pkl'
spese = '..\speseDb.pkl'
lista = [database, spese]
try:
    os.system('del "..\speseDb.pkl"')
    os.system('del "..\database.pkl"')
except:
    print(fex())

print('databases deleted')
# for d in lista:
#     check_call(['del', d],shell=True)
