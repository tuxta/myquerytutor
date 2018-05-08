#!/usr/bin/python3
import sys
from PyQt5.QtWidgets import QApplication

installer_building = False

if installer_building:
    from myquerytutor.mainwindow import MainWindow
else:
    from mainwindow import MainWindow


def main():
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
