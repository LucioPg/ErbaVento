from PyQt5 import QtWidgets, QtCore
from mongoengine import *
from mongo.MongoConnection import MongoConnection
from kwidget.dialog_export.export_gui import Ui_Dialog_exp_fields as Dialog
from typing import *
from pymongo import MongoClient
import time
from dataclasses import dataclass





class DialogExport(Dialog, QtWidgets.QDialog):

    EXPORT_END = QtCore.pyqtSignal()

    def __init__(self, collezioni_dict: dict, connection_dict, parent=None):
        super(DialogExport, self).__init__(parent)
        self.setupUi(self)
        self.current_date = QtCore.QDate().currentDate()
        self.current_month = self.current_date.month()
        self.current_year = self.current_date.year()
        self.dateEdit_exp_dal.setDate(self.current_date.addMonths(-1))
        self.dateEdit_exp_al.setDate(self.current_date)
        self.collezioni_dict = collezioni_dict
        self.selected = []
        self.connection_dict = connection_dict
        self.fill_list()
        self.bot_toggle_select_all.clicked.connect(self.toggle_select_all)
        # self.bot_toggle_select_all.clicked.connect(self.toggle_select_all)
        self.bot_ok_export.clicked.connect(self.accept)
        self.bot_canc_export.clicked.connect(self.reject)
        self.status_toggle_all = True
        # self.test()

    def test(self):
        tops = ['a', 'b', 'c', 'd']
        dic = {ind: [str(ord(ind)), str(ord(ind) + 5)] for ind in tops}
        for top in dic:
            item = QtWidgets.QTreeWidgetItem()
            item.setText(0, top)
            self.treeWidget.insertTopLevelItem(0, item)
            children = [QtWidgets.QTreeWidgetItem() for item in dic[top]]
            for child, campo in zip(children, dic[top]):
                child.setText(0, campo)
            item.addChildren(children)

    def toggle_select_all(self):

        self.status_toggle_all = not self.status_toggle_all
        self.treeWidget.expandAll()
        if not self.status_toggle_all:
            self.label_toggle_select_all.setText('Deseleziona Tutto')
            self.treeWidget.selectAll()
            print('toggle_select_all')
        else:
            self.treeWidget.clearSelection()
            self.label_toggle_select_all.setText('Seleziona Tutto')

    def clear_all(self):
        # for row in range(self.listWidget.count()):
            # self.listWidget.takeItem(row)
        self.treeWidget.clear()

    def fill_list(self):
        self.clear_all()
        for collezione, documenti in self.collezioni_dict.items():
            # nome_file = f'{self.connection_dict.nome_db}_{collezione}.txt'
            item = QtWidgets.QTreeWidgetItem()
            item.setText(0, collezione)
            self.treeWidget.insertTopLevelItem(0, item)
            children = [QtWidgets.QTreeWidgetItem() for item in documenti]
            for child, campo in zip(children, documenti):
                child.setText(0, campo)
            item.addChildren(children)
            # self.treeWidget.setIte



    def fill_list_old(self):
        self.listWidget.clear()
        for row, collection in enumerate(self.collezioni_dict):
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
                # self.export_thread.start()
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
        self.host = self.connection_dict['host']
        self.port = int(self.connection_dict['port'])
        self.name = self.connection_dict['user']
        self.password = self.connection_dict['password']
        self.nome_db = self.connection_dict['nome_db']

    def run(self):
        myclient = MongoClient(host=self.host, port=27017)
        myclient[self.nome_db].authenticate(name=self.name, password=self.password)
        # db = myclient[self.nome_db]['prenotazione'].find_one()