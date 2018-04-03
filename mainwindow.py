from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import (QMainWindow, QTreeWidgetItem, QTableWidgetItem)
from ui_mainwindow import Ui_MainWindow
from database_controller import DatabaseController
from lessondialog import LessonDialog
from expectedresult import ExpectedResult


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.db_ctrl = DatabaseController()

        self.build_selection_tree()
        self.topic = ''
        self.question = ''
        self.question_id = 0
        
        # Connect signals to slots #
        self.ui.questionSelectTree.clicked.connect(self.on_question_select_tree_clicked)
        self.ui.runQuery_button.clicked.connect(self.run_query_clicked)
        self.ui.expectedResult_button.clicked.connect(self.expected_result_clicked)
        self.ui.help_button.clicked.connect(self.help_clicked)
    
    def run_query_clicked(self):
        query = self.ui.queryTextArea.toPlainText()
        if query != '':
            column_names, row_data = self.db_ctrl.run_query(query)

            self.ui.resultsTable.setColumnCount(len(column_names))
            self.ui.resultsTable.setRowCount(len(row_data))
            self.ui.resultsTable.clear()
            self.ui.resultsTable.setHorizontalHeaderLabels(column_names)

            for row_num, row in enumerate(row_data):
                for col_num, item in enumerate(row):
                    cell = QTableWidgetItem()
                    cell.setText(str(item))
                    self.ui.resultsTable.setItem(row_num, col_num, cell)

    def expected_result_clicked(self):
        if self.question != '':
            query = self.db_ctrl.get_question_query(self.question_id)
            if query != '':
                column_names, row_data = self.db_ctrl.run_query(query)

                answer_dialog = ExpectedResult(self, self.question, column_names, row_data)

                answer_dialog.setModal(False)
                answer_dialog.show()
    
    def help_clicked(self):
        if not self.topic == '':
            lesson = self.db_ctrl.get_lesson(self.topic)
            lesson_dialog = LessonDialog(self, self.topic, lesson)
            lesson_dialog.setModal(False)
            lesson_dialog.show()

    def build_selection_tree(self):
        self.ui.questionSelectTree.setColumnCount(1)
        self.ui.questionSelectTree.header().close()

        questions_list = self.db_ctrl.get_questions_list()

        for topic in questions_list:
            topic_item = QTreeWidgetItem(self.ui.questionSelectTree)
            topic_item.setText(0, topic)
            for question in questions_list[topic]:
                QTreeWidgetItem(topic_item).setText(0, question)

    def on_question_select_tree_clicked(self, index: QModelIndex):
        topic_item = index.parent()
        self.topic = topic_item.data()
        self.question = index.data()

        self.question_id, description = self.db_ctrl.get_question(self.topic, self.question)
        self.ui.questionTextArea.setText(description)

        # For now, clearing the query
        # In future, reload previous query if exists
        self.ui.resultsTable.clear()
