from PyQt5.QtCore import (QDate, QObject, pyqtSignal, QSize, QAbstractItemModel, QModelIndex, QByteArray, Qt,
                          QStringListModel)
from PyQt5.QtWidgets import (QTableView, QWidget, QSizePolicy, QAbstractItemView, QHBoxLayout, QDialog, QPushButton,
                             QComboBox, QVBoxLayout, QSpacerItem, QDataWidgetMapper, QLineEdit,QApplication, QLabel)
from PyQt5.QtGui import (QFont, QColor, QBrush, QStandardItemModel, QStandardItem)
import sys
from traceback import format_exc as fex
import typing


class ComboSenzaFreccia(QComboBox):
    whoIsComing = pyqtSignal(QWidget)
    def __init__(self,parent=None):
        super(ComboSenzaFreccia, self).__init__(parent)
        self.setStyleSheet ("""QComboBox::drop-down {border-width: 0px;} QComboBox::down-arrow {image: url(noimg); border-width: 0px;} QComboBox {border: 0px; background-color:qlineargradient(spread:reflect, x1:0.5, y1:0, x2:1, y2:0, stop:0.511364 rgba(102, 191, 255, 214), stop:1 rgba(0, 0, 0, 0));}""")
        self.setMaxVisibleItems(12)
        self.setMaxCount(12)
        # self.setModelColumn(0)
        self.setObjectName("comboSenzaFreccia")
        # self.setEditable(True)
        # self.lineEdit().setReadOnly(True)


class Mytable(QTableView):
    resized = pyqtSignal()
    cellClickedMyTable = pyqtSignal(QDate)
    whoIsComing = pyqtSignal(QWidget)
    def __init__(self,parent=None):
        super(Mytable, self).__init__(parent)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizePolicy(sizePolicy)
        self.verticalHeader().setVisible(False)
        self.resized.connect(self.resizing)
        self.horizontalHeader().setDefaultSectionSize(500)
        self.horizontalHeader().setMinimumHeight(30)
        font = QFont('Arial', 20)
        font2 = QFont('Arial', 17)
        self.horizontalHeader().setFont(font2)
        self.setFont(font)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        # self.doubleClicked.connect(self.dClick)
        self.clicked.connect(self.dClick)

    def dClick(self,ind):
        data = self.model().date[ind.row()][ind.column()]
        self.cellClickedMyTable.emit(data)
        return data


