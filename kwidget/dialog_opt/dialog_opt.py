from PyQt5 import QtCore, QtGui, QtWidgets
from gui_option import Ui_Dialog_opt as DialogOptionGui
from kwidget.basiccolorselector.mybcolors import MyBcolors
from kwidget.basiccolorselector.mybcolors import MyBcolors_2
from kwidget.singleline.singleline import MySimpleLinEditDialog as SimpleLine
# from kwidget.mylineEdit.mylineEdit import MySimpleLineEdit as SimpleLine
import json
from copy import deepcopy
from traceback import format_exc as fex
import config_file
# from config_file import (fileConf,
#                          defaultTasse,
#                          defaultTasseAttive,
#                          defaultPlatforms,
#                          defaultImporti,
#                          defaultProvvigioni,
#                          defaultConfig)
import os



class DialogOption(DialogOptionGui, QtWidgets.QDialog):

    config = {}

    def __init__(self, parent=None):
        super(DialogOption, self).__init__(parent)
        self.setupUi(self)

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
        self.optIcon = QtGui.QIcon('./Icons/settingsIcon.png')
        self.setWindowIcon(self.optIcon)
        # funzioni pulsanti
        self.bot_aggiungiLetto.clicked.connect(self.aggiungiLetto)
        self.bot_sottraiLetto.clicked.connect(self.sottraiLetto)
        self.buttonBox.accepted.connect(self.saveConfigBot)
        self.bot_scegliColore.clicked.connect(self.chooseColor)

        # funzione radioButto tasse Attive
        self.radio_attivaTassa.clicked.connect(self.setTasseAttive)

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
        try:
            platAddPlat = ''
            dia = SimpleLine(icon=self.optIcon)
            if dia.exec_():
                platAddPlat = dia.newPlat
                print('nuova platform: ', platAddPlat)
            else:
                return
            if platAddPlat != '' and platAddPlat not in self.config['platforms'].keys():
                importi = [0 for x in range(self.config['numero letti'])]
                for sta in self.config['stagione']:
                    self.config['stagione'][sta]['importi'][platAddPlat] = importi
                self.config['provvigioni'][platAddPlat] = 0.0
                self.config['tasse attive'][platAddPlat] = self.radio_attivaTassa.isChecked()
                self.saveConfig(config_file.fileConf, self.config)
                self.chooseColor(platAddPlat)
                self.setComboPlat()
                self.combo_platform.setCurrentIndex(self.combo_platform.findText(platAddPlat))
            else:
                print('sono fuori')
        except:
            print(fex())

    def aggiungiLetto(self):
        numeroAttuale = int(self.label_numeroLetti.text())
        numero = str(numeroAttuale + 1)
        self.setNumeroLetti(numero)
        self.config['numero letti'] = numero
        self.displayImporti()

    @classmethod
    def checkConfigFile(cls):
        try:
            fileConf = os.path.join(os.getcwd(), config_file.fileConf)

            with open(fileConf, 'r') as fileconfig:
                config = json.load(fileconfig)
                cls.config = config
            # print(self.config)
        except FileNotFoundError:
            config = deepcopy(config_file.defaultConfig)
            cls.config = config
            cls.saveConfig(config_file.fileConf, cls.config)
            print('File di configurazione creato')
        return config

    def chooseColor(self, platCol=None):
        try:
            if platCol is None:
                platCol = self.combo_platform.currentText()

            coloriPresenti = [presente for presente in self.config['platforms'].values()]
            print('colori presenti: ', coloriPresenti)
            col = QtWidgets.QColorDialog.getColor()
            print('colore scelto: ', col.name())
            if col.isValid():
                if col.name() not in coloriPresenti:
                    self.bot_scegliColore.setStyleSheet("QPushButton { background-color: %s }"
                                                        % col.name())
                    self.config['platforms'][platCol] = col.name()
                    self.config['colori settati'][platCol] = col.name()
                else:
                    msg = QtWidgets.QMessageBox()
                    msg.setText('Il colore selezionato è già stato attribuito')
                    msg.setIcon(QtWidgets.QMessageBox.Warning)
                    msg.setWindowTitle("Attenzione!")
                    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    msg.exec_()
                    return self.chooseColor(platCol)
            # if colorForm.accepted():
            # print(colorForm.platColors)
            # self.config['platforms'] = colorForm.platColors
            # colorForm.currentColorChanged.connect(self.stampa)
            # self.setColor()
            # colorForm.close()
            # else:
            #     print('not accepted', colorForm.accepted())

        except:
            print(fex())

    def clearComboPlat(self):
        self.combo_platform.clear()

    def displayImporti(self, t=None):
        if t is not None:
            print('testo passato: ', t)
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
            self.setColor()
            self.displayTasseAttive()
        except KeyError:
            print('KeyErr in displayImporti')
        except:
            print(fex())

    def displayTasseAttive(self):
        plat = self.combo_platform.currentText()
        act = self.config['tasse attive'][plat]
        self.radio_attivaTassa.setChecked(act)

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
            self.setComboPlat()
            self.displayTasseAttive()
            self.setColor()


    def on_context_menu(self, point):
        # show context menu
        self.popMenu.exec_(self.combo_platform.mapToGlobal(point))

    def removePlatform(self):

        plat = self.combo_platform.currentText()
        del self.config['platforms'][plat]
        del self.config['provvigioni'][plat]
        del self.config['tasse attive'][plat]
        # self.config['platforms'].__delitem__(plat)
        # self.config['provvigioni'].__delitem__(plat)
        # self.config['tasse attive'].__delitem__(plat)
        for sta in self.config['stagione']:
            del self.config['stagione'][sta]['importi'][plat]
            # self.config['stagione'][sta]['importi'].__delitem__(plat)
        self.setComboPlat()
        self.saveConfig(self.fileConf, self.config)

    @staticmethod
    def saveConfig(fileConf, config):
        with open(fileConf, 'w') as fileconfig:
            json.dump(config, fileconfig, indent=4, sort_keys=True)

    def saveConfigBot(self):
        # fileConf = os.path.join(os.getcwd(), self.fileConf)
        self.saveConfig(config_file.fileConf, self.config)

    def setColor(self):
        plat = self.combo_platform.currentText()
        color = self.config['platforms'][plat]
        self.bot_scegliColore.setStyleSheet("QPushButton { background-color: %s }"
                                            % QtGui.QColor(color).name())

    def setComboPlat(self):
        self.combo_platform.clear()
        plats = self.config['platforms'].keys()
        for plat in plats:
            ind = self.combo_platform.findText(plat)
            if ind == -1:
                self.combo_platform.addItem(plat)

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

    def setTasseAttive(self):
        plat = self.combo_platform.currentText()
        self.config['tasse attive'][plat] = self.radio_attivaTassa.isChecked()



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
