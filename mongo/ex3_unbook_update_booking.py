from mongo.My_Documents.doc_erbavento import *
from mongoengine import *
from PyQt5.QtCore import QDate
if __name__ == '__main__':
    _connection = connect('test_db',
            host='localhost',
            port=27017
            )
    _connection['test_db'].authenticate(name='admin',
            password='admin')

    def queries_ospite(identificativo):
        return Ospite.objects.get(identificativo=identificativo)

    def queries_dates_from_book(prenotazione):
        return DatePrenotazioni.objects.get(prenotazione=prenotazione)

    def queries_dates(dates=None):
        for date_doc in  DatePrenotazioni.objects:
            if dates == date_doc.giorni:
                return date_doc

    def queries_prenotazioni(dates=None):
        if dates:
            return Prenotazione.objects.get(giorni=dates)

    def delete_ospite(ospite=None, identificativo=None):
        if not ospite and identificativo:
            ospite = queries_ospite(identificativo=identificativo)
        if ospite:
            if hasattr(ospite, 'prenotazioni'):
                for prenotazione_doc in ospite.prenotazioni:
                    prenotazione_doc.giorni.delete()
                    prenotazione_doc.delete()
            ospite.delete()


    def clear_all():
        for ospite in Ospite.objects:
            delete_ospite(ospite)
        for nota in Note.objects:
            nota.delete()
        # for spesa_giornaliera in SpeseGiornaliere.objects:
        #     spesa_giornaliera.delete()
        for spesa_mensile in SpeseMensili.objects:
            spesa_mensile.delete()
        for statistica in StatiSticheMensili.objects:
            statistica.delete()
        for data in DatePrenotazioni.objects:
            data.delete()
        for prenotazione in Prenotazione.objects:
            prenotazione.delete()




    # book(nome='Pepped', cognome='sotto', identificativo='Peppedsotto111', telefono='111', dates=dateList_2)
    # book(nome='filippo', cognome='sopra', telefono='111',
    #      dates=dateList, platform='Booking', stagione='Bassa', totale_ospiti=5)
    clear_all()
    # book(nome='filippo', cognome='sopra', telefono='111',
    #      dates=dateList_3, platform='AirB&B', stagione='Media', totale_ospiti=4, totale_bambini=2)
    # book(nome='filippo', cognome='sopra', telefono='111', dates=dateList_3, platform='Booking', stagione='Media')
    # book(nome='filippo', cognome='sopra', telefono='111', dates=dateList_3)
    # prenotazione = queries_dates(dateList_2).prenotazione
    # prenotazione = queries_dates(dateList).prenotazione
    # un_book(prenotazione)
    # update_booking(dates_to_update=dateList, prenotazione=prenotazione)
    # delete_ospite(queries_ospite('Peppedsotto111'))
    # delete_ospite(queries_ospite('filipposopra111'))
    for obj in Prenotazione.objects():
        print('#'*10)
        obj.pretty_print()

