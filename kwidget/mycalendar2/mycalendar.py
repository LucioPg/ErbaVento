### PROVO A MANDARE SOLO LA DATA DI OGGI, IL RESTO LO LASCIO FARE AL MODELLO

import sys
from traceback import format_exc as fex

from PyQt5.QtCore import (QDate, pyqtSignal, QSize, Qt,
                          QStringListModel, pyqtProperty, QModelIndex)
from PyQt5.QtGui import (QFont, QStandardItemModel, QStandardItem, QResizeEvent)
from PyQt5.QtWidgets import (QTableView, QWidget, QSizePolicy, QAbstractItemView, QHBoxLayout, QPushButton,
                             QComboBox, QVBoxLayout, QDataWidgetMapper, QApplication,
                             QFrame, QGridLayout)

from meseGiorniDictGen import MeseGiorniDictGen
from models import MyModel
from complexLabels import ComplexLabel as complexLabel


# noinspection PyBroadException
class Mytable(QTableView):
    resized = pyqtSignal()
    cellClickedMyTable = pyqtSignal(QDate)
    whoIsComing = pyqtSignal(QWidget)
    sigModel = pyqtSignal(int)

    def __init__(self, parent=None, mesi=None):
        if mesi is None:
            self._mesi = mesi
        super(Mytable, self).__init__(parent)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizePolicy(sizePolicy)
        self.verticalHeader().setVisible(False)
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Plain)
        self.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.frameRect()
        self.oggi = QDate().currentDate()
        self.pagine = MeseGiorniDictGen.bigList(self.oggi)
        self.horizontalHeader().setMinimumHeight(30)
        font = QFont('Arial', 20)
        font2 = QFont('Arial', 17)
        self.horizontalHeader().setFont(font2)
        self.setFont(font)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.clicked.connect(self.click)
        self.sigModel.connect(lambda x: self.model().setDate(x))
        self.setModel(MyModel(mesi=self.pagine, parent=parent))
        self.setSizeAdjustPolicy(self.AdjustToContentsOnFirstShow)
        self.resized.connect(self.resizing)
        self._sizeSection = self.genSizes()

    def getMese(self):
        return self._mesi

    def setMese(self, m):
        self._mesi = m
        self.model()

    def click(self, ind):
        data = self.model()._date[ind.row()][ind.column()]
        self.cellClickedMyTable.emit(data)

    def genSizes(self, m=150):
        size = m
        while True:
            yield size
            print('gen size ', size)
            size += 10

    def resizingFromParent(self, size):
        self.verticalHeader().setDefaultSectionSize(size)
        self.horizontalHeader().setDefaultSectionSize(size)

    def resizing(self, size=None):

        try:
            if size is None:
                size = int(self.horizontalHeader().size().width() / 7)
            self.verticalHeader().setDefaultSectionSize(size)
            self.setSizeAdjustPolicy(self.AdjustToContents)
        except:
            print(fex())

    def resizeEvent(self, event):
        self.resized.emit()
        return super(Mytable, self).resizeEvent(event)

    mesi = pyqtProperty(str, fget=getMese, fset=setMese, notify=sigModel)


