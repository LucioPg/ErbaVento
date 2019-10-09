"""modulo per l'automazione di flake8"""

import flake8
import subprocess
from sys import argv


class MyFlake8(object):
    """ritorna la configurazione di flake8"""

    MAXLINE = '90'
    IGN_ERR = ['F841']
    PREFIX = {
        'maxline': '--max-line-length=',
        'ign_err': '--ignore='
    }

    def __init__(self, script, maxline=None, ign_err=[]):
        if ign_err is None:
            ign_err = []
        self.script = script
        if maxline is None:
            self.maxline = MyFlake8.MAXLINE[:]
        else:
            self.maxline = maxline
        # ign_err è una lista
        if len(ign_err) == 0:
            self.ign_err = MyFlake8.IGN_ERR.copy()
        else:
            self.ign_err = ign_err

    def set_maxline(self, n=90):
        self.maxline = 90
        return self.maxline

    def update_ign_err(self, err):
        if err not in self.ign_err:
            self.ign_err.append(err)
        return self.ign_err


if __name__ == '__main__':
    src = argv[1]
    conf = MyFlake8(src)
    strng = 'flake8 ' + conf.PREFIX['maxline'] + conf.maxline + ' ' + conf.PREFIX['ign_err']
    for e in conf.ign_err:
        strng += e
        if conf.ign_err.index(e) < (len(conf.ign_err) - 1):
            strng += ','
    strng += (' ' + src)
    subprocess.call(strng)
    # print(strng)
