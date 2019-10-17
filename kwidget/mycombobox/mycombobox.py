import sys

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget


class MyWidget(QComboBox):
    EDITFINISHED = pyqtSignal(str)
    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)
        self.listaPlatform = ['Booking', 'AirB&B', 'Privati']
        self.preferPlat = 'Booking'
        # self.preferPlat = 'Privati'
        for p in self.listaPlatform:
            self.addPlatform(p)
        self.sortPreferPlat()
        # self.installEventFilter(self)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)

        # create context menu
        self.popMenu = QMenu(self)
        aggiungiAction = QAction('Aggiungi', self)
        self.popMenu.addAction(aggiungiAction)
        self.popMenu.addSeparator()
        rimuoviAction = QAction('Rimuovi', self)
        self.popMenu.addAction(rimuoviAction)
        self.popMenu.addSeparator()
        preferitoAction = QAction('Preferito', self)
        self.popMenu.addAction(preferitoAction)
        self.setEditable(False)
        aggiungiAction.triggered.connect(self.scriviNuovaPlat)
        rimuoviAction.triggered.connect(self.rimuoviPlat)
        preferitoAction.triggered.connect(self.setPreferrPlat)

    @pyqtSlot()
    def addPlatform(self, plat=None):
        if plat is None:
            plat = self.currentText()
        if plat not in self.listaPlatform:
            self.listaPlatform.append(plat)
        if -1 == self.findText(plat, Qt.MatchExactly):
            self.addItem(plat)
            self.model().sort(1)
        else:
            self.setEditable(False)
            return
        self.setEditable(False)

    def editFinished(self):
        text = self.lineEdit().text()
        return text

    def on_context_menu(self, point):
        # show context menu
        self.popMenu.exec_(self.mapToGlobal(point))

    def rimuoviPlat(self):
        ind = self.currentIndex()
        text = self.currentText()
        self.removeItem(ind)
        print(text, ' rimosso')

    def scriviNuovaPlat(self):
        self.setEditable(True)
        # QLineEdit.editingFinished()
        self.lineEdit().editingFinished.connect(self.addPlatform)

    def setPreferrPlat(self):
        text = self.currentText()
        self.preferPlat = text
        print("preferito: ", self.preferPlat)

    def sortPreferPlat(self):
        item = self.findText(self.preferPlat, Qt.MatchExactly)
        self.setCurrentIndex(item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dia = QDialog()
    grid = QGridLayout(dia)
    mw = MyWidget(dia)
    grid.addWidget(mw)
    dia.setLayout(grid)
    dia.show()
    sys.exit(app.exec_())
