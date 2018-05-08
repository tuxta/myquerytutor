# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lessondialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LessonDialog(object):
    def setupUi(self, LessonDialog):
        LessonDialog.setObjectName("LessonDialog")
        LessonDialog.setEnabled(True)
        LessonDialog.resize(640, 480)
        self.gridLayout = QtWidgets.QGridLayout(LessonDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.webView = QtWebEngineWidgets.QWebEngineView(LessonDialog)
        self.webView.setProperty("url", QtCore.QUrl("about:blank"))
        self.webView.setObjectName("webView")
        self.gridLayout.addWidget(self.webView, 0, 0, 1, 1)

        self.retranslateUi(LessonDialog)
        QtCore.QMetaObject.connectSlotsByName(LessonDialog)

    def retranslateUi(self, LessonDialog):
        _translate = QtCore.QCoreApplication.translate
        LessonDialog.setWindowTitle(_translate("LessonDialog", "Dialog"))

from PyQt5 import QtWebEngineWidgets
