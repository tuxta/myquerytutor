from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from ui_expectedresult import Ui_ExpectedResult


class ProgressDialog(QDialog):
    def __init__(self, parent, results_map):
        super(QDialog, self).__init__(parent)

        self.setModal(False)
        self.ui = Ui_ExpectedResult()
        self.ui.setupUi(self)

        self.setWindowTitle('Progress')
        self.ui.resultTable.horizontalHeader().setVisible(False)

        num_columns = 0
        for topic in results_map:
            length = len(results_map[topic])
            if length > num_columns:
                num_columns = length

        self.ui.resultTable.setColumnCount(num_columns + 1)
        self.ui.resultTable.setRowCount(len(results_map))
        self.ui.resultTable.clear()
        self.ui.resultTable.setShowGrid(False)

        for i in range(1, num_columns + 1):
            self.ui.resultTable.setColumnWidth(i, 30)

        row_num = 0
        for key, queries in results_map.items():

            key_cell = QTableWidgetItem()
            key_cell.setText(key)
            self.ui.resultTable.setItem(row_num, 0, key_cell)

            for col_num, item in enumerate(queries):
                cell = QTableWidgetItem()
                if item == 0:
                    cell.setBackground(QColor(255, 100, 0))
                elif item == 1:
                    cell.setBackground(QColor(0, 255, 0))
                else:
                    cell.setBackground(QColor(200, 200, 200))

                self.ui.resultTable.setItem(row_num, col_num + 1, cell)

            row_num += 1
