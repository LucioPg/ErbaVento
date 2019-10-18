from kwidget.dialog_info.dialog_info import Ui_Dialog as Gui
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *


class DialogInfo(QDialog):
    def __init__(self, tipo, showBool=False, parent=None):
        super(DialogInfo, self).__init__(parent)
        self.tipo = tipo
        self.showBool = showBool
        self.gui = Gui()
        self.gui.setupUi(Dialog=self)
        if not self.showBool:
            if self.tipo == 'Note':
                self.gui.label_dialog_info.setText('Note')
                self.gui.textBrowser_dialog_info.setReadOnly(True)
            else:
                self.gui.label_dialog_info.setText('Spese')
                self.gui.textBrowser_dialog_info.setReadOnly(False)
        else:
            if self.tipo == 'Note':
                self.gui.label_dialog_info.setText('Note')
                self.gui.textBrowser_dialog_info.setReadOnly(False)
            else:
                self.gui.label_dialog_info.setText('Spese')
                self.gui.textBrowser_dialog_info.setReadOnly(False)
        self.show()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    # Dialog = QDialog()
    ui = DialogInfo('Spese')
    # ui.setupUi(Dialog)
    # Dialog.show()
    sys.exit(app.exec_())
