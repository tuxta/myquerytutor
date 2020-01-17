from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt

installer_building = False

if installer_building:
    from myquerytutor.ui_settingsdialog import Ui_SettingsDialog
else:
    from ui_settingsdialog import Ui_SettingsDialog


class SettingsDialog(QDialog):
    def __init__(self, parent, app_settings, server_address, class_key, ssl):
        super(QDialog, self).__init__(parent)

        self.app_settings = app_settings

        self.setModal(False)
        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Settings")

        self.ui.lineEdit.setText(server_address)
        self.ui.lineEdit_2.setText(class_key)
        self.ui.checkBox.setChecked(ssl)

        self.ui.buttonBox.accepted.connect(self.ok)

    def ok(self):
        self.app_settings.set_server_details(self.ui.lineEdit.text(), self.ui.lineEdit_2.text())
