import os
import shutil
from PyQt5.QtCore import Qt, QStandardPaths
from PyQt5.Qt import QWizardPage, QLabel, QGridLayout, QLineEdit, QPalette, QPixmap
from PyQt5.QtWidgets import QWizard


class FirstRunWiz(QWizard):
    def __init__(self, app_settings):
        QWizard.__init__(self)
        self.app_settings = app_settings
        layout = [QWizard.Stretch, QWizard.BackButton, QWizard.NextButton, QWizard.FinishButton, QWizard.CancelButton]
        self.setButtonLayout(layout)
        self.setOptions(self.NoBackButtonOnStartPage)

        self.setWizardStyle(QWizard.ModernStyle)
        self.setWindowTitle("MQT First Run Wizard")
        self.setPixmap(QWizard.WatermarkPixmap, QPixmap('watermark.png'))

        self.first_name = ''
        self.surname = ''
        self.first_name_edit = None
        self.surname_edit = None

        self.teacher_name = ''
        self.teacher_email = ''
        self.teacher_name_edit = None
        self.teacher_email_edit = None

        self.setPage(1, self.intro())
        self.setPage(2, self.user_info())
        self.setPage(3, self.teacher_info())
        self.setPage(4, self.complete())

        self.setStartId(1)

    def intro(self):
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

    def teacher_info(self):
        page = QWizardPage()
        page.setTitle("Your details")
        page.setSubTitle("Complete the form and click next")
        layout = QGridLayout(page)
        teacher_name_label = QLabel("Teacher Name    ")
        self.teacher_name_edit = QLineEdit()
        teacher_email_label = QLabel("Teacher Email   ")
        self.teacher_email_edit = QLineEdit()

        layout.addWidget(teacher_name_label, 0, 0)
        layout.addWidget(self.teacher_name_edit, 0, 1)
        layout.addWidget(teacher_email_label, 1, 0)
        layout.addWidget(self.teacher_email_edit, 1, 1)

        return page

    def user_info(self):
        page = QWizardPage()
        page.setTitle("Your details")
        page.setSubTitle("Complete the form and click next")
        layout = QGridLayout(page)
        first_name_label = QLabel("First Name  ")
        self.first_name_edit = QLineEdit()
        surname_label = QLabel("Surname     ")
        self.surname_edit = QLineEdit()

        layout.addWidget(first_name_label, 1, 0)
        layout.addWidget(self.first_name_edit, 1, 1)
        layout.addWidget(surname_label, 2, 0)
        layout.addWidget(self.surname_edit, 2, 1)

        return page

    def complete(self):
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
            self.check_name_entry()
            if len(self.first_name) == 0 or \
                    len(self.surname) == 0:
                return 2
            self.app_settings.set_user_name(self.first_name, self.surname)
            return 3
        elif current_id == 3:
            self.check_teacher_entry()
            if len(self.teacher_name) == 0 or \
                    len(self.teacher_email) == 0:
                return 2
            self.app_settings.set_teacher_info(self.teacher_name, self.teacher_email)
            self.make_local_database()
            return 4
        else:
            return -1

    def check_name_entry(self):
        self.first_name = self.first_name_edit.text()
        self.surname = self.surname_edit.text()
        if len(self.first_name) == 0:
            palette = self.first_name_edit.palette()
            palette.setColor(QPalette.Base, Qt.yellow)
            self.first_name_edit.setPalette(palette)
        else:
            palette = self.first_name_edit.palette()
            palette.setColor(QPalette.Base, Qt.white)
            self.first_name_edit.setPalette(palette)
        if len(self.surname) == 0:
            palette = self.surname_edit.palette()
            palette.setColor(QPalette.Base, Qt.yellow)
            self.surname_edit.setPalette(palette)
        else:
            palette = self.surname_edit.palette()
            palette.setColor(QPalette.Base, Qt.white)
            self.surname_edit.setPalette(palette)

    def check_teacher_entry(self):
        self.teacher_name = self.teacher_name_edit.text()
        self.teacher_email = self.teacher_email_edit.text()
        if len(self.teacher_name) == 0:
            palette = self.teacher_name_edit.palette()
            palette.setColor(QPalette.Base, Qt.yellow)
            self.teacher_name_edit.setPalette(palette)
        else:
            palette = self.teacher_name_edit.palette()
            palette.setColor(QPalette.Base, Qt.white)
            self.teacher_name_edit.setPalette(palette)
        if len(self.teacher_email) == 0:
            palette = self.teacher_email_edit.palette()
            palette.setColor(QPalette.Base, Qt.yellow)
            self.teacher_email_edit.setPalette(palette)
        else:
            palette = self.teacher_email_edit.palette()
            palette.setColor(QPalette.Base, Qt.white)
            self.teacher_email_edit.setPalette(palette)

    def make_local_database(self):
        dir_path = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
        file_name = os.path.join(dir_path, 'MQT_APP.sqlite')
        shutil.copy('MQT_APP.sqlite', file_name)
