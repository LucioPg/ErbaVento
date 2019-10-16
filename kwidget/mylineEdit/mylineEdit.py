""" questa versione di qlineedit ha un diverso tipo di filtro
    applicato ai campi di testo che viene determinato at run time
    passando una stringa nell'istanza"""

from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore


class MyLineEdit(QLineEdit):
    """ questa versione di qlineedit ha un diverso tipo di filtro
        applicato ai campi di testo che viene determinato at run time
        passando una stringa nell'istanza
        campi nome e cognome possono accettare lettere, apostrofo e spazio
        telefono solo numeri e il segno +
        l'email solo il formato adatto:
        nome@dominio
        deve esserci solo una @
        in nome ci possono essere punti, lettere, numeri ma non spazi
        in dominio ci deve essere un punto

        """

    TABPRESSED = QtCore.pyqtSignal(bool)
    def __init__(self, parent=None, nome=''):
        super().__init__(parent)
        self._nome = nome
        self.setText(nome.replace('lineEdit_', ''))
        self.nomeCognome = None
        # self.lineEdit = QLineEdit(self._text,self)
        self.setObjectName(self._nome)
        print(self.objectName())
        self.func = None
        shortcut = QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Tab), self,
                             context=QtCore.Qt.WidgetWithChildrenShortcut, activated=self.do_something)

    @QtCore.pyqtSlot()
    def do_something(self):
        print("do_something")
        flag = self.selector(self.text())
        if not flag:
            self.clear()
        self.TABPRESSED.emit(flag)
        return flag
        # self.returnPressed.connect(self.selector)
        # self.selector()

    # def keyPressEvent(self, e: QtGui.QKeyEvent):
    #     if e.key() == QtCore.Qt.Key_Tab:
    #         print("presto")
    #     else:
    #         print(e.key())
    # @QtCore.pyqtSlot()
    def setText(self, a0: str) -> None:
        super(MyLineEdit, self).setText(a0)
        self.clear()

    def selector(self, text):
        """
        sceglie quale funzione sarà usata dal segnale
        returPressed in base al testo passato nell'istanza
        :return:
        """
        print("selector : ", text)
        if text == '':
            return False
        if self.objectName() == 'lineEdit_nome' or self.objectName() == 'lineEdit_cognome':
            if self.filtraLettere(text):
                return True
            else:
                return False
        elif self.objectName() == 'lineEdit_telefono':
            if self.filtraTelefono(text):
                return True
            else:
                return False
        elif self.objectName() == 'lineEdit_email':
            if self.filtraEmail(text):
                return True
            else:
                return False
        else:
            self.setText('')
        self.setText(text)
        # print(f"type func {self._text}: ",type(func))

    def filtraLettere(self, text):
        lista = list(text)
        print(text)
        for ch in lista:
            if ('a' <= ch <= 'z') or ('A' <= ch <= 'Z') or ch == ' ' or ch == "'":
                pass
            else:
                print("The Given Character ", ch, "is an NOT Alphabet")
                return False
        return True

    def filtraTelefono(self, text):
        lista = list(text)
        if (lista[0].startswith('+') and text.count('+') == 1) or lista[0].isdigit():
            for ch in lista:
                if ('0' <= ch <= '9') or ch == '+':
                    pass
                else:
                    return False
            print("t'appost")
            return True

        else:
            return self.setText('')

    def filtraEmail(self, text):
        special = ['.', '@']
        print('email')
        try:
            nome, dominio = text.split('@')
            prec = ''
            for n in list(nome):
                if n.isdigit() or n.isalpha() or n == '.':
                    if prec == '.' and n == '.':
                        return False
                    else:
                        prec = n
                        print("carattere precedente: ", prec)

                else:
                    return False
            if dominio.count('.') == 1:
                dom, com = dominio.split('.')
                if len(com) != 3:
                    return False
                dominio = dominio.replace('.', '')

                for d in list(dominio):
                    if d.isdigit() or d.isalpha():
                        pass
                    else:
                        return False
                return True
            else:
                return False
        except ValueError:
            print('value err')

            return False
        except:
            print('input invalido\n')
            return False


class Dumb:
    def stampa(self):
        print("dumb")
