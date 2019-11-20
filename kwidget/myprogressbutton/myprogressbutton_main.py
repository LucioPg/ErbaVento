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
from traceback import format_exc as fex


noteButton = Note()
speseButton = Spese()
verde = Verde()
rosso = Rosso()


class ColorButton(QPushButton):
    statoCambiato = QtCore.pyqtSignal(bool)
    tipoSpese = """QPushButton{background-color: rgba(255, 50, 50, 150);}
                                QPushButton::pressed{background-color: rgba(155, 10, 10, 150);}"""

    tipoNote = """QPushButton{background-color: rgba(170, 255, 127, 150);}
                                    QPushButton::pressed{background-color: rgba(70, 155, 27, 150);}"""

    def __init__(self, parent=None, tipo=''):
        super(ColorButton, self).__init__(parent)
        if tipo == '':
            tipo = 'spese'
        self.tipo = tipo
        self.state = False
        self.statoCambiato.connect(self.changeColor)

    # @QtCore.pyqtSlot()
    def changeColor(self, state):
        if state:
            if self.tipo == 'spese':
                self.setStyleSheet(self.tipoSpese)
            elif self.tipo == 'note':
                self.setStyleSheet(self.tipoNote)
        else:
            self.setStyleSheet("""""")

    def setState(self, state: bool):

        self.state = state
        self.statoCambiato.emit(state)

    def setTipo(self,tipo: str):
        self.tipo = tipo

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
        if info is not None and type(info) is str:
            if info != '':
                self.info = info
                print('informazioni ricevute, ', self._text)
                return True
            else:
                return False
        elif type(info) is dict:
            self.info = 'is a dict'
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
            self.MPB_signal.emit(self._text)



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
