from mongo.My_Documents.doc_erbavento import *
from mongoengine import *
from pymongo import errors
from PyQt5.QtCore import QDate

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
    _connection = connect('test_db',
            host='localhost',
            port=27017,
            ServerSelectionTimeoutMs=1000
           )
    try:
        c = _connection['test_db']
        c.authenticate(name='admin',
                password='admin')

        gusti = Gusti(cibo='pizza', data=datetime.today(), numero=12)


        uno = Uno(nome='Lucio', eta=37, gusti=gusti)
        due = Due(nome='Antonella', eta=38, gusti=gusti)

        # uno.gusti['cibo'] = 'pasta'
        try:
            uno.save()
            due.save()
        except NotUniqueError:
            pass
        # show(uno)
        # show(due)
        def del_docs():

            for uno, due in zip(Uno.objects(), Due.objects()):
                if uno:
                    uno.delete()
                if due:
                    due.delete()

        # del_docs()

        # tre = Uno.objects(nome='Lucio')
        # print(tre)
        # show(tre[0])
        # quattro = Uno.objects.get(nome='Lucio')
        # show(quattro)
        # del_docs()
        # print(c.list_collection_names())

        print(c.command('ping'))
    except errors.ServerSelectionTimeoutError:
        print('spento')
    except OperationError:
        print('error')

    except errors.OperationFailure:
        print('error 2')
    # except Exception as e:
    #     print(e)
    #     print('error 2')
