from mongoengine import *
from pprint import pprint
from PyQt5.QtCore import QDate
from datetime import datetime
import string
import itertools

class DateExc(NotUniqueError):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None
    def __str__(self):
        if self.message:
            return f'{self.__class__.__name__},  {self.message}'

class OspiteExc(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'{self.__class__.__name__},  {self.message}'
        else:
            return 'Errore validazione Ospite'

# class OspiteIllegalName(OspiteExc):
class OspiteIllegalName(Exception):
    def __init__(self, *args):
        # super(OspiteIllegalName, self).__init__(*args)
        self.message = 'Il nome o il cognome non è valido'

    def __str__(self):
        if self.message:
            return f'{self.__class__.__name__},  {self.message}'
        else:
            return 'Errore validazione Ospite'

class QDateField(DateTimeField):
    """ Custom field to manage PyQt5.QtCore.QDate object"""
    def __init__(self, *args, **kwargs):
        super(QDateField, self).__init__(*args, **kwargs)
        self.counter = 0
    def validate(self, value):
        new_value = self.to_mongo(value)
        if not isinstance(new_value, datetime):
            self.error('cannot parse date "%s"' % value)

    def to_mongo(self, value):
        """ the QDate needs to be converted into datetime before sending to mongo"""

        try:
            if not isinstance(value, datetime) or not value:
                pdate = value.toPyDate()
                return datetime(pdate.year, pdate.month, pdate.day)
            else:
                return value
        except AttributeError:
            return value

        # pyValue = value.toPyDate()
        # return datetime(pyValue.year, pyValue.month, pyValue.day)

    def to_python(self, value):
        if not isinstance(value, QDate):
            qdate = QDate(value.year, value.month, value.day)
            return qdate
        else:
            return value

    def prepare_query_value(self, op, value):
        return super(QDateField, self).prepare_query_value(op, self.to_mongo(value))


class Prenotazione(Document):
    """ central class joining dates and users"""

    stagioni = [
        'Alta',
        'Media',
        'Bassa'
    ]
    data = QDateField(required=1)
    statistiche = ReferenceField('StatiSticheMensili')
    ospite_id = ReferenceField('Ospite', required=True)
    giorni = ReferenceField('DatePrenotazioni',required=True)
    stagione = StringField(choices=stagioni, default='Alta')
    platform = StringField(required=1, default='Privato')
    totale_notti = IntField(default=None)
    totale_ospiti = IntField(default=None)
    totale_bambini = IntField(default=None)
    colazione = BooleanField(default=False)
    # spese = FloatField(default=0.0)
    spese = 0
    importo = FloatField(default=0.0)
    tasse = FloatField(default=0.0)
    _tassa_giornaliera = 2
    _giorni_tassati = 3
    lordo = FloatField(default=0.0)
    netto = FloatField(default=0.0)
    # note = StringField(default='Questa è una nota', max_length=200)
    note = ReferenceField('Note')
    arrivo = QDateField(required=True)
    ultima_notte = QDateField(required=True)
    giorno_pulizie = QDateField(required=True)


    def clean(self):
        self.check_max_ospiti()
        self.check_max_bambini()
        self._compute_giorni()
        self._compute_arrivo()
        self._compute_data()
        self._compute_ultima_notte()
        self._compute_giorno_pulizie()
        self._compute_totale_notti()
        # self._compute_netto()
        # self._compute_tasse()
        # self._compute_lordo()



    ##### CHECKS #####

    def check_max_ospiti(self):
        if self.totale_ospiti >= 5:
            self.totale_ospiti = 5

    def check_max_bambini(self):
        if self.totale_bambini and not self.totale_ospiti:
            raise ValidationError('Non ci possono essere solo bambini')


    #### COMPUTED #####

    def _compute_giorni(self):

        self._giorni = self.giorni.giorni

    def _compute_arrivo(self):
        self.arrivo = min(self._giorni)

    def _compute_data(self):
        self.data = self.arrivo

    def _compute_ultima_notte(self):
        self.ultima_notte = max(self._giorni)

    def _compute_giorno_pulizie(self):
        self.giorno_pulizie = self.ultima_notte.addDays(1)

    def _compute_totale_notti(self):
        self.totale_notti = self.arrivo.daysTo(self.giorno_pulizie)

    def _compute_lordo(self):
        self.lordo = self.netto + self.tasse + self.spese

    def _compute_netto(self):
        self.netto = (self.importo * (self.totale_ospiti - self.totale_bambini))

    def _compute_tasse(self):
        tasse = 0
        contatore = 1
        permanenza = self.arrivo.daysTo(self.ultima_notte) + 1
        print('confronta permanenza con tot_notti ', permanenza == self.totale_notti)
        print(f'permanenza {permanenza}')
        mese = self.arrivo.month()
        data = self.arrivo
        for giorno in range(permanenza):
            data = data.addDays(1)
            if data.month() != mese:
                contatore = 0
                mese = data.month()
            if contatore < self._giorni_tassati:
                tasse += self._tassa_giornaliera
                print(f'tasse: {tasse} data: {data}')
                contatore += 1

        self.tasse = tasse * abs(self.totale_ospiti - self.totale_bambini)

    def pretty_print(self):
        user_dict = self.ospite_id.identificativo
        doc = {
            'user': user_dict,
            'giorni': self.giorni.giorni
        }
        return pprint(doc)


class Ospite(Document):
    """ doc for Hosts"""
    nome = StringField(required=True)
    cognome = StringField(required=True)
    telefono = StringField(required=1)
    identificativo = StringField(required=True, unique=True)
    data = QDateField(required=1)
    email = EmailField()
    prenotazioni = ListField(ReferenceField('Prenotazione'), reverse_delete_rule=CASCADE)
    data = QDateField(required=1)
    # cliente = BooleanField(default=False)

    def clean(self):
        self.validate_phonenumber()
        self.validate_nome_cognome()
        self._compute_identificativo()


    #### CHECKS #####

    def validate_phonenumber(self):
        """ checks the number provided is valid by searching for special chars, '+' excluded, and for alpha"""
        special_chars = set(string.punctuation.replace('+', ''))
        for number in self.telefono:
            if number.isalpha() or number in special_chars:
                raise OspiteExc('Il campo numero di telefono non è valido')

    def validate_nome_cognome(self):
        alpha = set(list(string.ascii_letters + "' ") + [None])
        for lettera_nome, lettera_cognome in itertools.zip_longest(self.nome, self.cognome, fillvalue=None):
            if (lettera_nome or lettera_cognome) not in alpha :
                raise OspiteIllegalName

    #### COMPUTE ####
    def _compute_identificativo(self):
        self.identificativo = self.nome + self.cognome + self.telefono


class DatePrenotazioni(Document):
    """ doc for dates info"""


    ospite = ReferenceField('Ospite')
    prenotazione = ReferenceField('Prenotazione')
    giorni = ListField(QDateField(), unique=True)
    data = QDateField(unique=1)
    spese = FloatField(default=0.0)

    # is_arrivo = BooleanField()
    # is_partenza = BooleanField()
    # is_booked = BooleanField()

    def clean(self):
        self.check_sequence_for_days()
        self._compute_data()

    #### CHECKS ####

    def check_sequence_for_days(self):
        """ checking if dates are in sequence"""
        # delta = (max(self.giorni) - min(self.giorni)).days + 1  # the difference returns a timedelta
        try:
            delta = abs(max(self.giorni).daysTo(min(self.giorni))) + 1
            if delta != len(self.giorni):
                raise ValidationError('dates need to be in sequence')
        except ValueError as e:
            return print(e)
    #### COMPUTE ####
    def _compute_data(self):
        if self.giorni:
            self.data = self.giorni[0]

class Note(Document):
    """ bind notes with dates"""

    data = QDateField(required=1, unique=1)
    note = StringField()

class SpeseGiornaliere(EmbeddedDocument):

    data = QDateField(unique=1, required=1)
    # spese = ListField( required=1)
    spese = DictField()
    tot_spese_giornaliere = FloatField(default=0.0)
    old_spese = None

    def clean(self):
        # self.validate_spese()
        self._compute_tot_spese_giornaliere()

    def set_spese(self, _spese):
        self.old_spese = self.spese
        self.spese = _spese
        try:
            # self.validate_spese()
            self._compute_tot_spese_giornaliere()
        except Exception as e:
            self.spese = self.old_spese
            print('setSpese_SpeseGiorn, ', e)

    def validate_spese(self):
        for lista_spesa in self.spese:
            if type(lista_spesa) is not tuple:
                print('validate_spese ',lista_spesa)
                lista_spesa = tuple(lista_spesa)
                # raise ValidationError("lista della spesa deve essere una tupla")
                # raise ValidationError("lista della spesa deve essere una tupla")
            if len(lista_spesa) != 2:
                raise ValidationError('manca o il nome della spesa o importo')
            if type(lista_spesa[0]) is not str or type(lista_spesa[1]) is not float:
                raise ValidationError("il nome o l'importo non sono nel formato corretto")
        print('validate_spese ',self.spese)

    def _compute_tot_spese_giornaliere(self):
        # self.tot_spese_giornaliere = sum([spesa[1] for spesa in self.spese])
        self.tot_spese_giornaliere = sum([spesa for spesa in self.spese.values()])

class SpeseMensili(Document):

    anno = IntField(required=1)
    mese = IntField(required=1)
    data = QDateField(required=1, unique=1)
    # spese_giornaliere = ListField(ReferenceField('SpeseGiornaliere'))
    spese_giornaliere = EmbeddedDocumentListField(SpeseGiornaliere)
    spese_mensili = FloatField(default=0.0)

    def clean(self):
        self._compute_spese_mensili()

    def _compute_spese_mensili(self):
        self.spese_mensili = 0
        for spesa_giornaliera in self.spese_giornaliere:
            self.spese_mensili += spesa_giornaliera.tot_spese_giornaliere

class StatiSticheMensili(Document):


    anno = IntField(required=1)
    mese = IntField(required=1)
    data = QDateField(required=1, unique=1)
    date_prenotate = ListField(ReferenceField('DatePrenotazioni'), default=[])
    notti_3 = IntField(required=1, default=0)  # da prenotazioni
    notti_2 = IntField(required=1, default=0)  # da prenotazioni
    notte_1 = IntField(required=1, default=0)  # da prenotazioni
    totale_notti = IntField(required=1, default=0)  # da prenotazioni
    tasse_mensili = FloatField(required=1, default=0.0)  # da prenotazioni
    netto_mensile = FloatField(required=1, default=0.0)  # da prenotazioni
    spese_mensili_obj = ReferenceField('SpeseMensili')
    spese_mensili = FloatField(required=1, default=0.0)
    totale_ospiti = IntField(required=1, default=0)  # da prenotazioni
    totale_bambini = IntField(required=1, default=0)  # da prenotazioni

    def clean(self):
        self._compute_data()
        self._compute_spese_mensili()
        self._compute_from_prenotazioni()

    def _compute_data(self):
        self.data = QDate(self.anno, self.mese, 1)

    def _compute_spese_mensili(self):
        if self.spese_mensili_obj:
            try:
                self.spese_mensili = self.spese_mensili_obj.spese_mensili
                print('spese mensili obj in statistiche: ', self.spese_mensili_obj)
            except Exception as e:
                print('statistiche spese mensili except')
                print(e)
                self.spese_mensili = None
        else:
            print('statistiche spese mensili none, doc_Erb')
            self.spese_mensili = 0.0

    def _compute_from_prenotazioni(self):
        self.totale_notti = 0
        self.totale_bambini = 0
        self.totale_ospiti = 0
        self.netto_mensile = 0
        self.tasse_mensili = 0
        self.notte_1 = 0
        self.notti_2 = 0
        self.notti_3 = 0

        for data in self.date_prenotate:
            if data:

                totale_notti = data.prenotazione.totale_notti
                self.totale_notti += totale_notti
                if totale_notti >= 3:
                    self.notti_3 +=1
                elif totale_notti == 2:
                    self.notti_2 += 1
                else:
                    self.notte_1 += 1
                self.totale_ospiti += data.prenotazione.totale_ospiti
                self.totale_bambini += data.prenotazione.totale_bambini
                self.netto_mensile += data.prenotazione.netto
                self.tasse_mensili += data.prenotazione.tasse

        self.netto_mensile -= self.spese_mensili