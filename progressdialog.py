from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QDialog, QTableWidgetItem

installer_building = True

if installer_building:
    from myquerytutor.ui_expectedresult import Ui_ExpectedResult
else:
    from ui_expectedresult import Ui_ExpectedResult


class ProgressDialog(QDialog):
    def __init__(self, parent, questions_map, questions_list, db_ctrl):
        super(QDialog, self).__init__(parent)

        self.setModal(False)
        self.ui = Ui_ExpectedResult()
        self.ui.setupUi(self)

        self.setWindowTitle('Progress')
        self.ui.resultTable.horizontalHeader().setVisible(False)

        num_columns = 0
        for topic in questions_list:
            length = len(questions_map[topic])
            if length > num_columns:
                num_columns = length

        self.ui.resultTable.setColumnCount(num_columns + 1)
        self.ui.resultTable.setRowCount(len(questions_list))
        self.ui.resultTable.clear()
        self.ui.resultTable.setShowGrid(False)

        for i in range(1, num_columns + 1):
            self.ui.resultTable.setColumnWidth(i, 30)

        row_num = 0
        for topic in questions_list:
            key_cell = QTableWidgetItem()
            key_cell.setText(topic)
            self.ui.resultTable.setItem(row_num, 0, key_cell)
            queries = questions_map[topic]
            for col_num, question in enumerate(queries):
                success = db_ctrl.is_successful(topic, question)

                cell = QTableWidgetItem()
                if success == 0:
                    cell.setBackground(QColor(255, 100, 0))
                elif success == 1:
                    cell.setBackground(QColor(0, 255, 0))
                else:
                    cell.setBackground(QColor(200, 200, 200))

                self.ui.resultTable.setItem(row_num, col_num + 1, cell)

            row_num += 1
