from traceback import format_exc as fex

from PyQt5.QtCore import (QDate, QModelIndex, Qt,
                          QAbstractTableModel)
from PyQt5.QtGui import (QColor, QBrush)

from complexLabels import ComplexLabel as complexLabel
from collections import OrderedDict as Od

# noinspection PyUnusedLocal
class TableModel:
    def __init__(self, parent):
        pass


# noinspection PyUnusedLocal
class ComboModel:
    def __init__(self, parent):
        pass


class CombinedModel(object):

    def __init__(self):
        self.items = [['Pet', 'Dog'], ['Pet', 'Cat'], ['Bird', 'Eagle'], ['Bird', 'Jay'], ['Bird', 'Falcon']]
        self.selectors = list({k[0] for k in self.items})
        self.table_if = TableModel(self)
        self.combo_if = ComboModel(self)
        self.currentSelection = None

    def currentItems(self):
        return [k[1] for k in self.items if k[0] == self.currentSelection]

    def setSelection(self, combo_row):
        self.currentSelection = self.selectors[combo_row]
        self.table_if.layoutChanged.emit()


# noinspection PyBroadException
class MyModel(QAbstractTableModel):
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

    # noinspection PyUnusedLocal
    def __init__(self, info=None, mesi=None, parent=None):
        super(MyModel, self).__init__(parent)
        if info is None:
            info = {}
        if mesi is None:
            mesi = [['dumb'] for x in range(0, 12)]
        self.oggi = QDate().currentDate()
        self._mesi = mesi
        self._date = self._mesi[self.oggi.month() - 1]
        self._info = info
        self.labelCreated = bool
        self.complexLabelsDict = Od()

    def setCurrentDate(self, dato: QDate = ...) -> QDate:
        self.currentDate = dato
        return self.currentDate

    def setDate(self, i):
        self._date = self._mesi[i]
        index = QModelIndex()
        self.dataChanged.emit(index, index)

    def setLabelCreated(self,flag):
        self.labelCreated = flag

    def data(self, index: QModelIndex, role: int = ...):

        try:
            row = index.row()
            col = index.column()

            if role == Qt.DisplayRole:
                # print(row,'|',col)

                dato = self._date[row][col]
                if index not in self.complexLabelsDict.keys():
                    label = complexLabel()
                    self.complexLabelsDict[index] = label
                label = self.complexLabelsDict[index]
                self.parent().setIndexWidget(index, label)
                label.setText(str(dato.day()))
                return
                # return dato.day()
            elif role == Qt.TextAlignmentRole:
                # return QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom
                return Qt.AlignHCenter | Qt.AlignVCenter
            elif role == Qt.BackgroundRole:
                dato = self._date[row][col]
                if dato in self._info.keys():
                    return QColor(Qt.cyan)
                # if col % 2 != 0:
                #     return QColor(Qt.darkRed)
                pass
            elif role == Qt.DecorationRole:
                pass
        except:
            print(fex())

    def flags(self, index: QModelIndex):
        try:
            if index.isValid():
                return Qt.ItemFlags() | Qt.ItemIsEnabled
        except:
            print(fex())

    def rowCount(self, parent: QModelIndex = ...) -> int:
        # print(parent.row())
        return 6

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 7

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        nomeGiorno = ''
        try:
            nomeGiorno = self._mesi[0][0][section].shortDayName(self._mesi[0][0][section].dayOfWeek())
        except IndexError:
            nomeGiorno = QDate().shortDayName(7)
        except:
            print('*************************** ', self._mesi)
            print(fex())

        weekEnd = [QDate().shortDayName(6), QDate().shortDayName(7)]
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return nomeGiorno

        if role == Qt.ForegroundRole:
            if nomeGiorno in weekEnd:
                return QColor(Qt.red)

        if role == Qt.BackgroundRole:  # necessario   CAMBIARE QAPPLICATION.SETSTYLE("FUSION")
            color = QColor('darkGray')
            brush = QBrush(color)
            return brush

    def setData(self, index, value, role=Qt.EditRole):

        if not index.isValid() or role != Qt.EditRole:
            return False

        self.lst[index.row()][index.column()] = value
        self.dataChanged.emit(index, index)
        return True

    def lastRoleName(self) -> int:
        last = max([r for r in self.roleNames().keys()])
        return last

    def setRoleNames(self, roleName):
        last = self.lastRoleName() + Qt.UserRole
        self.roleNames()[last] = roleName
