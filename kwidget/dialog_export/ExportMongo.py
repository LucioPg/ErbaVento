from PyQt5 import QtWidgets, QtCore
from mongoengine import *
from mongo.MongoConnection import MongoConnection
from kwidget.dialog_export.export_gui import Ui_Dialog_exp_fields as Dialog
from kwidget.mydateedit.mydate_edit_3_main import My_dateedit_3
from typing import *
from pymongo import MongoClient
import time
from pprint import pprint
import csv
from dataclasses import dataclass





class DialogExport(Dialog, QtWidgets.QDialog):

    EXPORT_END = QtCore.pyqtSignal()

    def __init__(self, collezioni_dict: dict, connection_dict, parent=None):
        super(DialogExport, self).__init__(parent)
        self.setupUi(self)
        self.radio_exp_all.setChecked(True)
        self.prepare_date_edits()
        self.setWindowModality(QtCore.Qt.WindowModal)
        self.current_date = QtCore.QDate().currentDate()
        self.current_month = self.current_date.month()
        self.current_year = self.current_date.year()
        self.dateEdit_exp_dal.setDate(self.current_date.addMonths(-1))
        # self.dateEdit_exp_dal.dateEdit.setDate(self.current_date.addMonths(-1))
        # self.dateEdit_exp_al.dateEdit.setDate(self.current_date)
        self.dateEdit_exp_al.setDate(self.current_date)
        self.collezioni_dict = collezioni_dict
        self.selected = {}
        self.connection_dict = connection_dict
        print('----------------------------------------------', connection_dict)
        self.fill_list()
        self.bot_toggle_select_all.clicked.connect(self.toggle_select_all)
        # self.bot_toggle_select_all.clicked.connect(self.toggle_select_all)
        self.bot_ok_export.clicked.connect(self.accept)
        self.bot_canc_export.clicked.connect(self.reject)
        self.status_toggle_all = True
        # self.test()

    def prepare_date_edits(self):
        self.dateEdit_exp_dal = My_dateedit_3(self.dateEdit_exp_dal_wid)
        self.dateEdit_exp_al = My_dateedit_3(self.dateEdit_exp_al_wid)
        lay_dal = QtWidgets.QGridLayout()
        lay_dal.addWidget(self.dateEdit_exp_dal)
        self.dateEdit_exp_dal_wid.setLayout(lay_dal)
        lay_al = QtWidgets.QGridLayout()
        lay_al.addWidget(self.dateEdit_exp_al)
        self.dateEdit_exp_al_wid.setLayout(lay_al)
        self.dateEdit_exp_dal.dateEdit.dateChanged.connect(self.adjust_dates)
        # self.dateEdit_exp_al.dateEdit.setMinimumDate(self.dateEdit_exp_dal.date.addMonths(1))

    def adjust_dates(self):
        self.dateEdit_exp_al.dateEdit.setMinimumDate(self.dateEdit_exp_dal.date.addMonths(1))
        if self.dateEdit_exp_dal.date == self.dateEdit_exp_al.date:
            self.dateEdit_exp_al.setDate(self.dateEdit_exp_dal.date.addMonths(1))

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
        self.selected = self.treeWidget.get_selected()
        return self.selected

    def write_file_field(self,doc, campi:List):
        self.nome_file = self.connection_dict.nome_db + '_fields.txt'
        # campi = self.selected
        if campi:
            with open(self.nome_file, 'w') as f:
                stringa = ''.join([str(campo)+',' for campo in campi]).strip(',')
                f.write(stringa)
            return True
        else:
            return False

    def export_test(self):
        self.get_selected()
        # pprint(self.selected)
        # for doc, fields in self.selected.items():
        #     pass
        print('sto esportando...')
        try:
            # self.export_thread = ExportThread()
            self.export_thread = QtCore.QThread()

            def start():
                self.export_thread.start()

            # todo configure dates on the radio
            if self.radio_exp_all.isChecked():
                dates = []
            elif self.radio_exp_just_this_month:
                dates = []
            elif self.radio_exp_untill_this_month:
                dates = []
            else:
                dates = []
            self.export_engine = ExportEngine(self.selected, dates, self.connection_dict)
            self.export_engine.moveToThread(self.export_thread)
            #### il thread va spostato fuori dalla classe
            start()
            self.export_thread.started.connect(self.export_engine.run)
            self.export_engine.FINISHED.connect(self.export_thread.quit)
            # self.export_thread.start()
        except Exception as e:
            print(e)


    # def export(self):
    #     if self.write_file_field(campi=self.get_selected()):
    #         print('sto esportando...')
    #         try:
    #             # self.export_thread = ExportThread()
    #             self.export_thread = QtCore.QThread()
    #             def start():
    #                 self.export_thread.start()
    #             # todo configure dates on the radio
    #             if self.radio_exp_all.isChecked():
    #                 dates = []
    #             elif self.radio_exp_just_this_month:
    #                 dates = []
    #             elif self.radio_exp_untill_this_month:
    #                 dates = []
    #             self.export_engine = ExportEngine(self.nome_file, dates, self.connection_dict)
    #             self.export_engine.moveToThread(self.export_thread)
    #             #### il thread va spostato fuori dalla classe
    #             self.export_thread.started.connect(self.export_engine.run)
    #             # self.export_engine.FINISHED.connect(self.export_thread.quit)
    #             start()
    #
    #             # self.export_thread.start()
    #         except Exception as e:
    #             print(e)
    #     else:
    #         print('lista selezionati da esportare vuota')

    def export_end(self):
        try:
            self.export_thread.quit()
            self.EXPORT_END.emit()
            l = [1, 2, 3]
            stringa = ''.join([str(x)+',' for x in l]).strip(',')
        except Exception as e:
            print(e)



