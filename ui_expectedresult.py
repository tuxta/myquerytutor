# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'expectedresult.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ExpectedResult(object):
    def setupUi(self, ExpectedResult):
        ExpectedResult.setObjectName("ExpectedResult")
        ExpectedResult.resize(640, 480)
        self.gridLayout = QtWidgets.QGridLayout(ExpectedResult)
        self.gridLayout.setObjectName("gridLayout")
        self.resultTable = QtWidgets.QTableWidget(ExpectedResult)
        self.resultTable.setFrameShadow(QtWidgets.QFrame.Raised)
        self.resultTable.setLineWidth(0)
        self.resultTable.setMidLineWidth(0)
        self.resultTable.setObjectName("resultTable")
        self.resultTable.setColumnCount(0)
        self.resultTable.setRowCount(0)
        self.resultTable.verticalHeader().setVisible(False)
        self.gridLayout.addWidget(self.resultTable, 0, 0, 1, 1)

        self.retranslateUi(ExpectedResult)
        QtCore.QMetaObject.connectSlotsByName(ExpectedResult)

    def retranslateUi(self, ExpectedResult):
        _translate = QtCore.QCoreApplication.translate
        ExpectedResult.setWindowTitle(_translate("ExpectedResult", "Expected Result"))

