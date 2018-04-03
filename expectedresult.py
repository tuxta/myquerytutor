from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from ui_expectedresult import Ui_ExpectedResult


class ExpectedResult(QDialog):
    def __init__(self, parent, title, column_names, row_data):
        super(QDialog, self).__init__(parent)

        self.setModal(False)
        self.ui = Ui_ExpectedResult()
        self.ui.setupUi(self)

        self.setWindowTitle(title)

        self.ui.resultTable.setColumnCount(len(column_names))
        self.ui.resultTable.setRowCount(len(row_data))
        self.ui.resultTable.clear()
        self.ui.resultTable.setHorizontalHeaderLabels(column_names)

        for row_num, row in enumerate(row_data):
            for col_num, item in enumerate(row):
                cell = QTableWidgetItem()
                cell.setText(str(item))
                self.ui.resultTable.setItem(row_num, col_num, cell)
