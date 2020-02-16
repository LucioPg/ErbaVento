from mongoengine import *
from pprint import pprint
from PyQt5.QtCore import QDate
from datetime import datetime
import string

class QDateField(DateTimeField):
    """ Custom field to manage PyQt5.QtCore.QDate object"""
    def validate(self, value):
        new_value = self.to_mongo(value)
        if not isinstance(new_value, datetime):
            self.error('cannot parse date "%s"' % value)

    def to_mongo(self, value):
        """ the QDate needs to be converted into datetime before sending to mongo"""
        pyValue = value.toPyDate()
        return datetime(pyValue.year, pyValue.month, pyValue.day)

    def to_python(self, value):
        print(value)
        if not isinstance(value, QDate):
            qdate = QDate(value.year, value.month, value.day)
            return qdate
        else:
            return value

    def prepare_query_value(self, op, value):
        """ maybe useless"""
        return super(QDateField, self).prepare_query_value(op, self.to_mongo(value))


class SchedaOspite(Document):

    stagioni = [
        'Alta',
        'Media',
        'Bassa'
    ]

    nome = StringField(required=True)
    cognome = StringField(required=True)
    telefono = StringField(required=1)
    email = EmailField()
    totale_notti = IntField(default=1)
    totale_ospiti = IntField(default=1)
    totale_bambini = IntField(default=0)
    colazione = BooleanField(default=False)
    spese = FloatField(default=0.0)
    importo = FloatField(default=50.0)
    tasse = FloatField(default=0.0)
    lordo = FloatField(default=0.0)
    netto = FloatField(default=0.0)
    note = StringField(max_length=200)
    stagione = StringField(choices=stagioni, default='Alta')
    arrivo = QDateField(required=True, unique=1)
    partenza = QDateField(required=True)

    def clean(self):
        self.total_check()
        self.total_compute()

    def validate_phonenumber(self):
        """ checks the number provided is valid by searching for special chars, '+' excluded, and for alpha"""
        special_chars = set(string.punctuation.replace('+', ''))
        for number in self.telefono:
            if number.isalpha() or number in special_chars:
                raise ValidationError('Il campo numero di telefono non è valido')

    # def calc_spese(self):
    #     permanenza = self.arrivo.daysTo(self.partenza)
    #     for giorno in range(permanenza):
    #

    def check_max_ospiti(self):
        if self.totale_ospiti >= 5:
            self.totale_ospiti = 5

    def check_max_bambini(self):
        if self.totale_bambini and not self.totale_ospiti:
            raise ValidationError('Non ci possono essere solo bambini')

    def check_partenza(self):
        if not self.partenza:
            self.partenza = self.arrivo.addDays(1)

    def total_check(self):
        self.check_max_ospiti()
        self.check_max_bambini()
        self.check_partenza()
        self.validate_phonenumber()

    def total_compute(self):
        self.compute_totale_notti()
        self.compute_tasse()
        self.compute_netto()
        self.compute_lordo()

    def compute_totale_notti(self):
        self.totale_notti = self.arrivo.daysTo(self.partenza)

    def compute_lordo(self):
        self.lordo = self.netto + self.tasse + self.spese

    def compute_netto(self):
        self.netto = (self.importo * (self.totale_ospiti - self.totale_bambini))

    def compute_tasse(self):
        tasse = 0
        contatore = 1
        permanenza = self.arrivo.daysTo(self.partenza)
        print(f'permanenza {permanenza}')
        mese = self.arrivo.month()
        data = self.arrivo
        for giorno in range(permanenza):
            data = data.addDays(1)
            if data.month() != mese:
                contatore = 0
                mese = data.month()
            if contatore < 3:
                tasse += 2
                print(f'tasse: {tasse} data: {data}')
                contatore += 1

        self.tasse = tasse * (self.totale_ospiti - self.totale_bambini)

    def pretty_print(self):
        doc = {
            'nome': self.nome,
            'cognome': self.cognome,
            'telefono': self.telefono,
            'email': self.email,
            'arrivo': self.arrivo,
            'partenza': self.partenza,
            'importo': self.importo,
            'tasse': self.tasse,
            'lordo': self.lordo,
            'netto': self.netto,
        }
        return pprint(doc)
    # meta = {
    #     'indexes': ['author', 'title'],
    #     'ordering': ['-published', '-version']
    # }
