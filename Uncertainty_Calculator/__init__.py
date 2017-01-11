# -*- coding:utf-8
'''
@author: frokaikan
'''

from PyQt5 import QtGui,QtWidgets
import sys
from .gui.mainwindow import Calculator

def start():
    app = QtWidgets.QApplication(sys.argv)
    tmp = Calculator()
    sys.exit(app.exec_())

