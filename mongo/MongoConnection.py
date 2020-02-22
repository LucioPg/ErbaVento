from mongo.mongo_check_connection import *
from mongo.My_Documents.doc_erbavento import *
from mongoengine import *
from PyQt5.QtCore import QDate

DateExc = DateExc
OspiteExc = OspiteExc
OspiteIllegalName = OspiteIllegalName
SpeseGiornaliere = SpeseGiornaliere
SpeseMensili = SpeseMensili
StatiSticheMensili = StatiSticheMensili


class MongoConnection:

    def __init__(self):
        self.CONNECTED = False
        self.make_connection()

    def make_connection(self):
        if  mongo_check_connection():
            self.CONNECTED = True
            _connection = connect('test_db',
                        host='localhost',
                        port=27017
                        )
            _connection['test_db'].authenticate(name='admin',
                    password='admin')

    def create_ospite(self,nome, cognome, telefono):
        ospite = Ospite(nome=nome, cognome=cognome, telefono=telefono)
        return ospite  # it does not save for checking for dates during booking

    def create_prenotazione_doc(self,ospite,
                                date_document,
                                platform,
                                stagione,
                                importo,
                                totale_ospiti,
                                totale_bambini,
                                note,
                                colazione,
                                lordo,
                                netto,
                                tasse):
        return Prenotazione(ospite_id=ospite, giorni=date_document,
                            totale_ospiti=totale_ospiti, totale_bambini=totale_bambini,
                            importo=importo, platform=platform, stagione=stagione, note=note, colazione=colazione,
                            lordo=lordo, netto=netto, tasse=tasse).save()

        # if stagione and platform:
        #     return Prenotazione(ospite_id=ospite, giorni=date_document, platform=platform, stagione=stagione).save()
        # elif stagione and not platform:
        #     Prenotazione(ospite_id=ospite, giorni=date_document, stagione=stagione).save()
        # elif platform and not stagione:
        #     Prenotazione(ospite_id=ospite, giorni=date_document, platform=platform).save()
        # else:
        #     Prenotazione(ospite_id=ospite, giorni=date_document).save()

    def queries_ospite(self,identificativo):
        try:
            return Ospite.objects.get(identificativo=identificativo)
        except :
            pass

    def queries_dates_from_book(self,prenotazione):
        return DatePrenotazioni.objects.get(prenotazione=prenotazione)

    def queries_dates(self,dates=None):
        for date_doc in  DatePrenotazioni.objects:
            if dates == date_doc.giorni:
                return date_doc
    def get_date_doc(self, data):
        try:
            date_doc = DatePrenotazioni.objects.get(data=data)
        except DoesNotExist:
            return None
    def queries_prenotazioni(self,dates=None):
        if dates:
            return Prenotazione.objects.get(giorni=dates)

    def create_prenotazione(self,ospite, dates, platform, stagione,importo,
                                    totale_ospiti,
                                    totale_bambini,
                                    note,
                                    colazione,
                                    lordo,
                                    netto,
                                    tasse,
                                    ):
        prenotazione = self.create_prenotazione_doc(ospite,
                                                    dates,
                                                    platform,
                                                    stagione,
                                                    importo,
                                                    totale_ospiti,
                                                    totale_bambini,
                                                    note,
                                                    colazione,
                                                    lordo,
                                                    netto,
                                                    tasse,
                                                    )
        ospite.prenotazioni.append(prenotazione)
        dates.prenotazione = prenotazione
        dates.save(clean=False)
        ospite.save(clean=False)
        return prenotazione

    def book(self,ospite=None, identificativo=None,
             nome=None, cognome=None, telefono=None,
             dates=None, platform='Privato', stagione='alta',
             totale_ospiti=0, totale_bambini=0,
             colazione=False, importo = 0.0, note='', lordo=0.0,
             netto=0.0, tasse=0.0
             ):
        if not self.CONNECTED:
            return print('Not connected')
        if dates:  # it checks if dates are present before confirm the creation of an useless user
            if not ospite:
                try:
                    ospite = self.create_ospite(nome=nome, cognome=cognome, telefono=telefono)
                    ospite.save()  # ospite needs to be saved before creating a referenced doc
                except OspiteExc as e:
                    print('ospexc ',e)
                    raise OspiteExc(e)
                except OspiteIllegalName as e:
                    print(f'{e}\n going for updating')
                    raise OspiteIllegalName
                except NotUniqueError as e:
                    try:
                        if identificativo:
                            ospite = self.queries_ospite(identificativo=identificativo)
                        else:
                            ospite = self.queries_ospite(identificativo=nome + cognome + telefono)
                        if ospite is None:
                            raise OspiteExc('Ospite non trovato nel database')
                    except ValidationError as e:
                        raise OspiteExc(e)

                            # return print(e, '\nospite or identificativo is needed')
            try:
                date_document = DatePrenotazioni(
                    giorni=dates,
                    ospite=ospite,
                ).save()
                prenotazione = self.create_prenotazione(ospite,
                                    date_document,
                                    platform,
                                    stagione,
                                    importo,
                                    totale_ospiti,
                                    totale_bambini,
                                    note,
                                    colazione,
                                    lordo,
                                    netto,
                                    tasse,

                                    )

                date_document.prenotazione = prenotazione
                date_document.save()
                stat = self.get_stat(data=dates[0], data_doc=date_document, _create=1)

                prenotazione.save()
                prenotazione.statistiche = stat
                prenotazione.save()
                return prenotazione
            except NotUniqueError as e:
                print(e, 'interno')
                if not len(ospite.prenotazioni):
                    self.delete_ospite(ospite=ospite)
                raise DateExc('Date Occupate')
        else:
            return print('dates are mandatory, if an instance of user was present it has been aborted')

    def un_book(self,prenotazione, preserve=False):
        if not self.CONNECTED:
            return print('Not connected')
        ospite = prenotazione.ospite_id
        dates = prenotazione.giorni
        ospite.prenotazioni.remove(prenotazione)
        if not ospite.prenotazioni and not preserve:
            ospite.delete()
        else:
            ospite.save()
        dates.delete()
        note = prenotazione.note
        filtro = '\nNote Prenotazione:\n'
        if note and filtro in note.note:
            note_splitted = note.note.split(filtro)
            note.note = note_splitted[0]
            if not note.note:
                note.delete()
            else:
                note.save()
        statistiche = self.get_stat(dates.giorni[0])
        if prenotazione.giorni in statistiche.date_prenotate:
            statistiche.date_prenotate.remove(prenotazione.giorni)
            statistiche.save()
        prenotazione.delete()
        return note

    def delete_ospite(self,ospite=None, identificativo=None):
        if not self.CONNECTED:
            return print('Not connected')
        if not ospite and identificativo:
            ospite = self.queries_ospite(identificativo=identificativo)
        if ospite:
            if hasattr(ospite, 'prenotazioni'):
                for prenotazione_doc in ospite.prenotazioni:
                    prenotazione_doc.giorni.delete()
                    prenotazione_doc.delete()
            ospite.delete()

    def update_booking(self,dates_to_update=None, prenotazione=None):

        if dates_to_update and prenotazione:
            stagione = prenotazione.stagione
            platform= prenotazione.platform
            totale_ospiti = prenotazione.totale_ospiti
            totale_bambini = prenotazione.totale_bambini
            colazione = prenotazione.colazione
            importo = prenotazione.importo
            giorni_tassati = prenotazione._giorni_tassati
            tassa_giornaliera = prenotazione._tassa_giornaliera
            note = prenotazione.note
            if self.un_book(prenotazione, preserve=True):
                self.book(ospite=prenotazione.ospite_id, dates=dates_to_update,
                     stagione=stagione, platform=platform,
                     totale_ospiti=totale_ospiti, totale_bambini=totale_bambini, importo=importo, colazione=colazione)
            raise Exception('errore nella modifica della prenotazione')
        else:
            print('date di prenotazione necessarie')

    def get_prenotazioni_pulizie(self):
        datePrenotate = {}
        datePulizie = []
        if self.CONNECTED:
            print('Connesso')
            for prenotazione in Prenotazione.objects:
                platform = prenotazione.platform
                for giorno in prenotazione.giorni.giorni:
                    datePrenotate[giorno] = platform
                datePulizie.append(prenotazione.giorno_pulizie)

            return datePrenotate, datePulizie
        else:
            print('Non Connesso')
            self.make_connection()
            return self.get_prenotazioni_pulizie()

    # def get_prenotazione(self, data):
    #     for prenotazione in Prenotazione.objects:
    #         print(prenotazione)
    #         if data in prenotazione.giorni.giorni:
    #             return {'nome': prenotazione.ospite_id.nome,
    def get_info_from_prenotazione(self, prenotazione):
        if prenotazione.note:
            note = prenotazione.note.note
        else:
            note = ''
        return {'nome': prenotazione.ospite_id.nome,
                'cognome': prenotazione.ospite_id.cognome,
                'telefono': prenotazione.ospite_id.telefono,
                'email': prenotazione.ospite_id.email,
                'platform': prenotazione.platform,
                'data arrivo': prenotazione.arrivo,
                'data partenza': prenotazione.giorno_pulizie,
                'totale notti': prenotazione.totale_notti,
                'numero ospiti': prenotazione.totale_ospiti,
                'bambini': prenotazione.totale_bambini,
                'spese': '',
                'colazione': prenotazione.colazione,
                'stagione': prenotazione.stagione,
                'importo': prenotazione.importo,
                'lordo': prenotazione.lordo,
                'tasse': prenotazione.tasse,
                'netto': prenotazione.netto,
                'note': note,
                'prenotazione': prenotazione
                }

    def get_prenotazione_from_nota_doc(self, nota_doc):
        try:
            return Prenotazione.objects.get(note=nota_doc)
        except DoesNotExist:
            return None

    def get_prenotazione_from_date(self, data):
        try:
            for prenotazione in Prenotazione.objects:
                if data in prenotazione.giorni.giorni:
                    return prenotazione
        except DoesNotExist:
            return None

    def info_from_date(self, data):
        for prenotazione in Prenotazione.objects:
            if data in prenotazione.giorni.giorni:
                return {'nome': prenotazione.ospite_id.nome,
                'cognome': prenotazione.ospite_id.cognome,
                'telefono': prenotazione.ospite_id.telefono,
                'email': prenotazione.ospite_id.email,
                'platform': prenotazione.platform,
                'data arrivo': prenotazione.arrivo,
                'data partenza': prenotazione.giorno_pulizie,
                'totale notti': prenotazione.totale_notti,
                'numero ospiti': prenotazione.totale_ospiti,
                'bambini': prenotazione.totale_bambini,
                'spese': '',
                'colazione': prenotazione.colazione,
                'stagione': prenotazione.stagione,
                'importo': prenotazione.importo,
                'lordo': prenotazione.lordo,
                'tasse': prenotazione.tasse,
                'netto': prenotazione.netto,
                'note': prenotazione.note,
                'prenotazione': prenotazione
                        }

    def create_notes(self, data, note):
        try:
            nota = Note(data=data, note=note).save()
            return nota
        except NotUniqueError:
            self.update_note(note, self.get_note(data))



    def get_note(self, data, _create=False):
        try:
            dt = datetime(data.year(), data.month(), data.day())
            note_doc = Note.objects.get(data=dt)
            return note_doc
        except DoesNotExist:
            if _create:
                return self.create_notes(data, '')
            else:
                return None

    def get_all_note(self):
        for nota in Note.objects:
            yield nota

    def update_note(self,nuove_note, note_doc):
        try:
            note_doc.note += f'\n{nuove_note}'
            note_doc.save()
        except Exception as e:
            print(e)

    def get_spese_mensili(self, data_di_riferimento):
        try:
            return SpeseMensili.objects.get(data_di_riferimento=data_di_riferimento)
        except DoesNotExist:
            print('SpeseMensili does not exist, proceed with creation')
            return self.create_spesa_mensile(data_di_riferimento)

    def get_spesa_giornaliera(self, data, spesa_mensile):
        try:

            if isinstance(spesa_mensile, SpeseMensili):
                spese_giornaliere = [giornaliera for giornaliera in spesa_mensile.spese_giornaliere if giornaliera.data == data]
                if spese_giornaliere:
                    return spese_giornaliere[0]
                else:
                    spese_giornaliere = SpeseGiornaliere(data=data, spese={})
                    spesa_mensile.spese_giornaliere.append(spese_giornaliere)
                    spesa_mensile.save()
                    return spese_giornaliere

            return None, None
        except DoesNotExist:
            return None, None

    def update_spesa_giornaliera(self,spesa_giornaliera_doc, spese_dict):
        spese = [(nome, spesa) for nome, spesa in spese_dict.items()]
        if spese != spesa_giornaliera_doc.spese:
            if not spese:

                spesa_giornaliera_doc.delete()
                for mese in SpeseMensili.objects:
                    if mese.mese == spesa_giornaliera_doc.data.month() and mese.anno == spesa_giornaliera_doc.data.year():
                        statistiche = StatiSticheMensili.objects.get(mese=mese.mese)
                        if spesa_giornaliera_doc in mese.spese_giornaliere:
                            mese.spese_giornaliere.remove(spesa_giornaliera_doc)
                        if not mese.spese_giornaliere:
                            statistiche.spese_mensili_obj = None
                            mese.delete()
                        else:
                            mese.save()

                        statistiche.save()
                return False
            else:
                spesa_giornaliera_doc.spese = spese
                spesa_giornaliera_doc.save()
                return True


    def create_spesa_mensile(self, data):
        anno, mese = data.year(), data.month()
        # emb_spesa_giornaliera = SpeseGiornaliere()
        try:
            spesa_mensile = SpeseMensili(anno=anno, mese=mese, data_di_riferimento=self.make_data_ref(data)).save()

        except NotUniqueError as e:
            print(e)
            try:
                return SpeseMensili.objects.get(data_di_riferimento=self.make_data_ref(data))
            except DoesNotExist as e:
                print(e)
                return None


    def make_data_ref(self, data):
        return QDate(data.year(), data.month(), 1)

    def get_spesa_mensile(self, data):
        try:
            return SpeseMensili.objects.get(data_di_riferimento=self.make_data_ref(data))
        except DoesNotExist:
            return self.create_spesa_mensile(data)
    def create_em_spesa_giornaliera(self, data, spese_dict):
        try:
            return SpeseGiornaliere(data=data, spese_dict=spese_dict)
        except NotUniqueError as e:
            print(e)
            return None

    def update_emb_spesa_giornaliera(self, data, spese_dict):
        try:
            data_ref = QDate(data.year(), data.month(), 1)
            mensile = SpeseMensili.objects(data_di_riferimento=data_ref)
            giornaliera = [doc for doc in mensile.spese_giornaliere if doc.data == data][0]
            if giornaliera:
                giornaliera.set_spese(spese_dict)
            else:
                return None
        except Exception as e:
            print(e)

    def create_spesa_giornaliera(self,data, spese_dict):
        if spese_dict:
            spesa_giornaliera = SpeseGiornaliere(data=data, spese=[(nome, spesa) for nome, spesa in spese_dict.items()]).save()
            if spesa_giornaliera:
                data_di_riferimento = QDate(data.year(), data.month(), 1)
                spesa_mensile = self.get_spese_mensili(data_di_riferimento)
                if spesa_mensile:
                    if spesa_giornaliera not in spesa_mensile.spese_giornaliere:
                        spesa_mensile.spese_giornaliere.append(spesa_giornaliera)
                    spesa_mensile.save()

                        # if not statistiche.spese_mensili:
                        #     statistiche.spese_mensili = spesa_mensile
                        #     statistiche.save()

                else:
                    spesa_mensile = SpeseMensili(anno=data.year(),
                                             mese=data.month(),
                                             data_di_riferimento=data_di_riferimento,
                                             spese_giornaliere=[spesa_giornaliera]).save()
                return True
            else:
                return False
        else:
            return False

    def check_spesa(self,data):
        try:
            mensile = self.get_spese_mensili(self.make_data_ref(data))
            for giornaliera in mensile.spese_giornaliere:
                if giornaliera.spese and giornaliera.data == data:
                    return True
                elif not giornaliera.spese:
                    mensile.spese_giornaliere.remove(giornaliera)
                    if mensile.spese_giornaliere:
                        mensile.save()
                    else:
                        mensile.delete()
            return False
        except DoesNotExist:
            return False

    def get_spese_date(self):
        # d = [data for mensile in SpeseMensili.objects for data in mensile.spese_giornaliere if mensile.spese_giornaliere]
        d = [giornaliera.data   for mensile in SpeseMensili.objects for giornaliera in mensile.spese_giornaliere if mensile.spese_giornaliere]
        return d
        # for mensile in SpeseMensili.objects:
        #     if mensile.spese_giornaliere:
        #         for data in mensile.spese_giornaliere:




    def get_stat(self, data, data_doc=None, spese_mensili=None, _create=0):
        try:
            # stat = StatiSticheMensili.objects.get(anno=anno, mese=mese)
            stat = StatiSticheMensili.objects.get(identificativo=self.make_data_ref(data))
            if data_doc and data_doc not in stat.date_prenotate:
                print('get_stat ',data_doc)
                stat.date_prenotate.append(data_doc)
                stat.save()
            return stat
        except DoesNotExist:
            if _create:
                return self.create_stat_doc(data, data_doc, spese_mensili)

    def create_stat_doc(self, data, data_doc=None, spese_mensili_obj=None):
        anno, mese = data.year(), data.month()
        try:
            stat = StatiSticheMensili(anno=anno, mese=mese, spese_mensili_obj=spese_mensili_obj)
            # stat = self.get_stat(data, data_doc, spese_mensili_obj)
            if data_doc:
                stat.date_prenotate.append(data_doc)
            if spese_mensili_obj:
                stat.spese_mensili_obj= spese_mensili_obj
            stat.save()
            return stat
        except NotUniqueError as e:
            print(e)
            stat = self.get_stat(data, data_doc, spese_mensili_obj)
        return stat

    # def get_stat(self, date):
    #     stat = {}
    #     listaKeysStat = ['3 Notti', '2 Notti', '1 Notte', 'Tasse finora', 'Netto finora', 'Spese finora']
    #     for anno in stat.keys():
    #         for mese in stat[anno].keys():
    #             stat[anno][mese] = {k: 0 for k in listaKeysStat}
    #     for anno in database.keys():
    #         for mese in database[anno].keys():
    #             for giorno in database[anno][mese].keys():
    #                 chiave = deepc(database[anno][mese][giorno]['checkIn'])
    #                 numeroNotti = int(chiave['totale notti'])
    #                 stat[anno][mese]['Spese finora'] = int(chiave['spese'])
    #                 if numeroNotti >= 3:
    #                     stat[anno][mese]['3 Notti'] += 1
    #                 elif numeroNotti == 2:
    #                     stat[anno][mese]['2 Notti'] += 1
    #                 elif numeroNotti == 1:
    #                     stat[anno][mese]['1 Notte'] += 1
    #                 tasse = int(chiave['tasse'])
    #                 stat[anno][mese]['Tasse finora'] += tasse
    #                 netto = int(chiave['netto'])
    #                 stat[anno][mese]['Netto finora'] += netto
    #     return stat