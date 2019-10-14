"""

"""

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
import sys
# from strategy import N as Note
# from ./strategy import SpeseText_MPBStrategy as Spese
from kwidget.myprogressbutton.strategy import NoteText_MPBStrategy as Note
from kwidget.myprogressbutton.strategy import SpeseText_MPBStrategy as Spese
from kwidget.myprogressbutton.strategy import Green_ColorMPBStrategy as Verde
from kwidget.myprogressbutton.strategy import Red_ColorMPBStrategy as Rosso


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
        # self.noteBar = QProgressBar(self)
        # self.noteBar.setValue(100)
        # self.noteBar = ProgressButton(Note(),Verde(),self)
        # self.noteBar = MyProgressButton_old(parent=self)
        # self.bot = QPushButton('ciao',self)
        # self.bot.setText('ciao')
        # self.gridLayout = QGridLayout(self)
        # self.gridLayout.setObjectName("gridLayout")
        # self.gridLayout.addWidget(self.bot)
        self.initUI()

    def initUI(self):
        wid = QWidget(self)
        self.setCentralWidget(wid)
        # self.bot = QPushButton('Click me', self)
        # self.bot.setText('ciao')
        self.gridLayout = QGridLayout(wid)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.addWidget(self.speseBar)
        self.gridLayout.addWidget(self.noteBar)
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.statusBar().showMessage('In progress')  # Added
        wid.setLayout(self.gridLayout)
        self.show()




noteButton = Note()
speseButton = Spese()
verde = Verde()
rosso = Rosso()


class ProgressButton(QProgressBar):

    def __init__(self, text_strategy, color_strategy, parent):
        super().__init__(parent)
        self._setText_strategy = text_strategy
        self._setColor_strategy = color_strategy
        self._text = text_strategy._text
        self.setStyleSheet(self._setColor_strategy.show_color())
        # self._text = 'porca troia'
        self._value = 0
        self.setRange(0, 0)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.act_status = False
        self.nome = self._setColor_strategy.nome()

        # self.setText(text_strategy._text)
        # self.setText(text_strategy._text)
        # self.setText('aaaaaaaah')
        # self.showText()

    def setActive(self, status):
        if status:
            val = 0
        else:
            val = 100
        self.setMaximum(val)
        self.act_status = status
        print(self.nome, " status: ", status)
        return self.act_status

    def showText(self):
        print(self._text)
        return self._text

    def text(self):
        return self._text
# Types of Ducks


class GreenProgressButton(ProgressButton):
    def __init__(self, parent):
        super(GreenProgressButton, self).__init__(noteButton, verde, parent)
        # self.nome = "green progress button"

    def setText(self, text):
        self._text = text


class RedProgressButton(ProgressButton):
    def __init__(self, parent):
        super(RedProgressButton, self).__init__(speseButton, rosso, parent)
        # self.nome = "red progress button"
        # self.setText('Spese')

    def setText(self, text):
        self._text = text


class MyProgressButton_old(QProgressBar):
    """
        Progress bar in busy mode with text displayed at the center.
    """
    DEFAULTSTYLE = """
    QProgressBar::chunk {background-color:qlineargradient(spread:reflect, x1:1, y1:0, x2:0.500455, y2:0, stop:0.414773 rgba(255, 255, 255, 20), stop:1 rgba(0, 255, 61, 255))}
    QProgressBar{border: 0px solid red;background-color: rgba(255, 255, 255,0);};
    font: 175 16pt \"MS Shell Dlg 2\";
    
    
    """

    def __init__(self, parent=None, text='Note'):
        super().__init__(parent=None)
        self.parent = parent
        self.setRange(0, 0)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self._text = None
        self.act_status = False
        self.setStyleSheet(self.DEFAULTSTYLE)

        # self.setStyleSheet(self.styleSheet()+"font: 175 110pt \"MS Shell Dlg 2\";")
        # self.setStyleSheet(stylelist[0]+stylelist[1])
        self.setText(text)
        self.setObjectName('progressBarButton')

    def setText(self, text):
        if type(text) is not str:
            text = str(text)
        self._text = text

    def setActive(self, act):
        if not act:
            self.setRange(0, 100)
        else:
            self.setRange(0, 0)
        self.act_status = act
        return self.act_status

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        print(self.objectName())
    def text(self):
        return self._text


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainW()
    # print(main.noteBar.parent())
    # main.initUI()
    # lay = QGridLayout(main)
    # lab = QLabel(main)
    # lab2 = QLabel(main)
    # lab.setText('CIAO')
    # lab2.setText('2222')
    # hbox = QHBoxLayout()
    # hbox.addWidget(lab)
    # hbox.addWidget(lab2)
    # lay.addLayout(hbox,0,0,0,0)
    # main.setLayout(hbox)
    # main.layout().addWidget(lab)
    # main.layout().addWidget(lab)
    # main.addWidget(lab,0,0,0,1)
    # lay.addWidget(lab2,0,0,0,0)
    # lay.addWidget(lab2,0,0,0,0)

    # print(main.layout().addWidget(lab))
    # main.setLayout(lay)
    # main.show()
    # a = MyProgressButton()
    # a.setActive(1)
    # a.show()
    # print(a.style().CE_ProgressBarGroove)
    # sys.exit(app.exec_())

    # note = GreenProgressButton()
    #
    #
    # spese = RedProgressButton()
    #
    # note.showText()
    # note.setText('NOTE')
    # note.showText()
    # spese.showText()
    # note.show()
    # spese.show()
    sys.exit(app.exec_())
