from PyQt5 import QtCore, QtGui, QtWidgets
from gui_option import Ui_Dialog as DialogOptionGui
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
        self.defaultImporti = {'Booking.com': [72, 74, 92, 111, 130],
                               'AirB&B': [64, 65, 85, 100, 117],
                               'Privati': [72, 74, 92, 111, 130]}
        self.defaultProvvigioni = [0.15, 0.03, 0]
        self.config = {}
        self.defaultConfig = {'numero letti': 5,
                              'platforms': self.defaultPlatforms,
                              'stagione': {'alta': {'provvigioni': {pl: prov for pl, prov in zip(self.defaultPlatforms,
                                                                                                 self.defaultProvvigioni)},
                                                    'importi': self.defaultImporti
                                                    },
                                           'bassa': {'provvigioni': {pl: prov for pl, prov in zip(self.defaultPlatforms,
                                                                                                  self.defaultProvvigioni)},
                                                     'importi': self.defaultImporti
                                                     },
                                           'media': {'provvigioni': {pl: prov for pl, prov in zip(self.defaultPlatforms,
                                                                                                  self.defaultProvvigioni)},
                                                     'importi': self.defaultImporti
                                                     }
                                           },
                              }

        self.checkConfigFile()

    def loadConfig(self):
        pass

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
            return print('File di configurazione creato')


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = DialogOption()
    ui.show()
    sys.exit(app.exec_())
