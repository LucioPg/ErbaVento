from PyQt5 import QtCore, QtGui, QtWidgets
from gui_option import Ui_Dialog_opt as DialogOptionGui
import json
from copy import deepcopy
from traceback import format_exc as fex
import os


class DialogOption(DialogOptionGui, QtWidgets.QDialog):
    fileConf = 'config.json'
    defaultTasse = 1
    defaultTasseAttive = {'Booking': False,
                          'AirB&B': False,
                          'Privati': False}
    defaultPlatforms = {'Booking': QtGui.QColor(QtCore.Qt.cyan).name(),
                        'AirB&B': QtGui.QColor(QtCore.Qt.darkRed).name(),
                        'Privati': QtGui.QColor(QtCore.Qt.darkGreen).name()
                        }
    defaultImporti = {'Booking': [72, 74, 92, 111, 130],
                      'AirB&B': [64, 65, 85, 100, 117],
                      'Privati': [72, 74, 92, 111, 130]}
    defaultProvvigioni = {'Booking': 0.15, 'AirB&B': 0.03, 'Privati': 0}
    defaultConfig = {'numero letti': 5,
                     'platforms': defaultPlatforms,
                     'stagione': {
                         'Alta': {
                             'importi': defaultImporti
                         },
                         'Bassa': {
                             'importi': defaultImporti
                         },
                         'Media': {
                             'importi': defaultImporti
                         }
                     },
                     'provvigioni': {pl: prov for pl, prov in defaultProvvigioni.items()},
                     'stagione preferita': 'Media',
                     'tasse': defaultTasse,
                     'tasse attive': defaultTasseAttive
                     }
    config = {}

    def __init__(self, parent=None):
        super(DialogOption, self).__init__(parent)
        self.setupUi(self)
        # self.fileConf = '../../config.json'
        # self.defaultPlatforms = ['Booking',
        #                          'AirB&B',
        #                          'Privati'
        #                          ]
        # self.defaultImporti = {'Booking': [72, 74, 92, 111, 130],
        #                        'AirB&B': [64, 65, 85, 100, 117],
        #                        'Privati': [72, 74, 92, 111, 130]}
        # self.defaultProvvigioni = {'Booking': 0.15, 'AirB&B': 0.03, 'Privati': 0}
        # self.config = {}
        # self.defaultConfig = {'numero letti': 5,
        #                       'platforms': self.defaultPlatforms,
        #                       'stagione': {
        #                           'Alta': {
        #                                             'importi': self.defaultImporti
        #                                    },
        #                           'Bassa': {
        #                                              'importi': self.defaultImporti
        #                                     },
        #                           'Media': {
        #                                              'importi': self.defaultImporti
        #                                     }
        #                           },
        #                       'provvigioni': {pl: prov for pl, prov in self.defaultProvvigioni.items()}
        #                       }
        self.checkConfigFile()
        self.loadConfig()

        # funzione del menucontestuale
        addPlat = QtWidgets.QAction('Add...', self)
        removePlat = QtWidgets.QAction('Del...', self)
        addPlat.triggered.connect(self.addPlatform)
        removePlat.triggered.connect(self.removePlatform)
        self.combo_platform.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.combo_platform.customContextMenuRequested.connect(self.on_context_menu)
        self.popMenu = QtWidgets.QMenu(self)
        self.popMenu.addAction(addPlat)
        self.popMenu.addSeparator()
        self.popMenu.addAction(removePlat)

        # funzioni pulsanti
        self.bot_aggiungiLetto.clicked.connect(self.aggiungiLetto)
        self.bot_sottraiLetto.clicked.connect(self.sottraiLetto)
        self.buttonBox.accepted.connect(self.saveConfigBot)

        # funzioni comboBoxes
        self.combo_platform.currentTextChanged.connect(self.displayImporti)
        self.combo_stagione.currentIndexChanged.connect(self.displayImporti)

        # funzioni spinbox_provvigioni e tasse
        self.spinbox_provvigione.valueChanged.connect(self.setProvvigione)
        self.spinbox_tasse.valueChanged.connect(self.setTasse)

        # funzioni tableWidget
        self.tableWidget__importi.cellChanged.connect(self.setImporti)

    # def stampa(self, *args, **kwargs):
    #     print('args: ', args)
    #     print('kwargs: ', kwargs)

    def addPlatform(self):
        pass

    def aggiungiLetto(self):
        numeroAttuale = int(self.label_numeroLetti.text())
        numero = str(numeroAttuale + 1)
        self.setNumeroLetti(numero)
        self.config['numero letti'] = numero
        self.displayImporti()

    @classmethod
    def checkConfigFile(cls):
        try:
            fileConf = os.path.join(os.getcwd(), cls.fileConf)

            with open(fileConf, 'r') as fileconfig:
                config = json.load(fileconfig)
                cls.config = config
            # print(self.config)
        except FileNotFoundError:
            config = deepcopy(cls.defaultConfig)
            cls.config = config
            cls.saveConfig(cls.fileConf, cls.config)
            print('File di configurazione creato')
        return config

    def displayImporti(self):
        try:
            rows = int(self.label_numeroLetti.text())
            self.tableWidget__importi.setRowCount(rows)
            stagione, platform = self.getPlatStag()
            self.config['stagione preferita'] = stagione
            flagNuvoImporto = False
            for i in range(rows):
                itemNumero = QtWidgets.QTableWidgetItem()
                itemImporto = QtWidgets.QTableWidgetItem()
                itemNumero.setText(str(i + 1))
                try:
                    importo = self.config['stagione'][stagione]['importi'][platform][i]
                    itemImporto.setText(str(importo))
                except IndexError:
                    flagNuvoImporto = True

                self.tableWidget__importi.setItem(i, 0, itemNumero)
                self.tableWidget__importi.setItem(i, 1, itemImporto)
                if flagNuvoImporto:
                    self.setNuovoImporto()
            self.setProvvigione()
        except:
            print(fex())

    def getPlatStag(self):
        """
        ottiene la stagione e la platform dalle combo
        :return:
        """
        stagione = self.combo_stagione.currentText()
        platform = self.combo_platform.currentText()
        return stagione, platform

    def loadConfig(self):
        if self.checkConfigFile() is not None:
            self.spinbox_provvigione.setSingleStep(0.5)
            self.spinbox_tasse.setSingleStep(0.5)
            self.setNumeroLetti(str(self.config['numero letti']))
            self.displayImporti()
            self.setProvvigione()
            self.setTasse(self.config['tasse'])
            self.combo_stagione.setCurrentIndex(self.combo_stagione.findText(self.config['stagione preferita']))

    def on_context_menu(self, point):
        # show context menu
        self.popMenu.exec_(self.combo_platform.mapToGlobal(point))

    def removePlatform(self):
        pass

    @staticmethod
    def saveConfig(fileConf, config):
        with open(fileConf, 'w') as fileconfig:
            json.dump(config, fileconfig, indent=4, sort_keys=True)

    def saveConfigBot(self):
        fileConf = os.path.join(os.getcwd(), self.fileConf)
        self.saveConfig(fileConf, self.config)

    def setImporti(self, i=None):
        try:
            if i is not None:
                # row = i.row()
                row = i
                stagione, platform = self.getPlatStag()
                try:
                    importo = int(self.tableWidget__importi.item(row, 1).text())
                except ValueError:
                    importo = self.config['stagione'][stagione]['importi'][platform][row]
                    item = self.tableWidget__importi.item(row, 1)
                    item.setText(str(importo))
                self.config['stagione'][stagione]['importi'][platform][row] = importo

        except:
            print(fex())

    def setNumeroLetti(self, nl):
        self.label_numeroLetti.setText(nl)

    def setNuovoImporto(self):
        row = self.tableWidget__importi.rowCount()
        self.tableWidget__importi.setFocus(True)
        self.tableWidget__importi.scrollToBottom()
        item = self.tableWidget__importi.item(row - 1, 1)
        item.setSelected(True)
        self.tableWidget__importi.editItem(item)

    def setProvvigione(self, prov=None):
        stagione, platform = self.getPlatStag()
        try:
            if prov is not None:
                self.config['provvigioni'][platform] = prov
            else:
                prov = self.config['provvigioni'][platform]
                self.spinbox_provvigione.setValue(prov)
        except:
            for k, v in self.config['stagione'].items():
                print(k, '       ', v)
            # print(self.config.keys())

    def setProvvigioniDefault(self, plat, prov):
        self.defaultProvvigioni[plat] = prov

    def setTasse(self, tassa=None):
        if tassa is None:
            tassa = self.defaultTasse
        self.config['tasse'] = tassa
        self.spinbox_tasse.setValue(float(tassa))

    def sottraiLetto(self):
        numeroAttuale = int(self.label_numeroLetti.text())
        if numeroAttuale == 0:
            return
        numero = str(numeroAttuale - 1)
        self.setNumeroLetti(numero)
        self.config['numero letti'] = numero
        if int(numero) > 0:
            self.tableWidget__importi.setRowCount(int(numero))



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = DialogOption()
    ui.show()
    sys.exit(app.exec_())
