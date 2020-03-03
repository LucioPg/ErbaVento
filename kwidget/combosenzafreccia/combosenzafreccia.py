from PyQt5 import QtWidgets, QtCore, QtGui

import sys
from traceback import format_exc as fex


class ComboSenzaFreccia(QtWidgets.QComboBox):
    whoIsComing = QtCore.pyqtSignal(QtWidgets.QWidget)
    def __init__(self,parent=None):
        super(ComboSenzaFreccia, self).__init__(parent)
        self.setStyleSheet ("""QComboBox::drop-down {border-width: 0px;} QComboBox::down-arrow {image: url(noimg); border-width: 0px;} QComboBox {border: 0px; background-color:qlineargradient(spread:reflect, x1:0.5, y1:0, x2:1, y2:0, stop:0.511364 rgba(102, 191, 255, 214), stop:1 rgba(0, 0, 0, 0));}""")
        self.setMaxVisibleItems(12)
        self.setMaxCount(12)
        # self.setModelColumn(0)
        self.setObjectName("comboSenzaFreccia")
        # self.setEditable(True)
        # self.lineEdit().setReadOnly(True)
        # self.currentIndexChanged.connect(self.setAlign)
    def setUpFont(self,font=QtGui.QFont('Arial', 17,)):
        self.setFont(font)

    def paintEvent(self, e: QtGui.QPaintEvent) -> None:
        try:

            painter = QtWidgets.QStylePainter(self)
            painter.setPen(QtCore.Qt.white)
            font = QtGui.QFont('Arial', 17,)
            painter.setFont(font)
            option = QtWidgets.QStyleOptionComboBox()
            self.initStyleOption(option)
            painter.drawComplexControl(QtWidgets.QStyle.CC_ComboBox, option)
            textRect = QtWidgets.qApp.style().subControlRect(QtWidgets.QStyle.CC_ComboBox, option,
                                                         QtWidgets.QStyle.SC_ComboBoxEditField, self)

            painter.drawItemText(
                textRect.adjusted(-1,1,-1,1),
                QtWidgets.qApp.style().visualAlignment(self.layoutDirection(), QtCore.Qt.AlignCenter),
                self.palette(), self.isEnabled(),
                self.fontMetrics().elidedText(self.currentText(), QtCore.Qt.ElideRight, textRect.width())
            )
        except:
            print(fex())

    def setAlign(self):
        for i in range(self.count()):
            data = self.itemText(i)
            self.setItemData(i,QtCore.Qt.AlignCenter, QtCore.Qt.TextAlignmentRole)




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dia = QtWidgets.QDialog()
    com1 = QtWidgets.QComboBox(dia)
    com1.addItems(['ciao','combo1'])
    com2 = ComboSenzaFreccia(dia)
    com2.addItems(['hello','combo2'])
    # com1.show()
    vbox = QtWidgets.QVBoxLayout()
    vbox.addWidget(com1)
    vbox.addWidget(com2)
    dia.setLayout(vbox)
    dia.show()
    sys.exit(app.exec_())