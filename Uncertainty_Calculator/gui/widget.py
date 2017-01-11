# -*- coding:utf-8 -*-
'''
@author: frokaikan
'''

from ..formula.formula_base import Mean,StandardDeviation,ua,ub,uc
from ..formula.formula_indirect import Indirect_Uncertainty,_1,_2,_3,_4,_5,_6,_7,_8,_9,_0
from ..formula.formula_fit import fit
from PyQt5 import QtWidgets,QtGui,QtCore
from collections import OrderedDict

class Status_Sig(QtCore.QObject):
    sig = QtCore.pyqtSignal()
    
class MainInput(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self._init()
        self._data = []
        self._data_I = []
        self._ans = None
        
    def _showMsg(self,msg):
        self._status.showMessage(msg)
        
    def _init(self):
        btn_Imode = QtWidgets.QPushButton('Direct Measurement',self)
        btn_Imode.setCheckable(True)
        btn_Imode.clicked.connect(self._changeType)
        self._btnImode = btn_Imode
        
        btn_IShow = QtWidgets.QPushButton('Show IData',self)
        btn_IShow.setEnabled(False)
        btn_IShow.clicked.connect(self._Show_IData)
        self._btnIShow = btn_IShow
        
        btn_IAdd = QtWidgets.QPushButton('Add to IData',self)
        btn_IAdd.setEnabled(False)
        btn_IAdd.setShortcut('Ctrl+Enter')
        btn_IAdd.clicked.connect(self._AddToIData)
        self._btnIAdd = btn_IAdd
        
        btn_IDropLast = QtWidgets.QPushButton('Drop Last IData',self)
        btn_IDropLast.setEnabled(False)
        btn_IDropLast.clicked.connect(self._IDropLast)
        self._btnIDropLast = btn_IDropLast
        
        btn_ICompute = QtWidgets.QPushButton('Indirect Compute',self)
        btn_ICompute.setEnabled(False)
        btn_ICompute.setShortcut('Ctrl+Shift+Enter')
        btn_ICompute.clicked.connect(self._ICompute)
        self._btnICompute = btn_ICompute
        
        HBox1 = QtWidgets.QHBoxLayout()
        HBox1.addWidget(btn_Imode)
        HBox1.addWidget(btn_IShow)
        HBox1.addStretch(1)
        HBox1.addWidget(btn_IAdd)
        HBox1.addWidget(btn_IDropLast)
        HBox1.addStretch(1)
        HBox1.addWidget(btn_ICompute)
        
        edt = QtWidgets.QLineEdit(self)
        edt.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(r'[0-9]+(?:\.[0-9]*)?')))
        self._edt = edt
        
        btn_enter = QtWidgets.QPushButton('Submit',self)
        btn_enter.clicked.connect(self._Submit)
        btn_enter.setShortcut('Enter')
        
        btn_check = QtWidgets.QPushButton('Show Data',self)
        btn_check.clicked.connect(self._Show_Data)
        
        btn_dropLast = QtWidgets.QPushButton('Drop Last',self)
        btn_dropLast.clicked.connect(self._Drop_Last)
        
        btn_clearAll = QtWidgets.QPushButton('Clear All',self)
        btn_clearAll.clicked.connect(self._Clear_All)
        btn_clearAll.setShortcut('Shift+Backspace')
        
        btn_modify = QtWidgets.QPushButton('Modify Data',self)
        btn_modify.clicked.connect(self._Modify)
        
        btn_fit = QtWidgets.QPushButton('Fit Data',self)
        btn_fit.setEnabled(False)
        btn_fit.clicked.connect(self._Fit)
        self._btnFit = btn_fit
        
        btn_HBox2 = QtWidgets.QHBoxLayout()
        btn_HBox2.addWidget(btn_check)
        btn_HBox2.addStretch(1)
        btn_HBox2.addWidget(btn_dropLast)
        btn_HBox2.addWidget(btn_clearAll)
        btn_HBox2.addWidget(btn_modify)
        btn_HBox2.addStretch(1)
        btn_HBox2.addWidget(btn_fit)
        
        btn_eval = QtWidgets.QPushButton('Compute',self)
        btn_eval.clicked.connect(self._Compute)
        btn_eval.setShortcut('Shift+Enter')
        
        VBox=QtWidgets.QVBoxLayout()
        VBox.addLayout(HBox1)
        VBox.addStretch(5)
        VBox.addWidget(edt)
        VBox.addStretch(3)
        VBox.addWidget(btn_enter)
        VBox.addStretch(1)
        VBox.addLayout(btn_HBox2)
        VBox.addStretch(1)
        VBox.addWidget(btn_eval)
        self.setLayout(VBox)
        
    def _Submit(self):
        txt = self._edt.text()
        if txt:
            self._data.append(float(txt))
            self._edt.setText('')
            self._showMsg('Add: %0.6f'%float(txt))
            
    def _Show_Data(self):
        text = ''
        count = 0
        for data in self._data:
            count += 1
            text += format(str(count),'>2') + '\t\t' + str(data) + '\n'
        QtWidgets.QMessageBox.information(self,'Data',text,QtWidgets.QMessageBox.Ok)
        
    def _Drop_Last(self):
        if self._data:
            self._data.pop()
            if self._data:
                self._showMsg('Now Last: %0.6f'%self._data[-1])
            else:
                self._showMsg('Data is empty...')
            
    def _Clear_All(self):
        self._data = []
        self._showMsg('Data is empty...')
        
    def _Modify(self):
        text,ok = QtWidgets.QInputDialog.getText(self,'Modify Data','Please Input As:\n1:23.1')
        if ok:
            try:
                No,Num = text.split(':')
                No = int(No)
                if No <= 0:
                    raise IndexError
                Num = float(Num)
                self._data[No-1] = Num
                QtWidgets.QMessageBox.information(self,'Modify Success','Modify %d to %s'%(No,Num),QtWidgets.QMessageBox.Ok)
                self._showMsg('Now No_%d: %0.6f'%(No,Num))
            except IndexError:
                QtWidgets.QMessageBox.critical(self,'Modify Failed','Index ut of range!\nIndex should between 1 and %d'%len(self._data),QtWidgets.QMessageBox.Ok)
            except:
                QtWidgets.QMessageBox.critical(self,'Modify Failed','Please input As:\nIndex:Number!',QtWidgets.QMessageBox.Ok)
    
    def _Fit(self):
        datax,datay = self._data_I[0]['Data'],self._data_I[1]['Data']
        tmp = fit(datax,datay)()
        k,b = tmp
        txt = 'y = %0.6g * x + %0.6g'%(k,b)
        QtWidgets.QMessageBox.information(self,'Fit Answer',txt,QtWidgets.QMessageBox.Ok)
        self._showMsg(txt)
    
    def _Compute(self):
        if not self._data:
            QtWidgets.QMessageBox.critical(self,'Data is empty','Please input your data!',QtWidgets.QMessageBox.Ok)
            return
            
        delta_dialog = QtWidgets.QInputDialog()
        while True:
            text,ok = delta_dialog.getText(self,'Delta','Please input Delta:')
            if ok:
                try:
                    delta = float(text)
                except:
                    QtWidgets.QMessageBox.critical(self,'Invalid Delta','Please input a float number!',QtWidgets.QMessageBox.Ok)
                else:
                    break
            else:
                return

        answer = OrderedDict(zip(('Delta','Count','Mean','StdDev','ua','ub','uc'),(
            delta,
            len(self._data),
            Mean(*self._data),
            StandardDeviation(*self._data),
            ua(delta,*self._data),
            ub(delta),
            uc(delta,*self._data)
        )))
        self._ans = answer
        
        answer_str = ''
        for item,value in answer.items():
            answer_str += format(item,'>6') + ':\t\t' + format(value,'0.6g') + '\n'
        QtWidgets.QMessageBox.information(self,'Data Analysis',answer_str,QtWidgets.QMessageBox.Ok)

    def _changeType(self,pressed):
        if pressed:
            self._btnImode.setText('Indirect Measurement')
            self._flag = 1
            self._btnIShow.setEnabled(True)
            self._btnIAdd.setEnabled(True)
            self._btnIDropLast.setEnabled(True)
            self._btnICompute.setEnabled(True)
            self._showMsg('Now Indirect_Measurement...')
        else:
            self._btnImode.setText('Direct Measurement')
            self._flag = 0
            self._btnIShow.setEnabled(False)
            self._btnIAdd.setEnabled(False)
            self._btnIDropLast.setEnabled(False)
            self._btnICompute.setEnabled(False)
            self._btnFit.setEnabled(False)
            self._data_I = []
            self._showMsg('Now Direct_Measuerment...')

    def _Show_IData(self):
        tmp = ''
        k = 0
        for dat in self._data_I:
            k += 1
            tmp += format(str(k),'>2') + '\tMean:\t' + format(dat['Mean'],'0.6f') + '\tuc:\t' + format(dat['uc'],'0.6f') + '\n'
        QtWidgets.QMessageBox.information(self,'Indirect Data',tmp,QtWidgets.QMessageBox.Ok)
            
    def _AddToIData(self):
        if not self._ans:
            QtWidgets.QMessageBox.critical(self,'None Data','Please compute your data.',QtWidgets.QMessageBox.Ok)
        tmp_data = {}
        tmp_data['Data'] = self._data
        tmp_data['Mean'] = self._ans['Mean']
        tmp_data['uc'] = self._ans['uc']
        self._data_I.append(tmp_data)
        
        if len(self._data_I) == 2:
            self._btnFit.setEnabled(True)
        else:
            self._btnFit.setEnabled(False)
        
    def _IDropLast(self):
        if self._data_I:
            self._data_I.pop()
            
        if len(self._data_I) == 2:
            self._btnFit.setEnabled(True)
        else:
            self._btnFit.setEnabled(False)
            
    def _ICompute(self):
        if not self._data_I:
            QtWidgets.QMessageBox.critical(self,'IData is empty','Please add at least 1 datium!',QtWidgets.QMessageBox.Ok)
            return
        
        formula_dialog = QtWidgets.QInputDialog()
        while True:
            text,ok = formula_dialog.getText(self,'Formula','Please Enter Fourmula.\nUse _1,_2,... to represent param1,2...')
            if ok:
                try:
                    formula = eval(text)
                except:
                    QtWidgets.QMessageBox.critical(self,'Bad Input','Please check your formula.')
                else:
                    break
            else:
                return
                
        answer_f = Indirect_Uncertainty(formula,self._data_I)
        try:
            ans = str(answer_f)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self,'A Bug',e,QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.information(self,'IData Analysis',ans)