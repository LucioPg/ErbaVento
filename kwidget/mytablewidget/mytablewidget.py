import sys

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget


class MyTableWidget(QTableWidget):
    EDITFINISHED = pyqtSignal(str)

    def __init__(self, parent=None):
        super(MyTableWidget, self).__init__(parent)
        self.insertRow(0)
        self.insertColumn(0)
        item = QTableWidgetItem()
        item.setText('ciao')
        self.setItem(0, 0, item)
        line = QLineEdit(self)
        line.setText('eccomi!!!')
        self.insertRow(1)
        self.setCellWidget(1, 0, line)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dia = QDialog()
    grid = QGridLayout(dia)
    mw = MyTableWidget(dia)
    grid.addWidget(mw)
    dia.setLayout(grid)
    dia.show()
    sys.exit(app.exec_())
