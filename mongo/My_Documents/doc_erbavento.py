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
    identificativo = StringField(required=True, unique=True)  #needs to be computed
    email = EmailField()
    prenotazioni = ListField(ReferenceField('Prenotazione'), reverse_delete_rule=CASCADE)
    arrivo = QDateField(required=False, unique=1, sparse=1)  # needs to be referenced
    partenza = QDateField(required=False)  # needs to be  referenced
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
    # totale_ospiti = IntField(default=1)
    # totale_bambini = IntField(default=0)
    # colazione = BooleanField(default=False)
    spese = FloatField(default=0.0)

    # is_arrivo = BooleanField()
    # is_partenza = BooleanField()
    # is_booked = BooleanField()

    def clean(self):
        self.check_sequence_for_days()

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


class Note(Document):
    """ bind notes with dates"""

    data = QDateField(required=1, unique=1)
    note = StringField()

class SpeseListField(ListField):
    pass
class SpeseGiornaliere(Document):

    data = QDateField(unique=1, required=1)
    spese = ListField( required=1)
    tot_spese_giornaliere = FloatField(default=0.0)

    def clean(self):
        self.validate_spese()
        self._compute_tot_spese_giornaliere()

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
        self.tot_spese_giornaliere = sum([spesa[1] for spesa in self.spese])

class SpeseMensili(Document):

    anno = IntField(required=1)
    mese = IntField(required=1)
    data_di_riferimento = QDateField(required=1)
    spese_giornaliere = ListField(ReferenceField('SpeseGiornaliere'))
    spese_mensili = FloatField(default=0.0)

    def clean(self):
        self._compute_spese_mensili()

    def _compute_spese_mensili(self):
        for spesa_giornaliera in self.spese_giornaliere:
            self.spese_mensili += sum([spesa[1] for spesa in spesa_giornaliera.spese])