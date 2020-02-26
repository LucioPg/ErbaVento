from PyQt5 import QtWidgets, QtCore
from mongoengine import *
from mongo.MongoConnection import MongoConnection
from kwidget.dialog_export.export_gui import Ui_Dialog_exp_fields as Dialog
from typing import *
import time
from dataclasses import dataclass





class DialogExport(Dialog, QtWidgets.QDialog):

    EXPORT_END = QtCore.pyqtSignal()

    def __init__(self, lista_collezioni:List, connection_dict, parent=None):
        super(DialogExport, self).__init__(parent)
        self.setupUi(self)
        self.lista_collezioni = lista_collezioni
        self.selected = []
        self.connection_dict = connection_dict
        self.fill_list()

    def clear_all(self):
        for row in range(self.listWidget.count()):
            self.listWidget.takeItem(row)

    def fill_list(self):
        self.listWidget.clear()
        for row, collection in enumerate(self.lista_collezioni):
            item = QtWidgets.QListWidgetItem(collection)
            self.listWidget.insertItem(row, item)

    def get_selected(self):
        rows = self.listWidget.count()
        self.selected.clear()
        for row in range(rows):
            campo = self.listWidget.item(row)
            if campo.isSelected():
                print(campo.text())
                self.selected.append(campo.text())

        return self.selected

    def write_file_field(self, campi:List):
        self.nome_file = self.connection_dict.nome_db + '_fields.txt'
        # campi = self.selected
        if campi:
            with open(self.nome_file, 'w') as f:
                stringa = ''.join([str(campo)+',' for campo in campi]).strip(',')
                f.write(stringa)
            return True
        else:
            return False

    def export(self):
        if self.write_file_field(campi=self.get_selected()):
            print('sto esportando...')
            try:
                self.export_thread = ExportThread()
                self.export_engine = ExportEngine(self.nome_file, self.connection_dict)
                self.export_engine.moveToThread(self.export_thread)
                #### il thread va spostato fuori dalla classe
                self.export_thread.started.connect(self.export_engine.run)
                self.export_thread.start()
                self.export_thread.start()
            except Exception as e:
                print(e)
        else:
            print('lista selezionati da esportare vuota')

    def export_end(self):
        try:
            self.export_thread.quit()
            self.EXPORT_END.emit()
            l = [1, 2, 3]
            stringa = ''.join([str(x)+',' for x in l]).strip(',')
        except Exception as e:
            print(e)



class ExportThread(QtCore.QThread):
    """ """
    def run(self):
        count = 0
        while count < 5:
            time.sleep(1)
            print("sto esportando... ", count)
            count += 1

    # def finished(self) -> None:
    #     super(ExportThread, self).finished()

class ExportEngine(QtCore.QObject):

    FINISHED = QtCore.pyqtSignal()

    def __init__(self, nome_file: str, connection_dict: dict):
        super(ExportEngine, self).__init__()
        self.nome_file = nome_file
        self.connection_dict = connection_dict

    def run(self):
        pass