from PyQt5 import QtCore, QtGui
from copy import deepcopy
fileConf = 'config.json'
defaultTasse = 2
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
                 'tasse attive': defaultTasseAttive,
                 'colori settati': deepcopy(defaultPlatforms)
                 }