class MyDialog(QDialog):
    def __init__(self,parent=None):
        super(MyDialog, self).__init__(parent)
        self.datas()
        self.selfSetUp()
        self.setUpWidgets()
        self.setUpLayouts()
        self.setUpModels()
        self.setUpMapper()
        self.setUpConnections()


    def datas(self):
        self.kinds = ['vegetale', 'animale']

    def selfSetUp(self):
        self.setWindowTitle('TableView v 0.2')
        self.setMinimumSize(QSize(int(680 * 1.5), int(600 * 1.5)))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        sizePolicy.setWidthForHeight(self.sizePolicy().hasWidthForHeight())
        self.setSizePolicy(sizePolicy)

    def setUpWidgets(self):
        # self.table = Mytable(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        sizePolicy.setWidthForHeight(self.sizePolicy().hasWidthForHeight())
        self.table = QLineEdit()
        self.table.setStyleSheet("background-color: rgb(255, 255, 127)")
        labSize = QSize(100,30)
        self.table.setFixedSize(labSize)
        self.table.setSizePolicy(sizePolicy)
        self.combo = ComboSenzaFreccia(self)
        botSize = QSize(30,30)
        self.bot_next = QPushButton(text='Next', parent=self)
        self.bot_prev = QPushButton(text='Prev', parent=self)
        self.bot_prev.setSizePolicy(sizePolicy)
        self.bot_next.setSizePolicy(sizePolicy)
        self.bot_prev.setFixedSize(botSize)
        self.bot_next.setFixedSize(botSize)


    def setUpLayouts(self):
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.finalLay = QHBoxLayout()
        self.finalLay.setObjectName("finalLay")
        self.prevLay = QVBoxLayout()
        self.prevLay.setObjectName("prevLay")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.bot_prev.setObjectName("bot_prev")
        self.horizontalLayout_3.addWidget(self.bot_prev)
        self.prevLay.addLayout(self.horizontalLayout_3)
        spacerItem1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.prevLay.addItem(spacerItem1)
        self.finalLay.addLayout(self.prevLay)
        self.centLay = QVBoxLayout()
        self.centLay.setObjectName("centLay")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.combo.setMaxVisibleItems(12)
        self.combo.setMaxCount(12)
        self.combo.setObjectName("ComboSenzaFreccia")
        self.verticalLayout_2.addWidget(self.combo)
        # self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setObjectName("table")
        # self.table.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_2.addWidget(self.table)
        self.centLay.addLayout(self.verticalLayout_2)
        self.finalLay.addLayout(self.centLay)
        self.nextLay = QVBoxLayout()
        self.nextLay.setObjectName("nextLay")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.bot_next.setObjectName("bot_next")
        self.horizontalLayout_4.addWidget(self.bot_next)
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.nextLay.addLayout(self.horizontalLayout_4)
        spacerItem3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.nextLay.addItem(spacerItem3)
        self.finalLay.addLayout(self.nextLay)
        self.horizontalLayout.addLayout(self.finalLay)
        self.setLayout(self.horizontalLayout)
    def setUpLayouts_old(self):
        vboxPrev = QVBoxLayout()
        self.prevLay = QHBoxLayout()
        sp = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        vboxPrev.addItem(sp)
        vboxPrev.addWidget(self.bot_prev)
        sp = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.prevLay.addLayout(vboxPrev)
        self.prevLay.addItem(sp)

        vboxPrev = QVBoxLayout()
        self.nextLay = QHBoxLayout()
        sp = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        vboxPrev.addWidget(self.bot_next)
        vboxPrev.addItem(sp)
        sp = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.nextLay.addLayout(vboxPrev)
        self.nextLay.addItem(sp)

        self.centLay = QVBoxLayout()
        self.centLay.addWidget(self.combo)
        self.centLay.addWidget(self.table)

        self.finalLay = QHBoxLayout()
        self.finalLay.addLayout(self.prevLay)
        self.finalLay.addLayout(self.centLay)
        self.finalLay.addLayout(self.nextLay)

        self.setLayout(self.finalLay)

    def setUpModels(self):
        ## sono gli items che devo essere nella combo (es: i mesi)
        items = ['cane', 'gatto', 'melo', 'pero']
        #i numeri 4 e 2 passati come argomenti per il modello base indicano le righe e le colonne del modello
        # basate sulla len di items e di self.kinds
        self.model = QStandardItemModel(4, 2, self)
        # questo è il modello passato alla combo, che ha come elementi gli items
        self.typeModel = QStringListModel(items, self)
        self.combo.setModel(self.typeModel)
        # a ogni elemento di items deve corrispondere un valore, self.kinds, ricavato dall'indice
        types = ("1", "1", "0", "0")
        # per ogni item viene assegnato il valore nel modello matrice
        # la mappatura ha nella colonna 0 la combobox e gli viene assegnato un item
        # alla colonna 1 del modello viene assegnato il riferimento a self.kinds passato attraverso types
        for row, item in enumerate(items):
            self.model.setItem(row, 0, QStandardItem(item))
            self.model.setItem(row, 1, QStandardItem(self.kinds[int(types[row])]))
            # self.model.setItem(row, 1, QStandardItem(types[row]))
        # for row, col in enumerate()
    def setUpMapper(self):
        self.mapper = QDataWidgetMapper(self)
        self.mapper.setModel(self.model)
        # self.mapper.addMapping(self.table,1,b'currentIndex')
        self.mapper.addMapping(self.table,1)
        # self.mapper.addMapping(self.combo,0,b'currentIndex')
        self.mapper.addMapping(self.combo,0)
        self.mapper.currentIndexChanged.connect(self.updateButtons)
        self.mapper.toFirst()

    def setUpConnections(self):
        self.bot_next.clicked.connect(self.mapper.toNext)
        self.bot_prev.clicked.connect(self.mapper.toPrevious)
        try:
            self.combo.currentIndexChanged.connect(lambda x: self.mapper.setCurrentIndex(x))
            pass
        except:
            print(fex())
        # self.combo.currentIndexChanged.connect(lambda x: self.mapper.model().c)
    def updateButtons(self, row):
        self.bot_prev.setEnabled(row > 0)
        self.bot_next.setEnabled(row < self.model.rowCount() - 1)
        print('mapper current index', self.mapper.currentIndex())
        print('combo current index', self.combo.currentIndex())
        # print('mapper model rows count', self.mapper.model().rowCount())
        print('-'*20)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dia = MyDialog()
    dia.show()
    sys.exit(app.exec_())