# class ExportThread(QtCore.QThread):
#
#     """ """
#     pass
    # def run(self):
    #     while True:
    #         pass
        # count = 0
        # while count < 5:
        #     time.sleep(1)
        #     print("sto esportando... ", count)
        #     count += 1

    # def finished(self) -> None:
    #     super(ExportThread, self).finished()

class ExportEngine(QtCore.QObject):

    FINISHED = QtCore.pyqtSignal()

    def __init__(self, selected: dict, dates: List, connection_dict):
        super(ExportEngine, self).__init__()
        self.selected = selected
        self.dates = dates
        self.connection_dict = connection_dict
        self.host = self.connection_dict.host
        self.port = int(self.connection_dict.port)
        self.name = self.connection_dict.user
        self.password = self.connection_dict.password
        self.nome_db = self.connection_dict.nome_db

    def run(self):
        print('run export engine')
        myclient = MongoClient(host=self.host, port=27017)
        myclient[self.nome_db].authenticate(name=self.name, password=self.password)
        # db = myclient[self.nome_db]['prenotazione'].find_one()
        time.sleep(2)
        db = myclient['test_db']['prenotazione']

        for x in db.find():
            print(x['arrivo'])
        # for doc, fields in self.selected.items():
        #     print(doc, type(doc))
        #     db = myclient['test_db']['prenotazione']
        #     # print(db['arrivo'].find_one())
        #     # db = clt['test_db']['prenotazione'].find_one()
        #     for x in db.find():
        #         print(x['ultima_notte'])
        #     # value = myclient[self.nome_db][doc].find()
        #     # for field in fields:
        #     #     print('\t'* len(doc), field)
        #     #     result = value[field]
        #     #     print(f'exported {doc}-{field}: {result}')
        self.FINISHED.emit()
        print('end export engine')

    def set_file_name(self, doc, dates):
        if dates:
            return f'{doc}_{dates[0]}-{dates[1]}.csv'
        else:
            return f'{doc}_all.csv'

    def get_info(self, doc, dates, fields):
        data_gen = self.dates_generator(dates[0])


    def dates_generator(self,first: QtCore.QDate):
        """ used for generate dates untill the selected upper limit"""
        yield first.addMonths(1)
