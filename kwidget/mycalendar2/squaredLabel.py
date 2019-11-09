import sys
from traceback import format_exc as fex

from PyQt5.QtCore import (QDate, pyqtSignal, QSize, Qt,
                          QStringListModel, pyqtProperty, QModelIndex, QEvent)
from PyQt5.QtGui import (QFont, QStandardItemModel, QStandardItem, QResizeEvent, QIcon, QCloseEvent)
from PyQt5.QtWidgets import (QTableView, QWidget, QSizePolicy, QAbstractItemView, QHBoxLayout, QPushButton,
                             QComboBox, QVBoxLayout, QSizePolicy, QApplication, QLabel, QDialog,
                             QFrame, QGridLayout, QSpacerItem )


class SquaredLabel(QLabel):
    """ Label that remains squared when resized"""
    def __init__(self,parent=None):
        super(SquaredLabel, self).__init__(parent)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        size = self.size()
        w = size.width()
        h = size.height()
        if w != h:
            if w > h:
                h = w
            else:
                w = h
            self.resize(w,h)