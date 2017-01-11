# -*- coding:utf-8 -*-
'''
@author: frokaikan
'''

from PyQt5 import QtGui,QtCore,QtWidgets
from .widget import MainInput

class Calculator(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.status_bar = self.statusBar()
        self.status_bar.showMessage('Ready...')
        self._main = MainInput()
        self._main._status = self.status_bar
        self._init()
        
    def _TxtLoader(self):
        fname_orig = QtWidgets.QFileDialog.getOpenFileName(self,'C:',filter = 'text file (*.txt)')
        fname = fname_orig[0]
        if fname.endswith('.txt'):
            old_data = self._main._data
            with open(fname,'rt') as f:
                try:
                    self._main._data = [float(x) for x in f.read().split()]
                except:
                    QtWidgets.QMessageBox.critical(self,'Text Error','Invalid Format!')
                    self._main._data = old_data
                else:
                    self._main._Show_Data()
        else:
            QtWidgets.QMessageBox.warning(self,'File Not Match','Please select a text file.')
    
    def _init(self):
        self.setCentralWidget(self._main)
        
        LoadTxt = QtWidgets.QAction(QtGui.QIcon(),'LoadTxt',self)
        LoadTxt.triggered.connect(self._TxtLoader)
        
        menu = self.menuBar()
        loader = menu.addMenu('Loader')
        loader.addAction(LoadTxt)
        
        self.setWindowTitle('Uncertainty Calculator')
        self.setGeometry(300,300,600,200)
        self.show()
        
        