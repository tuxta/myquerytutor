from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt

installer_building = False

if installer_building:
    from myquerytutor.ui_lessondialog import Ui_LessonDialog
else:
    from ui_lessondialog import Ui_LessonDialog


class LessonDialog(QDialog):
    def __init__(self, parent, title, content):
        super(QDialog, self).__init__(parent)

        self.setModal(False)
        self.ui = Ui_LessonDialog()
        self.ui.setupUi(self)

        self.setWindowTitle(title)
        self.ui.webView.setHtml(content)

        # Disable the right click menu in the WebEngineView
        self.ui.webView.setContextMenuPolicy(Qt.NoContextMenu)
        self.ui.webView.setContextMenuPolicy(Qt.PreventContextMenu)
