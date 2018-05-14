# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'expectedresult.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ExpectedResult(object):
    def setupUi(self, ExpectedResult):
        ExpectedResult.setObjectName("ExpectedResult")
        ExpectedResult.resize(640, 480)
        self.gridLayout = QtWidgets.QGridLayout(ExpectedResult)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.resultTable = QtWidgets.QTableWidget(ExpectedResult)
        self.resultTable.setFrameShadow(QtWidgets.QFrame.Raised)
        self.resultTable.setLineWidth(0)
        self.resultTable.setMidLineWidth(0)
        self.resultTable.setObjectName("resultTable")
        self.resultTable.setColumnCount(0)
        self.resultTable.setRowCount(0)
        self.resultTable.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.resultTable)
        self.label_correct = QtWidgets.QLabel(ExpectedResult)
        self.label_correct.setAlignment(QtCore.Qt.AlignCenter)
        self.label_correct.setObjectName("label_correct")
        self.verticalLayout.addWidget(self.label_correct)
        self.textBrowser = QtWidgets.QTextBrowser(ExpectedResult)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy)
        self.textBrowser.setMaximumSize(QtCore.QSize(16777215, 100))
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(ExpectedResult)
        QtCore.QMetaObject.connectSlotsByName(ExpectedResult)

    def retranslateUi(self, ExpectedResult):
        _translate = QtCore.QCoreApplication.translate
        ExpectedResult.setWindowTitle(_translate("ExpectedResult", "Expected Result"))
        self.label_correct.setText(_translate("ExpectedResult", "TextLabel"))

