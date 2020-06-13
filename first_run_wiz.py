import os
import re
import shutil
import sys
from PyQt5.QtCore import QStandardPaths
from PyQt5.Qt import QWizardPage, QLabel, QGridLayout, QLineEdit, QPixmap, QCheckBox
from PyQt5.QtWidgets import QWizard


class FirstRunWiz(QWizard):
    def __init__(self, app_settings):
        QWizard.__init__(self)
        self.app_settings = app_settings
        layout = [QWizard.Stretch, QWizard.BackButton, QWizard.NextButton, QWizard.FinishButton, QWizard.CancelButton]
        self.setButtonLayout(layout)
        self.setOptions(self.NoBackButtonOnStartPage)

        if getattr(sys, 'frozen', False):
            self.dir_path = os.path.dirname(sys.executable)
        else:
            self.dir_path = os.path.dirname(os.path.realpath(__file__))

        self.setWizardStyle(QWizard.ModernStyle)
        self.setWindowTitle("MQT First Run Wizard")
        self.setPixmap(QWizard.WatermarkPixmap, QPixmap(os.path.join(self.dir_path, "watermark.png")))

        self.first_name = ''
        self.surname = ''
        self.email = ''
        self.first_name_edit = None
        self.surname_edit = None
        self.email_edit = None

        self.server_address = ''
        self.class_key = ''
        self.ssl_checkbox = None
        self.server_address_edit = None
        self.class_key_edit = None

        self.setPage(1, self.intro())
        self.setPage(2, self.user_info())
        self.setPage(3, self.server_details())
        self.setPage(4, self.complete())

        self.setStartId(1)

    @staticmethod
    def intro():
        page = QWizardPage()
        page.setTitle("Welcome to My Query Tutor")
        page.setSubTitle("The best tool to learn SQL")
        welcome_label = QLabel('''
I can see that this is the first time
you have run My Query Tutor.

We will now set everything up and you
won't have to see this again :-D
'''
                               )
        description_label = QLabel('')

        layout = QGridLayout(page)
        layout.addWidget(welcome_label)
        layout.addWidget(description_label)

        return page

    def server_details(self):
        page = QWizardPage()
        page.setTitle("Server Details")
        page.setSubTitle("Optional server details (for syncing progress)")
        layout = QGridLayout(page)
        server_address_label = QLabel("Server Address    ")
        self.server_address_edit = QLineEdit()
        class_key_label = QLabel("Class Key         ")
        self.class_key_edit = QLineEdit()
        ssl_label = QLabel("SSL               ")
        self.ssl_checkbox = QCheckBox()

        layout.addWidget(server_address_label, 1, 0)
        layout.addWidget(self.server_address_edit, 1, 1)
        layout.addWidget(class_key_label, 2, 0)
        layout.addWidget(self.class_key_edit, 2, 1)
        layout.addWidget(ssl_label, 3, 0)
        layout.addWidget(self.ssl_checkbox, 3, 1)

        return page

    def user_info(self):
        page = QWizardPage()
        page.setTitle("Your details")
        page.setSubTitle("Complete the form and click next")
        layout = QGridLayout(page)
        first_name_label = QLabel("First Name      ")
        self.first_name_edit = QLineEdit()
        self.first_name_edit.setStyleSheet("QLineEdit { background-color : white; color : black; }")
        surname_label = QLabel("Surname         ")
        self.surname_edit = QLineEdit()
        self.surname_edit.setStyleSheet("QLineEdit { background-color : white; color : black; }")
        email_label = QLabel("Email Address   ")
        self.email_edit = QLineEdit()
        self.email_edit.setStyleSheet("QLineEdit { background-color : white; color : black; }")

        layout.addWidget(first_name_label, 1, 0)
        layout.addWidget(self.first_name_edit, 1, 1)
        layout.addWidget(surname_label, 2, 0)
        layout.addWidget(self.surname_edit, 2, 1)
        layout.addWidget(email_label, 3, 0)
        layout.addWidget(self.email_edit, 3, 1)

        return page

    @staticmethod
    def complete():
        page = QWizardPage()
        page.setTitle("Settings Complete")
        page.setSubTitle("All Done! (That was easy, wasn't it?)")

        label = QLabel("Click finish and start MQT")
        label.setWordWrap(True)

        layout = QGridLayout(page)
        layout.addWidget(label)

        return page

    def nextId(self):
        current_id = self.currentId()
        if current_id == 1:
            return 2
        elif current_id == 2:
            return 3
        elif current_id == 3:
            return 4
        else:
            return -1

    def validateCurrentPage(self) -> bool:
        current_id = self.currentId()
        all_goods = True
        if current_id == 2:
            if self.check_name_entry():
                self.app_settings.set_user_details(self.first_name, self.surname, self.email)
                self.make_local_database()
            else:
                all_goods = False
        if current_id == 3:
            if self.ssl_checkbox.isChecked():
                ssl = 'true'
            else:
                ssl = 'false'
            self.app_settings.set_server_details(
                self.server_address_edit.text(),
                self.class_key_edit.text(),
                "",
                ssl
            )

        return all_goods

    def check_name_entry(self):
        correct_style = "QLineEdit { background-color : white; color : black; }"
        incorrect_style = "QLineEdit { background-color : yellow; color : black; }"
        all_cool = True

        self.first_name = self.first_name_edit.text()
        self.surname = self.surname_edit.text()
        self.email = self.email_edit.text()

        if len(self.first_name) == 0:
            self.first_name_edit.setStyleSheet(incorrect_style)
            all_cool = False
        else:
            self.first_name_edit.setStyleSheet(correct_style)

        if len(self.surname) == 0:
            self.surname_edit.setStyleSheet(incorrect_style)
            all_cool = False
        else:
            self.surname_edit.setStyleSheet(correct_style)

        if re.match('''(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)''', self.email):
            self.email_edit.setStyleSheet(correct_style)
        else:
            self.email_edit.setStyleSheet(incorrect_style)
            all_cool = False

        return all_cool

    def make_local_database(self):
        src_db_file = os.path.join(self.dir_path, 'MQT_APP.sqlite')
        dir_path = QStandardPaths.writableLocation(QStandardPaths.AppLocalDataLocation)
        file_name = os.path.join(dir_path, 'MQT_APP.sqlite')
        shutil.copy(src_db_file, file_name)

        src_db_file = os.path.join(self.dir_path, 'MQT_EX.sqlite')
        dir_path = QStandardPaths.writableLocation(QStandardPaths.AppLocalDataLocation)
        file_name = os.path.join(dir_path, 'MQT_EX.sqlite')
        shutil.copy(src_db_file, file_name)

        src_dir = os.path.join(self.dir_path, 'images')
        dst_dir = os.path.join(dir_path, 'images')
        shutil.copytree(src_dir, dst_dir)
