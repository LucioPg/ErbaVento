from mongoengine import *
from pymongo import *
from mongo.scheda_ospite import *
from PyQt5.QtCore import QDate

connect('test_db', host='localhost', port=27017)

ospite = SchedaOspite(
    nome='Lucio',
    cognome='Di Capua',
    telefono='+393343519984',
    email='lucio.di.capua@gmail.com',
    arrivo=QDate(2020,2,25),
    partenza=QDate(2020,3,3),
    totale_ospiti=4,
    totale_bambini=1,
).save()

for obj in SchedaOspite.objects():
    print('#'*10)
    obj.pretty_print()
