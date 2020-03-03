from kwidget.dialog_info.dialog_info import Ui_Dialog as GuiText
from kwidget.dialog_info.gui_dialog_infoSpese import Ui_DialogInfoSpese as GuiTable
from kwidget.singleline.singleline import MySimpleLinEditDialog as SimpleLine
# from kwidget.mytablewidget.mytablewidget import MyTableWidget
from PyQt5 import QtCore, QtGui
from copy import deepcopy as deepc
from traceback import format_exc as fex
from PyQt5.QtWidgets import *


class LabelSettable(QLabel):
    DCSignal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(LabelSettable, self).__init__(parent)

    def mouseDoubleClickEvent(self, event):
        dia = SimpleLine(icon=self.optIcon)
        dia.setWindowTitle('Nuova Spesa')
        dia.setWindowTitle(dia.newPlat)
        if dia.exec_():
            nome = dia.newPlat
            if nome != '':
                self.text(dia.newPlat)
        return QLabel.mouseDoubleClickEvent(event)


class LineEditNum(QLineEdit):
    TABPRESSED = QtCore.pyqtSignal(bool)
    TABPRESSEDTYPE = QtCore.pyqtSignal(type, int, type(QtCore.Qt.Key_Tab))

    def __init__(self, row, parent=None):
        super(LineEditNum, self).__init__(parent)
        shortcut = QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Tab), self,
                             context=QtCore.Qt.WidgetWithChildrenShortcut, activated=self.do_something)
        self.row = row

    @QtCore.pyqtSlot()
    def do_something(self):
        print("do_something")
        flag = self.filtraNum(self.text())
        if not flag:
            self.clear()
        self.TABPRESSED.emit(flag)
        try:
            self.TABPRESSEDTYPE.emit(type(self), self.row, QtCore.Qt.Key_Tab)
        except:
            print(fex())
        return flag

    def setTextFiltered(self, p_):
        p_str = str(p_)
        if self.filtraNum(p_str):
            return self.setText(p_str)
        else:
            return self.setText('')

    def filtraNum(self, num):
        lista = str(num)
        for ch in lista:
            if '0' <= ch <= '9' or ch == '.' or ch == ',':
                pass
            else:
                return False
        return True


class LabLine(QWidget):
    def __init__(self, parent=None):
        super(LabLine, self).__init__(parent)
        self.nome = self.setNome('')
        self.hbox = QHBoxLayout()
        self.label = LabelSettable(parent)
        self.label.setMinimumSize(QtCore.QSize(90, 30))
        self.label.setText(self.nome)
        self.setObjectName(self.nome)
        self.lineEdit = LineEditNum(self)
        self.lineEdit.setMinimumSize(QtCore.QSize(90, 30))
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.label.setSizePolicy(sizePolicy)
        self.lineEdit.setSizePolicy(sizePolicy)
        self.hbox.addWidget(self.label)
        self.hbox.addWidget(self.lineEdit)

    def setLabel(self):
        self.label.setText(self.nome)

    def setNome(self, nome):
        self.nome = nome
        return self.nome


