from PyQt5 import QtWidgets, QtCore
from mongoengine import *
from mongo.MongoConnection import MongoConnection
from kwidget.dialog_export.export_gui import Ui_Dialog_exp_fields as Dialog
from typing import *
import time
from dataclasses import dataclass





class DialogExport(Dialog, QtWidgets.QDialog):

    EXPORT_END = QtCore.pyqtSignal()

    def __init__(self, collections:List, connection_dict, parent=None):
        super(DialogExport, self).__init__(parent)
        self.setupUi(self)
        self.collections = collections
        self.connection = connection_dict

    def clear_all(self):
        for row in range(self.listWidget.count()):
            self.listWidget.takeItem(row)

    def fill_list(self):
        self.listWidget.clear()
        for row, collection in enumerate(self.collections):
            item = QtWidgets.QListWidgetItem(collection)
            self.listWidget.insertItem(row, item)

    def write_file_field(self, nome_file, campi:List):
        with open(nome_file, 'w') as f:
            stringa = ''

            f.write(str(campi))

    def export(self):
        thread = ExportThread()
        thread.finished.connect(self.export_end)
        thread.start()

    def export_end(self):
        self.EXPORT_END.emit()
        l = [1, 2, 3]
        stringa = ''.join([str(x)+',' for x in l]).strip(',')



class ExportThread(QtCore.QThread):
    """ """
    def run(self):
        count = 0
        while count < 5:
            time.sleep(1)
            print("A Increasing ", count)
            count += 1

    # def finished(self) -> None:
    #     super(ExportThread, self).finished()

class ExportEngine(QtCore.QObject):

    FINISHED = QtCore.pyqtSignal()

    def __init__(self):
        super(ExportEngine, self).__init__()

    def run(self):
        pass