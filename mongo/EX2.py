from mongo.My_Documents.doc_erbavento import *
from mongoengine import *
from pymongo import MongoClient
from PyQt5.QtCore import QDate
from pprint import pprint

class Gusti(EmbeddedDocument):
    cibo = StringField()
    data = DateTimeField(default=datetime.today)
    numero = IntField()

class Uno(Document):
    nome = StringField(unique=1)
    eta = IntField()
    gusti = EmbeddedDocumentField(Gusti)

class Due(Document):
    nome = StringField(unique=1)
    eta = IntField()
    gusti = EmbeddedDocumentField(Gusti)

def show(doc):
    for campo in doc:
        valore = doc[campo]
        if type(valore) is Gusti:
            print(f'{campo}:')
            for gusto in valore:
                print(' '*len(campo), valore[gusto])
        else:
            print(f'{campo}: {valore} {type(valore)}')


if __name__ == '__main__':
    # _connection = connect('test_db',
    #         host='localhost',
    #         port=27017
    #         )
    # c = _connection['test_db'].authenticate(name='admin',
    #         password='admin')

    # clt = MongoClient("mongodb://admin:admin@localhost:27017/")
    # db = clt['test_db']
    # doc = db['prenotazione']

    gusti = Gusti(cibo='pizza', data=datetime.today(), numero=12)


    uno = Uno(nome='Lucio', eta=37, gusti=gusti)
    due = Due(nome='Antonella', eta=38, gusti=gusti)

    clt = MongoClient(host='localhost', port=27017)
    clt['test_db'].authenticate(name='admin',password='admin')
    db = clt['test_db']['prenotazione']
    # print(db['arrivo'].find_one())
    # db = clt['test_db']['prenotazione'].find_one()
    for x in db.find():
        print(x['arrivo'])
    # doc = db['c']
    # uno.gusti['cibo'] = 'pasta'

    # show(uno)
    # show(due)
    def del_docs():

        for uno, due in zip(Uno.objects(), Due.objects()):
            if uno:
                uno.delete()
            if due:
                due.delete()

    # del_docs()
    # _connection
    # # tre = Uno.objects(nome='Lucio')
    # print(tre)
    # show(tre[0])
    # quattro = Uno.objects.get(nome='Lucio')
    # show(quattro)
    # del_docs()
    # coll_names = _connection['test_db'].list_collection_names(nameOnly=False)

    # print(coll_names)
    # pprint(doc)
    # pprint(db)

    # docs = []
    # docs =_connection['test_db'].collections


    # _connection.get_document('prenotazione')
    # for coll in coll_names:
    #     docs.append(common.get_document(coll))
    # print(_connection['test_db']['prenotazione'].objects())
    # print(_connection['test_db']['prenotazione'])
    # pprint(docs)
    # print(_connection['test_db']['prenotazione'].list_collection_names())