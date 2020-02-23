import sys

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from traceback import format_exc as fex


class MyTableWidget(QTableWidget):
    EDITFINISHED = pyqtSignal(type, int, type(Qt.Key_Tab))

    # NORMALFINISHED = pyqtSignal(QTableWidgetItem)
    # LINEFINISHED = pyqtSignal()

    def __init__(self, parent=None):
        super(MyTableWidget, self).__init__(parent)
        # self.EDITFINISHED.connect(lambda x: self.stampa(x))
        self.NORMALFINISHED_nome_comando = 'NORMALFINISHED'
        self.LINEFINISHED_nome_comando = 'LINEFINISHED'
        # print('rowcount ',self.rowCount())

    def setPyqtSignal(self, s):
        return pyqtSignal(type(s))

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Return or key == Qt.Key_Enter:
            # Process current item here
            row = self.currentRow()
            item = self.currentItem()
            if item is None:
                item = self.cellWidget(row, 1)
                # self.EDITFINISHED.emit(self.LINEFINISHED_nome_comando)
                # nome = self.LINEFINISHED_nome_comando
            else:
                # self.EDITFINISHED.emit(self.NORMALFINISHED_nome_comando)
                pass
            self.EDITFINISHED.emit(type(item), row, key)
        else:
            super(MyTableWidget, self).keyPressEvent(event)

    def stampa(self, row):
        if type(row) is tuple:
            print('MyTableWidget stampa row:', type(row[0]))
        else:
            print('MyTableWidget stampa row:', row)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dia = QDialog()
    grid = QGridLayout(dia)
    mw = MyTableWidget(dia)
    grid.addWidget(mw)
    dia.setLayout(grid)
    dia.show()
    sys.exit(app.exec_())
