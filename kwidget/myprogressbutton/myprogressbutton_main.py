"""
Strategy pattern per qprogress bar con funzionalità di pulsante
"""

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
import sys
from kwidget.myprogressbutton.strategy import NoteText_MPBStrategy as Note
from kwidget.myprogressbutton.strategy import SpeseText_MPBStrategy as Spese
from kwidget.myprogressbutton.strategy import Green_ColorMPBStrategy as Verde
from kwidget.myprogressbutton.strategy import Red_ColorMPBStrategy as Rosso


noteButton = Note()
speseButton = Spese()
verde = Verde()
rosso = Rosso()


class ProgressButton(QProgressBar):
    MPB_signal = QtCore.pyqtSignal(str)

    def __init__(self, text_strategy, color_strategy, parent):
        super().__init__(parent)
        self._setText_strategy = text_strategy
        self._setColor_strategy = color_strategy
        self._text = text_strategy._text
        self.setStyleSheet(self._setColor_strategy.show_color())
        self._value = 0
        self.setRange(0, 0)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.act_status = False
        self.nome = self._setColor_strategy.nome()
        self.setActive(False)
        self.info = None

    @QtCore.pyqtSlot(bool)
    def setActive(self, status):
        if status:
            val = 0
        else:
            val = 100
        self.setMaximum(val)
        self.act_status = status
        # print(self.nome, " status: ", status)
        return self.act_status

    def setInfo(self, info):
        """
        le info possono essere le note o la lista della spesa
        :param info:
        :return:
        """
        if info is not None:
            if info != '':
                self.info = info
                print('informazioni ricevute, ', self._text)
                return True
            else:
                return False
        else:
            return False


    def text(self):
        return self._text

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        # print(self.func)
        # todo cambiare l'emissione di self.nome con le note o le spese
        # todo passate dal mittente
        # self.MPB_signal.emit(self.info)
        # todo da rimuovere il print
        if self.act_status:
            print("CIAOOO da ", self.text())
            self.MPB_signal.emit(self.info)



class GreenProgressButton(ProgressButton):
    def __init__(self, parent):
        super(GreenProgressButton, self).__init__(noteButton, verde, parent)
        # self.nome = "green progress button"

    def setText(self, text):
        self._text = text


class RedProgressButton(ProgressButton):
    def __init__(self, parent):
        super(RedProgressButton, self).__init__(speseButton, rosso, parent)

    def setText(self, text):
        self._text = text


class MainW(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Hello, world!'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.centralwidget = self
        self.speseBar = RedProgressButton(self)
        self.speseBar.setActive(True)
        self.noteBar = GreenProgressButton(self)
        self.noteBar.setActive(False)
        self.noteBar.MPB_signal.connect(self.showText)
        self.speseBar.MPB_signal.connect(self.showText)
        self.initUI()

    def initUI(self):
        wid = QWidget(self)
        self.setCentralWidget(wid)
        self.bot = QPushButton('Click me', self)
        self.gridLayout = QGridLayout(wid)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.addWidget(self.speseBar)
        self.gridLayout.addWidget(self.noteBar)
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.statusBar().showMessage('In progress')  # Added
        wid.setLayout(self.gridLayout)
        self.show()

    @QtCore.pyqtSlot(str)
    def showText(self, nome):
        self.bot.setText(nome)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainW()
    sys.exit(app.exec_())
