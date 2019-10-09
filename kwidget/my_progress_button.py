"""

"""
from PyQt5.QtWidgets import QProgressBar, QApplication
from PyQt5 import QtCore, QtGui
import sys


class MyProgressButton(QProgressBar):
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
    a = MyProgressButton()
    a.setActive(1)
    a.show()
    print(a.style().CE_ProgressBarGroove)
    sys.exit(app.exec_())
