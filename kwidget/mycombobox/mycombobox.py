import sys

from PyQt5.QtCore import QEvent
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget


class MyWidget(QComboBox):

    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)
        self.installEventFilter(self)

    def eventFilter(self, QObject, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.RightButton:
                print("Right button clicked")
        return super(MyWidget, self).eventFilter(QObject, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dia = QDialog()
    grid = QGridLayout(dia)
    mw = MyWidget(dia)
    grid.addWidget(mw)
    dia.setLayout(grid)
    dia.show()
    sys.exit(app.exec_())
