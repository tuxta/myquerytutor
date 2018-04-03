from PyQt5.QtWidgets import QDialog
from ui_lessondialog import Ui_LessonDialog


class LessonDialog(QDialog):
    def __init__(self, parent, title, content):
        super(QDialog, self).__init__(parent)

        self.setModal(False)
        self.ui = Ui_LessonDialog()
        self.ui.setupUi(self)

        self.setWindowTitle(title)
        self.ui.webView.setHtml(content)

