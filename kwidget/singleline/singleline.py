from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from traceback import format_exc as fex


class MySimpleLineEdit(QLineEdit):
    ECCETESTE = QtCore.pyqtSignal(str)
    keyPressed = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(MySimpleLineEdit, self).__init__(parent)

    # def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
    #     self.ECCETESTE.emit(self._text)
    #     return QLineEdit.closeEvent(a0)

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        try:
            # print('key ',type(a0.key()))
            # self.keyPressed.emit(a0.key())
            self.on_key(a0.key())
        except:
            print(fex())
        return super(MySimpleLineEdit, self).keyPressEvent(a0)

    @QtCore.pyqtSlot()
    def on_key(self, a0):
        if a0 == (QtCore.Qt.Key_Return or QtCore.Qt.Key_Enter):
            print("key pressed")
            text = self.getText()
            self.ECCETESTE.emit(text)

    def getText(self):
        text = self.text()
        return text


class MySimpleLinEditDialog(QDialog):
    def __init__(self, icon=None, parent=None):
        super(MySimpleLinEditDialog, self).__init__(parent)
        self.newPlat = ''
        self.optIcon = icon
        if self.optIcon is not None:
            self.setWindowIcon(self.optIcon)
        self.setWindowTitle('Inserire il nome della nuova piattaforma')
        wid = QWidget(self)
        # self.setWindowModality(QtCore.Qt.WindowModal)
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        grid = QGridLayout()
        self.lineEdit = MySimpleLineEdit(wid)
        grid.addWidget(self.lineEdit)
        wid.setLayout(grid)
        hbox = QHBoxLayout()
        hbox.addWidget(wid)
        self.setLayout(hbox)
        self.lineEdit.ECCETESTE.connect(self.setNewPlat)

    def setNewPlat(self, plat):
        self.newPlat = plat
        self.accept()
