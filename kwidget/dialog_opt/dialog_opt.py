from PyQt5 import QtCore, QtGui, QtWidgets
from gui_option import Ui_Dialog_opt as DialogOptionGui
import json
from copy import deepcopy
from traceback import format_exc as fex


class DialogOption(DialogOptionGui, QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(DialogOption, self).__init__(parent)
        self.setupUi(self)
        self.fileConf = '../../config.json'
        self.defaultPlatforms = ['Booking',
                                 'AirB&B',
                                 'Privati'
                                 ]
        self.defaultImporti = {'Booking': [72, 74, 92, 111, 130],
                               'AirB&B': [64, 65, 85, 100, 117],
                               'Privati': [72, 74, 92, 111, 130]}
        self.defaultProvvigioni = {'Booking.com': 0.15, 'AirB&B': 0.03, 'Privati': 0}
        self.config = {}
        self.defaultConfig = {'numero letti': 5,
                              'platforms': self.defaultPlatforms,
                              'stagione': {
                                  'Alta': {'provvigioni': {pl: prov for pl, prov in self.defaultProvvigioni.items()},
                                                    'importi': self.defaultImporti
                                           },
                                  'Bassa': {'provvigioni': {pl: prov for pl, prov in self.defaultProvvigioni.items()},
                                                     'importi': self.defaultImporti
                                            },
                                  'Media': {'provvigioni': {pl: prov for pl, prov in self.defaultProvvigioni.items()},
                                                     'importi': self.defaultImporti
                                            }
                                  },
                              }
        self.checkConfigFile()
        self.loadConfig()
        # funzioni pulsanti
        self.bot_aggiungiLetto.clicked.connect(self.aggiungiLetto)
        self.bot_sottraiLetto.clicked.connect(self.sottraiLetto)

        # funzioni comboBoxes
        self.combo_platform.currentTextChanged.connect(self.displayImporti)
        self.combo_stagione.currentIndexChanged.connect(self.displayImporti)

    def aggiungiLetto(self):
        try:
            numeroAttuale = int(self.label_numeroLetti.text())
            numero = str(numeroAttuale + 1)
            self.setNumeroLetti(numero)
            self.config['numero letti'] = numero
            self.displayImporti()
        except:
            print(fex())

    def sottraiLetto(self):
        try:
            numeroAttuale = int(self.label_numeroLetti.text())
            if numeroAttuale == 0:
                return
            numero = str(numeroAttuale - 1)
            self.setNumeroLetti(numero)
            self.config['numero letti'] = numero
            if int(numero) > 0:
                self.tableWidget__importi.setRowCount(int(numero))
        except:
            print(fex())

    def setNumeroLetti(self, nl):
        self.label_numeroLetti.setText(nl)

    def setProvvigioni(self, plat, prov):
        self.defaultProvvigioni[plat] = prov

    def displayImporti(self):
        try:
            rows = int(self.label_numeroLetti.text())
            self.tableWidget__importi.setRowCount(rows)
            stagione = self.combo_stagione.currentText()
            platform = self.combo_platform.currentText()
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
        except:
            print(fex())

    def setNuovoImporto(self):
        row = self.tableWidget__importi.rowCount()
        self.tableWidget__importi.setFocus(True)
        self.tableWidget__importi.scrollToBottom()
        item = self.tableWidget__importi.item(row - 1, 1)
        item.setSelected(True)
        self.tableWidget__importi.editItem(item)

    def loadConfig(self):
        if self.checkConfigFile():
            self.setNumeroLetti(str(self.config['numero letti']))
            self.displayImporti()


    def saveConfig(self):
        with open(self.fileConf, 'w') as fileconfig:
            json.dump(self.config, fileconfig, indent=4, sort_keys=True)

    def checkConfigFile(self):
        try:
            with open(self.fileConf, 'r') as fileconfig:
                self.config = json.load(fileconfig)
            print(self.config)
        except FileNotFoundError:
            self.config = deepcopy(self.defaultConfig)
            self.saveConfig()
            print('File di configurazione creato')
        return True


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = DialogOption()
    ui.show()
    sys.exit(app.exec_())
