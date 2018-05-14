from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtWidgets import (QMainWindow, QTreeWidgetItem)

installer_building = False

if installer_building:
    from myquerytutor.lessondialog import LessonDialog
    from myquerytutor.ui_mainwindow import Ui_MainWindow
    from myquerytutor.progressdialog import ProgressDialog
    from myquerytutor.expectedresult import ExpectedResult
    from myquerytutor.database_controller import DatabaseController
else:
    from lessondialog import LessonDialog
    from ui_mainwindow import Ui_MainWindow
    from progressdialog import ProgressDialog
    from expectedresult import ExpectedResult
    from database_controller import DatabaseController


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.queryTextArea.setFontPointSize(15)

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
        self.ui.progress_button.clicked.connect(self.show_progress)

        # Disable the right click menu in the WebEngineView
        self.ui.questionTextArea.setContextMenuPolicy(Qt.NoContextMenu)
        self.ui.questionTextArea.setContextMenuPolicy(Qt.PreventContextMenu)

        # Part of the horrible hack!!
        self.ui.queryTextArea.textChanged.connect(self.reset_font_query_edit)

    def reset_font_query_edit(self):
        """
        Horrible, Horrible, Horrible Hack!
        Necessary to get around the font resetting if the current text is deleted
        Every time something changes, the font size is set
        """
        self.ui.queryTextArea.setFontPointSize(15)
        self.ui.queryTextArea.setFontWeight(-1)

    def run_query_clicked(self):
        query = self.ui.queryTextArea.toPlainText()
        if query != '':

            column_names, row_data = self.db_ctrl.run_query(query)

            expected_result_query = self.db_ctrl.get_question_query(self.question_id)
            expected_names, expected_data = self.db_ctrl.run_query(expected_result_query)

            if column_names == expected_names and row_data == expected_data:
                result_color = 1
                self.db_ctrl.set_question_query(query, self.topic, self.question, 1)
            else:
                result_color = 2
                self.db_ctrl.set_question_query(query, self.topic, self.question, 0)

            # Compare the exemplar query with the user query to identify errors
            query_comparison_html = self.compare_queries(expected_result_query, query)
            print(query_comparison_html)

            result_dialog = ExpectedResult(self, self.question, column_names, row_data, result_color)
            result_dialog.setModal(False)
            result_dialog.show()

    def expected_result_clicked(self):
        if self.question != '':
            query = self.db_ctrl.get_question_query(self.question_id)
            if query != '':
                column_names, row_data = self.db_ctrl.run_query(query)

                answer_dialog = ExpectedResult(self, 'Expected Result for ' + self.question, column_names, row_data)

                answer_dialog.setModal(False)
                answer_dialog.ui.label_correct.setText('')
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

        questions_map, questions_list = self.db_ctrl.get_questions_list()

        for topic in questions_list:
            topic_item = QTreeWidgetItem(self.ui.questionSelectTree)
            topic_item.setText(0, topic)
            for question in questions_map[topic]:
                QTreeWidgetItem(topic_item).setText(0, question)

    def on_question_select_tree_clicked(self, index: QModelIndex):

        topic_item = index.parent()
        if not topic_item.isValid():
            return

        self.topic = topic_item.data()
        self.question = index.data()

        self.question_id, description = self.db_ctrl.get_question(self.topic, self.question)
        self.ui.questionTextArea.setHtml(description)

        # Load last query attempted for this question if on exists
        last_query = self.db_ctrl.get_last_query(self.topic, self.question)
        self.ui.queryTextArea.setText(last_query)

    def show_progress(self):
        questions_map, questions_list = self.db_ctrl.get_questions_list()

        progress_dialog = ProgressDialog(self, questions_map, questions_list, self.db_ctrl)

        progress_dialog.setModal(False)
        progress_dialog.ui.label_correct.setText('')
        progress_dialog.show()

    def compare_queries(self, exemplar_query, user_query):

        html_string_list = []

        # Set style rules
        html_header = '''
                    <style>
                      .Correct {
                        color:green;
                      }
                      .Incorrect {
                        color:red;
                      }
                    </style>
                    
                    <html>
                    '''
        # Break both queries into lists
        # Step through the user_query checking if each word
        # is in the exemplar. Set color and add to html string

        query_list = exemplar_query.split()
        exemplar_list = user_query.split()
        html_string_list.append(html_header)

        for word in query_list:
            if word in exemplar_list:
                html_string_list.append('<span class=Correct>' + word + '</span>')
            else:
                html_string_list.append('<span class=Incorrect>' + word + '</span>')

        html_string_list.append('''
                                
                                </html>
                                ''')

        html_string = ' '.join(html_string_list)

        return html_string
