"""

"""
from PyQt5.QtWidgets import QProgressBar, QApplication
from PyQt5 import QtCore
import sys


class MyProgressButton(QProgressBar):
    """
        Progress bar in busy mode with text displayed at the center.
    """

    def __init__(self, text='Note'):
        super().__init__()
        self.setRange(0, 0)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self._text = None
        self.act_status = False
        self.setStyleSheet("font: 75 11pt \"MS Shell Dlg 2\";")
        self.setText(text)

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

    def text(self):
        return self._text


if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = MyProgressButton()
    a.setActive(0)
    a.show()
    sys.exit(app.exec_())
