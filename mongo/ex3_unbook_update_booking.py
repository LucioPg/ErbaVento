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
    dateList = [QDate(2020,1,31), QDate(2020,2,1), QDate(2020,2,2)]  # changed from datetime.datetime
    dateList_2 = [QDate(2020,8,31), QDate(2020,9,1), QDate(2020,9,2)]  # changed from datetime.datetime
    dateList_3 = [QDate(2020,3,31), QDate(2020,4,1), QDate(2020,4,2)]  # changed from datetime.datetime


    def create_ospite(nome, cognome, telefono):
        ospite = Ospite(nome=nome, cognome=cognome, telefono=telefono)
        return ospite  # it does not save for checking for dates during booking

    def create_prenotazione_doc(ospite,
                                date_document,
                                platform,
                                stagione,
                                importo,
                                totale_ospiti,
                                totale_bambini,
                                note,
                                colazione):
        return Prenotazione(ospite_id=ospite, giorni=date_document,
                            totale_ospiti=totale_ospiti, totale_bambini=totale_bambini,
                            importo=importo, platform=platform, stagione=stagione).save()

        # if stagione and platform:
        #     return Prenotazione(ospite_id=ospite, giorni=date_document, platform=platform, stagione=stagione).save()
        # elif stagione and not platform:
        #     Prenotazione(ospite_id=ospite, giorni=date_document, stagione=stagione).save()
        # elif platform and not stagione:
        #     Prenotazione(ospite_id=ospite, giorni=date_document, platform=platform).save()
        # else:
        #     Prenotazione(ospite_id=ospite, giorni=date_document).save()

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

    def create_prenotazione(ospite, dates, platform, stagione,importo,
                                    totale_ospiti,
                                    totale_bambini,
                                    note,
                                    colazione):
        prenotazione = create_prenotazione_doc(ospite,
                                               dates,
                                               platform,
                                               stagione,
                                               importo,
                                               totale_ospiti,
                                               totale_bambini,
                                               note,
                                               colazione)
        ospite.prenotazioni.append(prenotazione)
        dates.prenotazione = prenotazione
        dates.save()
        ospite.save()

    def book(ospite=None, identificativo=None,
             nome=None, cognome=None, telefono=None,
             dates=None, platform='Privato', stagione='alta',
             totale_ospiti=1, totale_bambini=0,
             colazione=False, importo = 50.0, note=''
             ):

        if dates:  # it checks if dates are present before confirm the creation of an useless user
            if not ospite:
                try:
                    ospite = create_ospite(nome=nome, cognome=cognome, telefono=telefono)
                    ospite.save()  # ospite needs to be saved before creating a referenced doc
                except Exception as e:
                    print(f'{e}\n going for updating')
                    if identificativo:
                        ospite = queries_ospite(identificativo=identificativo)
                    else:
                        try:
                            ospite = queries_ospite(identificativo=nome + cognome + telefono)
                        except Exception as e:
                            return print(e, '\nospite or identificativo is needed')
            try:
                date_document = DatePrenotazioni(
                    giorni=dates,
                    ospite=ospite,
                ).save()
                create_prenotazione(ospite,
                                    date_document,
                                    platform,
                                    stagione,
                                    importo,
                                    totale_ospiti,
                                    totale_bambini,
                                    note,
                                    colazione
                                    )
            except Exception as e:
                print(e)
                if not len(ospite.prenotazioni):
                    delete_ospite()
        else:
            return print('dates are mandatory, if an instance of user was present it has been aborted')

    def un_book(prenotazione, preserve=False):
        ospite = prenotazione.ospite_id
        dates = prenotazione.giorni
        ospite.prenotazioni.remove(prenotazione)
        print('prenotazioni rimanenti: ', ospite.prenotazioni)
        if not ospite.prenotazioni and not preserve:
            ospite.delete()
        else:
            ospite.save()
        dates.delete()
        prenotazione.delete()

    def delete_ospite(ospite=None, identificativo=None):
        if not ospite and identificativo:
            ospite = queries_ospite(identificativo=identificativo)
        if ospite:
            if hasattr(ospite, 'prenotazioni'):
                for prenotazione_doc in ospite.prenotazioni:
                    prenotazione_doc.giorni.delete()
                    prenotazione_doc.delete()
            ospite.delete()

    def update_booking(dates_to_update=None, prenotazione=None):

        if dates_to_update and prenotazione:
            stagione = prenotazione.stagione
            platform= prenotazione.platform
            totale_ospiti = prenotazione.totale_ospiti
            totale_bambini = prenotazione.totale_bambini
            colazione = prenotazione.colazione
            importo = prenotazione.importo
            giorni_tassati = prenotazione._giorni_tassati
            tassa_giornaliera = prenotazione._tassa_giornaliera
            un_book(prenotazione, preserve=True)
            book(ospite=prenotazione.ospite_id, dates=dates_to_update)
        else:
            print('date di prenotazione necessarie')
            # create_prenotazione_doc(ospite)

    def clear_all():
        for ospite in Ospite.objects:
            delete_ospite(ospite)
        for nota in Note.objects:
            nota.delete()
        for spesa_giornaliera in SpeseGiornaliere.objects:
            spesa_giornaliera.delete()
        for spesa_mensile in SpeseMensili.objects:
            spesa_mensile.delete()
        for statistica in StatiSticheMensili.objects:
            statistica.delete()





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

