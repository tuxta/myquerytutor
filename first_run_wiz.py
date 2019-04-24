from PyQt5.QtCore import Qt
from PyQt5.Qt import QWizardPage, QLabel, QGridLayout, QLineEdit, QPalette
from PyQt5.QtWidgets import QWizard


class FirstRunWiz(QWizard):
    def __init__(self, app_settings):
        QWizard.__init__(self)
        self.app_settings = app_settings
        layout = [QWizard.Stretch, QWizard.BackButton, QWizard.NextButton, QWizard.FinishButton, QWizard.CancelButton]
        self.setButtonLayout(layout)
        self.setOptions(self.NoBackButtonOnStartPage)

        self.first_name = ''
        self.surname = ''
        self.first_name_edit = None
        self.surname_edit = None
        self.first_attempt_name = True

        self.setPage(1, self.intro())
        self.setPage(2, self.user_info())
        self.setPage(3, self.complete())

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

    def user_info(self):
        page = QWizardPage()
        page.setTitle("Your details")
        page.setSubTitle("Complete the form and click next")
        layout = QGridLayout(page)
        first_name_label = QLabel("First Name  ")
        self.first_name_edit = QLineEdit()
        surname_label = QLabel("Surname     ")
        self.surname_edit = QLineEdit()

        layout.addWidget(first_name_label, 0, 0)
        layout.addWidget(self.first_name_edit, 0, 1)
        layout.addWidget(surname_label, 1, 0)
        layout.addWidget(self.surname_edit, 1, 1)

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