class DialogInfoSpese(GuiTable, QDialog):
    SPESEPRONTE = QtCore.pyqtSignal(dict)

    def __init__(self, spese: dict, parent=None):
        print('dialog spese')
        super(DialogInfoSpese, self).__init__(parent)
        self.setupUi(self)
        # self.setModal(True)
        self.listaTipi = []
        self.spese = spese
        self.vecchieSpese = deepc(self.spese)
        self.tableWidget.setRowCount(0)
        self.riempiTable()
        # self.setWindowModality(QtCore.Qt.WindowModal)
        self.tableWidget.itemChanged.connect(lambda x: self.gotoLine(x.row()))
        self.bot_addLine.clicked.connect(self.addNewLine)
        self.bot_removeLine.clicked.connect(self.cancellaSpesa)
        self.bot_ok.clicked.connect(self.accept)
        self.bot_esci.clicked.connect(self.close)
        self.tableWidget.EDITFINISHED.connect(self.returnPressed)
        # self.show()

    def addLine(self, new=False, nome='Nuova Spesa', euro=0):
        def updateTypes(self, tipo):
            if tipo not in self.listaTipi:
                self.listaTipi.append(tipo)

        try:
            self.tableWidget.blockSignals(True)
            itemNome = QTableWidgetItem(nome)
            updateTypes(self, type(itemNome))
            row = self.tableWidget.rowCount()
            print('table dialog info spese, row: ', row)
            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row, 0, itemNome)
            line = LineEditNum(row=row, parent=self.tableWidget)
            updateTypes(self, type(line))
            line.setTextFiltered(euro)
            line.TABPRESSEDTYPE.connect(lambda x, y, k: self.returnPressed(type(line), row, QtCore.Qt.Key_Tab))
            # line.returnPressed.connect()
            self.tableWidget.setCellWidget(row, 1, line)
            self.tableWidget.blockSignals(False)
            if new:
                self.tableWidget.setCurrentCell(row, 0)
                # self.bot_removeLine.blockSignals(True)
                self.tableWidget.editItem(self.tableWidget.item(row, 0))


        except:
            print(fex())

    def addNewLine(self):
        self.addLine(new=True)

    def cancellaSpesa(self):
        row = self.tableWidget.currentRow()
        print('spesa cancellata ', row)
        row_count = self.tableWidget.rowCount()
        if row_count:
            self.tableWidget.removeRow(row)
        else:
            self.tableWidget.setRowCount(0)
            self.addNewLine()

    def gotoLine(self, row):
        try:
            line = self.tableWidget.cellWidget(row, 1)
            line.setFocus()
            line.selectAll()
        except:
            print(fex())


    def ottieniSpese(self):
        rows = self.tableWidget.rowCount()
        spese = {}
        for row in range(rows):
            itemR = self.tableWidget.cellWidget(row, 1)
            valore = itemR.text()
            try:
                valRow = float(valore)
            except ValueError:
                if ',' in itemR.text():
                    valore = valore.replace(',','.')
                valRow = float(valore)
            if valRow == 0:
                continue
            itemC = self.tableWidget.item(row, 0)
            chiaveCol = itemC.text()
            spese[chiaveCol] = spese.get(chiaveCol, 0.0) + valRow
            # spese[chiaveCol] = valRow
        self.spese = deepc(spese)
        self.SPESEPRONTE.emit(self.spese)
        return self.spese

    def returnPressed(self, tipoItem, row, key):
        print('returnPressed', self)
        if tipoItem is QTableWidgetItem:
            print('devo passare alla lineEdit')
            self.gotoLine(row)
        elif tipoItem is LineEditNum:
            if row < self.tableWidget.rowCount() - 1:
                print('minore')
                self.gotoLine(row + 1)
            else:
                print('sposto il focus sul pulsante ok')
                if key == QtCore.Qt.Key_Tab:
                    print('sposto il focus sul pulsante +')
                    self.bot_addLine.setFocus()
                else:
                    pass
                # print('sposto il focus sul pulsante +')
                # self.bot_addLine.setFocus()

    def riempiTable(self):
        if self.spese is None:
            print('dialogInfoSpese: il dizionario spese è None')
            return
        if len(self.spese) == 0:
            self.addNewLine()
        else:
            for nome, euro in self.spese.items():
                self.addLine(nome=nome, euro=euro)


class DialogInfo(QDialog):
    def __init__(self, tipo='Note', testo='', showBool=False, table=False, parent=None):
        super(DialogInfo, self).__init__(parent)
        self.tipo = tipo
        self.testo = testo
        self.showBool = showBool

        if not table:
            self.guiText = GuiText()
            self.guiText.setupUi(Dialog=self)
            # print("self.testo ", self.testo)
            try:
                self.guiText.textBrowser_dialog_info.setText(self.testo)
            except:
                import traceback
                print(traceback.format_exc())
            if not self.showBool:
                if self.tipo == 'Note':
                    self.guiText.label_dialog_info.setText('Note')
                    self.guiText.textBrowser_dialog_info.setReadOnly(True)
                else:
                    self.guiText.label_dialog_info.setText('Spese')
                    self.guiText.textBrowser_dialog_info.setReadOnly(False)
            else:
                if self.tipo == 'Note':
                    self.guiText.label_dialog_info.setText('Note')
                    self.guiText.textBrowser_dialog_info.setReadOnly(False)
                else:
                    self.guiText.label_dialog_info.setText('Spese')
                    self.guiText.textBrowser_dialog_info.setReadOnly(False)
        else:
            self.guiTable = GuiTable()
            self.guiTable.setupUi(self)
        # self.show()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    # Dialog = QDialog()
    # ui = DialogInfo('Spese')
    spesa = {'caffé': 2.99, 'latte': 1.5}
    ui = DialogInfoSpese(spesa)
    # ui.setupUi(Dialog)
    # Dialog.show()
    sys.exit(app.exec_())
