from PyQt5.Qt import QWizardPage, QLabel, QGridLayout, QPixmap
from PyQt5.QtWidgets import QWizard


class FirstRunWiz(QWizard):
    def __init__(self):
        QWizard.__init__(self)
        layout = [QWizard.Stretch, QWizard.BackButton, QWizard.NextButton, QWizard.FinishButton, QWizard.CancelButton]
        self.setButtonLayout(layout)
        self.setOptions(self.NoBackButtonOnStartPage)

        self.addPage(self.intro())
        self.addPage(self.complete())

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
        desciption_label = QLabel('')

        layout = QGridLayout(page)
        layout.addWidget(welcome_label)
        layout.addWidget(desciption_label)

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

    def accept(self):
        self.close()
