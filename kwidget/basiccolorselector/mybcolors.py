from PyQt5 import QtCore, QtWidgets, QtGui
from kwidget.basiccolorselector.gui_basiccolorselector import Ui_Form_colorSelector as Form


class MyBcolors(Form, QtWidgets.QDialog):
    def __init__(self, platform, platColors, parent=None):
        super(MyBcolors, self).__init__(parent)
        self.platform = platform
        self.a_string = """QPushButton{border:0px;
                        background-color: """
        self.b_string = """QPushButton::pressed{
                        background-color: rgb(255, 255, 255);}"""
        self.platColors = platColors
        self.setupUi(self)
        self.settaColori()
        # self.pushButton_4.clicked.connect(self.settaColori)

    def assegnaEchiudi(self):
        try:
            if type(self.sender()) is QtWidgets.QPushButton:
                bot = self.sender()
                # print(bot.objectName())
            else:
                return print('wrong sender: ', self.sender())

            bot.setText(self.platform)
            styleSheet = bot.styleSheet()
            if self.a_string in styleSheet:
                styleSheet = styleSheet.replace(self.a_string, '')
            if self.b_string in styleSheet:
                styleSheet = styleSheet.replace(self.b_string, '')
            if '}' in styleSheet:
                styleSheet = styleSheet.replace('}', '')
            if styleSheet not in self.platColors.values():
                self.platColors[self.platform] = styleSheet
            # print(styleSheet)
            return self.close()
        # templateNomePulsante = 'pushButton_'
        # try:
        #     for attr, value in QtCore.Qt.__dict__.items():
        #         print(attr, value)
        #         if value in range(4, 19):
        #             myStyleSheet = self.setMyStyleSheet(attr)
        #             nomePulsante = templateNomePulsante + str(value)
        #             for bot in self.children():
        #                 if nomePulsante == bot.objectName():
        #                     bot.setStyleSheet(myStyleSheet)
        #                     bot.setText('')
        #                     bot.setToolTip(attr)
        except:
            import traceback
            print(traceback.format_exc())

    def azione(self):
        pass

    def setMyStyleSheet(self, color):
        a = self.a_string
        b = self.b_string
        mystyleSheet = a + color + '}' + b
        # print(mystyleSheet)
        return mystyleSheet

    def settaColori(self):
        templateNomePulsante = 'pushButton_'

        # print( type(QtCore.Qt.red))
        try:
            for attr, value in QtCore.Qt.__dict__.items():
                # print(attr, value)
                if value in range(4, 19):
                    myStyleSheet = self.setMyStyleSheet(attr)
                    nomePulsante = templateNomePulsante + str(value)
                    for bot in self.children():
                        if nomePulsante == bot.objectName():
                            bot.setStyleSheet(myStyleSheet)
                            bot.setText('')
                            for p, c in self.platColors.items():
                                newColor = QtGui.QColor(attr)
                                if newColor.isValid():
                                    if QtGui.QColor(attr).name() == QtGui.QColor(c).name():
                                        bot.setText(p)
                                    else:
                                        bot.setToolTip(attr)
                                else:
                                    # print(QtGui.QColor(c).name(), '--->', QtGui.QColor(attr).name())
                                    bot.setToolTip(attr)
                            bot.clicked.connect(self.assegnaEchiudi)
            #             # bot.setStyleSheet(mystyleSheet)
        except:
            import traceback
            print(traceback.format_exc())


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    gui = MyBcolors('Booking')
    gui.show()
    sys.exit(app.exec_())