# noinspection PyUnresolvedReferences
class MyCalendar(QWidget):
    listaMesi = ['Gennaio',
                 'Febbraio',
                 'Marzo',
                 'Aprile',
                 'Maggio',
                 'Giugno',
                 'Luglio',
                 'Agosto',
                 'Settembre',
                 'Ottobre',
                 'Novembre',
                 'Dicembre']
    resized = pyqtSignal()
    doubleClicked = pyqtSignal(QDate)

    def __init__(self, parent=None):
        super(MyCalendar, self).__init__(parent)
        self.datas()
        self.selfSetUp()
        self.setUpWidgets()
        self.setUpModels()
        self.setUpMapper()
        self.setUpConnections()
        self.setUpLayouts()
        self.setCurrentDate(QDate().currentDate())
        self._info = {}

    def datas(self, annoNuovo: int = None):
        self.oggi = QDate().currentDate()
        if annoNuovo is not None:
            self.oggi = QDate(annoNuovo, 1, 1)
        self.pagine = MeseGiorniDictGen.bigList(self.oggi)

    def selfSetUp(self):
        self.setWindowTitle('TableView v 0.2')
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasWidthForHeight())
        sizePolicy.setWidthForHeight(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)


    def setUpWidgets(self):
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        sizePolicy.setWidthForHeight(self.sizePolicy().hasWidthForHeight())
        self.table = Mytable(self)
        self.table.setMinimumSize(QSize(0, 0))
        self.table.setFrameShape(QFrame.NoFrame)
        self.table.setFrameShadow(QFrame.Plain)
        self.table.setLineWidth(0)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setObjectName("table")
        self.table.setSizePolicy(sizePolicy)
        self.table.setToolTip('fai double click!!')
        self.combo = QComboBox()
        self.combo = ComboSenzaFreccia(self)
        self.combo.setMinimumSize(QSize(30, 40))
        self.combo.setMaxVisibleItems(12)
        self.combo.setMaxCount(12)
        self.combo.setModelColumn(0)
        self.combo.setObjectName("combo")
        self.bot_next = QPushButton(text='Next', parent=self)
        self.bot_prev = QPushButton(text='Prev', parent=self)
        self.bot_prev.setMinimumSize(QSize(40, 40))
        self.bot_prev.setMaximumSize(QSize(40, 40))
        self.bot_prev.setSizePolicy(sizePolicy)
        self.bot_prev.setObjectName("bot_prev")
        self.bot_next.setMinimumSize(QSize(40, 40))
        self.bot_next.setMaximumSize(QSize(40, 40))
        self.bot_next.setObjectName("bot_next")

    def setUpLayouts(self):
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bot_prev.sizePolicy().hasHeightForWidth())
        self.bot_prev.setSizePolicy(sizePolicy)
        self.horizontalLayout.addWidget(self.bot_prev)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo.sizePolicy().hasHeightForWidth())
        self.combo.setSizePolicy(sizePolicy)
        self.horizontalLayout.setSpacing(-15)
        self.horizontalLayout.addWidget(self.combo)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bot_next.sizePolicy().hasHeightForWidth())
        self.bot_next.setSizePolicy(sizePolicy)
        self.horizontalLayout.addWidget(self.bot_next)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.table.horizontalHeader().setStretchLastSection(False)
        self.verticalLayout.addWidget(self.table)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.setLayout(self.gridLayout)

    def setUpModels(self):
        ## sono gli items che devo essere nella combo (es: i mesi)
        # items = ['cane', 'gatto', 'melo', 'pero']
        items = self.listaMesi
        # i numeri 4 e 2 passati come argomenti per il modello base indicano le righe e le colonne del modello
        # basate sulla len di items e di self.pagine
        self.model = QStandardItemModel(len(items), len(items), self)
        # questo è il modello passato alla combo, che ha come elementi gli items
        self.typeModel = QStringListModel(items, self)
        self.combo.setModel(self.typeModel)
        # setto il modello per la tableView
        self.tableModel = MyModel(mesi=self.pagine, parent=self.table)
        self.table.setModel(self.tableModel)
        # a ogni elemento di items deve corrispondere un valore, self.pagine, ricavato dall'indice
        # types = ("1", "1", "0", "0")
        typesList = [str(x) for x in range(1, 13)]
        types = tuple(typesList)
        # per ogni item viene assegnato il valore nel modello matrice
        # la mappatura ha nella colonna 0 la combobox e gli viene assegnato un item
        # alla colonna 1 del modello viene assegnato il riferimento a self.pagine passato attraverso types
        for row, item in enumerate(items):
            self.model.setItem(row, 0, QStandardItem(item))
            self.model.setItem(row, 1, QStandardItem(types[row]))

    # noinspection PyUnresolvedReferences
    def setUpMapper(self):
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setModel(self.model)
        # self.mapper.addMapping(self.table,1,b'currentIndex')
        self.mapper.addMapping(self.table, 1, b'mesi')
        # self.mapper.addMapping(self.combo,0,b'currentIndex')
        self.mapper.addMapping(self.combo, 0)
        # self.mapper.currentIndexChanged.connect(self.updateButtons)
        self.mapper.currentIndexChanged.connect(lambda x: self.table.sigModel.emit(x))
        # self.mapper.toFirst()
        # self.mapper.toLast()
        self.mapper.setCurrentIndex(QDate().currentDate().month() - 1)

    def setUpConnections(self):
        self.resized.connect(self.tableAndComboResizing)
        self.bot_next.clicked.connect(self.toNext)
        self.bot_prev.clicked.connect(self.toPrevious)
        self.combo.currentIndexChanged.connect(lambda x: self.mapper.setCurrentIndex(x))
        self.table.cellClickedMyTable.connect(self.setCurrentDate)
        self.table.doubleClicked.connect(self.doubleClickSignal)
        self.doubleClicked.connect(self.book)

    def book(self):
        print('booked')
        if self.currentDate not in self._info.keys():
            self._info[self.currentDate] = 'manual insert'
        else:
            del self._info[self.currentDate]
        self.table.model()._info = self._info.copy()
        index = QModelIndex()
        self.table.model().dataChanged.emit(index,index)
        # app.exit(0)
    def doubleClickSignal(self, ind):
        data = self.table.model()._date[ind.row()][ind.column()]
        self.doubleClicked.emit(data)

    def toPrevious(self):
        currentIndex = self.mapper.currentIndex()
        try:
            self.mapper.setCurrentIndex(currentIndex - 1)
            afterIndex = self.mapper.currentIndex()
            if afterIndex == currentIndex:
                self.datas(self.oggi.year() - 1)
                self.table.model()._mesi = self.pagine
                self.mapper.toLast()
        except:
            print(fex())

    def toNext(self):
        currentIndex = self.mapper.currentIndex()
        try:
            self.mapper.setCurrentIndex(currentIndex + 1)
            afterIndex = self.mapper.currentIndex()
            if afterIndex == currentIndex:
                self.datas(self.oggi.year() + 1)
                self.table.model()._mesi = self.pagine
                self.mapper.toFirst()
        except:
            print(fex())

    def setCurrentDate(self, data):
        self.currentDate = data

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.resized.emit()

    def tableAndComboResizing(self):
        sizeD = self.size().height()
        self.table.resizingFromParent(int(sizeD / 8))


if __name__ == '__main__':
    from combosenzafreccia import ComboSenzaFreccia


    app = QApplication(sys.argv)
    app.setStyle('fusion')
    ui = MyCalendar()
    ui.show()
    sys.exit(app.exec_())
