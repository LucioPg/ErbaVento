import sys
from traceback import format_exc as fex
import os
from PyQt5.QtCore import (pyqtSignal, QModelIndex, QDate)
from PyQt5.QtGui import (QFont, QStandardItemModel, QStandardItem, QIcon, QCloseEvent)
from PyQt5.QtWidgets import (QTableView, QWidget, QAbstractItemView, QPushButton,
                             QApplication, QLabel, QGridLayout)

from kwidget.complexlabel.complex_gui import Ui_complexLabel as complexLabelGui


class ComplexLabel(complexLabelGui, QWidget):
    """Label equipped with 3 icons below. Ideal to be used into a QTableView cell"""
    iconActivated = pyqtSignal(int)

    # dictFlags = {'spese': 0, 'note': 0, 'pulizie': 0}
    def __init__(self,parent=None,data=None):
        super(ComplexLabel, self).__init__(parent)
        if data is None:
            data = 'data not setted'
        self.data = data
        self.setupUi(self)
        self.tuplaFlags = (1, 0, 0)
        self.dictFlags = {'spese': 0, 'note': 0, 'pulizie': 0}
        # self.dictFlags = {}
        # self.icons = [QIcon('../../Icons/iconaSpese.png'),
        #               QIcon('../../Icons/iconaNote.ico'),
        #               QIcon('../../Icons/iconaPulizie.png')
        #               ]
        self.iconsDict = {'spese': QIcon('./Icons/iconaSpese.png'),
                          'note': QIcon('./Icons/iconaNote.ico'),
                          'pulizie': QIcon('./Icons/iconaPulizie.png')}
        self.labelsDict = {'spese': self.labSpese, 'note': self.labNote, 'pulizie': self.labCleaning}
        self.labels = [self.labSpese, self.labNote, self.labCleaning]
        # self.bot = QPushButton('click me')
        # self.verticalLayout_5.addWidget(self.bot)
        # self.bot.clicked.connect(self.callUser)

    def addIcon(self,icon: QIcon, pos: int):
        self.icons[pos] = icon

    def callUser(self):
        self.changeActiveIcons()

    def enable(self, flag=True):
        for label in self.labels:
            label.setEnabled(flag)

    def setData(self, data: QDate()):
        if data is not None:
            self.data = data
        return self.data

    def setIcona(self, label: QLabel, icon: QIcon, remove=False):
        """ show the passed icon into the passed label and remove the icon if param remove is True"""
        if not remove:
            label.setPixmap(icon.pixmap(32, 32))
        else:
            label.clear()


    def setFont(self, font: QFont = None) -> None:
        if font is None:
            return
        else:
            self.lab_num.setFont(font)

    def setFontPointSize(self, px: int):
        self.lab_num.font().setPointSize(px)

    def setActiveTuple(self, flags: tuple = ()):
        """ it uses self.tuplaFlags or a passed tuple for setting the icons"""
        if len(flags) < 3:
            flags = self.tuplaFlags
        for indice, flag in enumerate(flags):
            print('flag: ', flag)
            label = self.labels[indice]
            icona = self.icons[indice]
            if flag:
                self.setIcona(label, icona)
            else:
                try:
                    self.setIcona(label, icona, remove=True)
                except:
                    print(fex())

    def setActive(self):
        """ it uses self.tuplaFlags or a passed tuple for setting the icons"""
        flags = self.dictFlags
        for key in flags.keys():
            label = self.labelsDict[key]
            # label = self.labels[indice]
            icona = self.iconsDict[key]
            # icona = self.icons[indice]
            if flags[key]:
                self.setIcona(label, icona)
                # print('flag setted: ', key, True)
            else:
                try:
                    # self.setIcona(label, icona, remove=True)
                    label.clear()
                except:
                    print(fex())

    # def setDictFlags(self,diz):
    #     self.__setattr__('dictflags', diz)

    def setText(self, text: str):
        self.lab_num.setText(text)

    def iconsOnOff(self,indice: int, stato: bool):
        flags = list[self.tuplaFlags]
        if stato:
            flags[indice] = 1
        else:
            flags[indice] = 0
        self.tuplaFlags = tuple(flags)
        self.setActive()


    def changeActiveIcons(self):
        """ testing purpouse"""
        flags = self.tuplaFlags
        if flags is not None:
            spese = flags[0]
            note = flags[1]
            cleaning = flags[2]
            if spese:
                spese = 0
                note = 1
                cleaning = 0
            elif note:
                spese = 0
                note = 0
                cleaning = 1
            elif cleaning:
                spese = 0
                note = 0
                cleaning = 0
            else:
                spese = 1
            tupla = (spese,note,cleaning)
            print('tupla: ',tupla)
            self.tuplaFlags = tupla
            self.setActive()

        # def permute(s, n, c):


class Button(QWidget):

    def __init__(self, *args):
        super(QWidget, self).__init__()
        grid = QGridLayout()
        names = ('One', 'Two', 'Three', 'Four', 'Five',
                 'Six', 'Seven', 'Eight', 'Nine', 'Ten')
        for i, name in enumerate(names):
            button = QPushButton(name, self)
            button.clicked.connect(self.make_calluser(name))
            row, col = divmod(i, 5)
            grid.addWidget(button, row, col)
        self.setLayout(grid)

    def make_calluser(self, name):
        def calluser():
            print(name)
        return calluser


# if __name__ == '__main__':
#     from combosenzafreccia import ComboSenzaFreccia
#
#
#     app = QApplication(sys.argv)
#     # app.setStyle('fusion')
#     dia = QDialog()
#     ui = ComplexLabel(dia)
#
#     hb = QHBoxLayout()
#     hb.addWidget(ui)
#     # hb.addWidget(bot)
#
#     dia.setLayout(hb)
#     dia.show()
#     but = Button()
#     but.show()
#     # bot.show()
#     sys.exit(app.exec_())
#
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    tab = QTableView()
    sti = QStandardItemModel()
    lista = []
    lista.append(QStandardItem())
    for i in range(3):
        lista.append(QStandardItem(str(i)))
    sti.appendRow(lista)
    tab.setModel(sti)
    # wid = QWidget()
    wid = ComplexLabel(tab)
    # vbox = QVBoxLayout()
    # vbox.addWidget(QLabel('hello'))
    # labIcon = QLabel()
    # icon = QIcon('sunny.ico')
    # icon2 = QIcon('iconSpese.ico')
    # icon.pixmap(QSize(64, 64))
    # labIcon.setPixmap(icon2.pixmap(QSize(64, 64)))
    # vbox.addWidget(labIcon)
    # wid.setLayout(vbox)
    # wid.show()
    tab.setEditTriggers(QAbstractItemView.NoEditTriggers)
    tab.setIndexWidget(sti.index(0, 0), wid)
    tab.verticalHeader().setMinimumSectionSize(100)
    tab.show()
    bot = QPushButton('click')
    # bot.clicked.connect(lambda: wid.changeActiveIcons())
    wid.dictFlags['spese'] = 1
    bot.clicked.connect(lambda: wid.setActive())
    wid.setText('ciao')
    # bot.clicked.connect(lambda: wid.enable(False))
    # todo attenzione le icone si trovano in ../../Icons/etc...
    bot.clicked.connect(lambda: wid.setEnabled(False))
    bot.setStyleSheet('background-color: green; font: 16px')
    bot.show()
    sys.exit(app.exec_())
