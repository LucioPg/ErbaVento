""" subclass di QDateEdit
    premendo i pulsanti step up /down si può accedere al mese successivo"""

from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from pprint import pprint





class MyDateEdit(QDateEdit):
    # SEGNALEFINEMESE = QtCore.pyqtSignal(QtCore.QDate)
    SEGNALEFINEMESE = QtCore.pyqtSignal()
    segnale_vecchia_data = QtCore.pyqtSignal(QtCore.QDate)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.installEventFilter(self)
        self.setDate(QtCore.QDate.currentDate())
        self.ieriSu = False
        self.ieriGiu = False
        self.vecchia_data = QtCore.QDate.currentDate()
        self.SEGNALEFINEMESE.connect(self.aggiorna)

    def set_direction(self, direction):
        self.ieriSu = direction
        self.ieriGiu = not direction

    def aggiorna(self):
        data = self.date()
        self.set_direction(self.vecchia_data < data)
        fineanno = QtCore.QDate(data.year(), 12, 31)
        capodanno = QtCore.QDate(data.year(), 1, 1)
        iniziomese = QtCore.QDate(data.year(), data.month(), 1)
        finemese = iniziomese.addMonths(1)
        finemese = finemese.addDays(-1)
        if finemese == data and self.ieriSu:
            if self.vecchia_data == fineanno:
                self.setDate(QtCore.QDate(data.year() + 1, 1, 1))
            else:
                self.setDate(self.date().addDays(1))
        elif iniziomese == data and self.ieriGiu:
            if self.vecchia_data == capodanno:
                self.setDate(QtCore.QDate(data.year() - 1, 12, 31))
            else:
                self.setDate(self.date().addDays(-1))

    def set_vecchia_data(self, vecchia):
        self.vecchia_data = vecchia

    def eventFilter(self, source, event: QtCore.QEvent) -> bool:
        if event.type() == 2:
            self.set_vecchia_data(self.date())
            return super(MyDateEdit, self).eventFilter(source, event)
        elif event.type() == 3:
            self.SEGNALEFINEMESE.emit()
        else:
            event.ignore()
        return False

class MyDateEdit_old(QDateEdit):
    SEGNALEFINEMESE = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.installEventFilter(self)
        self.setDate(QtCore.QDate.currentDate())
        self.ieriSu = False
        self.ieriGiu = False
        self.laltro = QtCore.QDate.currentDate()
        self.SEGNALEFINEMESE.connect(self.check_mese)

        self.prossimo = False

    def stepEnabled(self, *args, **kwargs):
        return super(MyDateEdit, self).stepEnabled(*args, **kwargs)

    @QtCore.pyqtSlot()
    def check_mese(self):
        d = self.date()
        a = d.year()
        m = d.addMonths(1).month()
        g = d.day()
        finemese = QtCore.QDate(a, m, 1).addDays(-1)
        iniziomese = QtCore.QDate(a, d.month(), 1)
        if self.laltro < d:
            self.ieriSu = True
            self.ieriGiu = False
        elif self.laltro > d:
            self.ieriGiu = True
            self.ieriSu = False
        if self.date() == iniziomese and self.ieriGiu:
            if not self.prossimo:
                self.prossimo = True
            else:
                self.setDate(d.addDays(-1))
                self.prossimo = False
        elif self.date() == finemese and self.ieriSu:
            if not self.prossimo:
                # print('if not self.ieriGiu:')
                self.prossimo = True
            else:
                # print('self.setDate(d.addDays(1))')
                self.setDate(d.addDays(1))
                self.prossimo = False
        self.laltro = d

    def eventFilter(self, source, event: QtCore.QEvent) -> bool:
        if event.type() == 3:
            self.SEGNALEFINEMESE.emit()
            return super(MyDateEdit, self).eventFilter(source, event)
        else:
            event.ignore()
        return False


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    main = QWidget()
    main.grid = QGridLayout(main)
    dateedit = MyDateEdit(main)
    main.grid.addWidget(dateedit)
    main.setLayout(main.grid)
    main.show()
    sys.exit(app.exec_())
