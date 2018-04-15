#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import QApplication
from mainwindow import MainWindow

app = QApplication(sys.argv)
main_win = MainWindow()
main_win.show()
sys.exit(app.exec_())
