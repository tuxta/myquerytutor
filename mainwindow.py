import os
import re
import sys
import requests
from bs4 import BeautifulSoup

from PyQt5.Qt import QPixmap
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtWebEngineWidgets import QWebEngineSettings
from PyQt5.QtWidgets import QMainWindow, QTreeWidgetItem, QSplashScreen, QLabel, QDialog, QBoxLayout

installer_building = False

if installer_building:
    from myquerytutor.lessondialog import LessonDialog
    from myquerytutor.ui_mainwindow import Ui_MainWindow
    from myquerytutor.progressdialog import ProgressDialog
    from myquerytutor.expectedresult import ExpectedResult
    from myquerytutor.database_controller import DatabaseController
    from myquerytutor.appsettings import AppSettings
    from myquerytutor.first_run_wiz import FirstRunWiz
    from myquerytutor.settingsdialog import SettingsDialog
else:
    from lessondialog import LessonDialog
    from ui_mainwindow import Ui_MainWindow
    from progressdialog import ProgressDialog
    from expectedresult import ExpectedResult
    from database_controller import DatabaseController
    from appsettings import AppSettings
    from first_run_wiz import FirstRunWiz
    from settingsdialog import SettingsDialog


class MainWindow:
    def __init__(self):

        self.dir_path = os.path.dirname(os.path.realpath(__file__))

        self.splash_screen = QSplashScreen()
        self.splash_screen.setPixmap(QPixmap('splash.png'))
        self.splash_screen.show()

        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)
        self.ui.queryTextArea.setFontPointSize(15)
        self.app_settings = AppSettings()
        self.settings_cancelled = False
        self.erd = None

        first_run = False
        if not self.app_settings.has_settings():
            first_run = True
            wiz = FirstRunWiz(self.app_settings)
            wiz.setMinimumWidth(650)
            self.splash_screen.hide()
            wiz_result = wiz.exec()
            if wiz_result == 0:
                self.settings_cancelled = True
                sys.exit()

        self.db_ctrl = self.initial_checks()
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
        self.ui.syncButton.clicked.connect(self.sync_progress)
        self.ui.erdButton.clicked.connect(self.show_erd)

        # Disable the right click menu in the WebEngineView
        self.ui.questionTextArea.setContextMenuPolicy(Qt.NoContextMenu)
        self.ui.questionTextArea.setContextMenuPolicy(Qt.PreventContextMenu)

        self.ui.questionTextArea.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, True)
        self.ui.questionTextArea.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)

        # Set the initial Webview content - Credits
        self.ui.questionTextArea.setHtml('''
                                         <style>

                                         body {
                                           background-color: white;
                                         }

                                         h1 {
                                           text-align:center;
                                           text-decoration:underline;
                                           font-weight:bold;
                                         }
                                         
                                         .syntaxbox {
                                           box-sizing: border-box;
                                           border: 4px solid black;
                                           float: center;
                                           font: italic bold 15px Monospace;
                                           background: wheat;
                                           padding: 20px;
                                           margin-left: 40px;
                                           margin-right: 40px;
                                           text-align: center;
                                         }
                                         
                                         .examplebox {
                                           box-sizing: border-box;
                                           border: 4px solid black;
                                           float: center;
                                           font: bold 16px Arial;
                                           background: PaleTurquoise;
                                           padding: 20px;
                                           margin-left: 40px;
                                           margin-right: 40px;
                                           text-align: center;
                                         }
                                         
                                         </style>
                                         
                                         <body>
                                           <h1>My Query Tutor</h1>
                                           <div class="syntaxbox">
                                             <p>Software Developer</p>
                                             Steven Tucker
                                           </div>
                                           
                                           <div class="examplebox">
                                             <p>Content Developer</p>
                                             Peter Darcy
                                           </div>
                                           
                                           <div class="syntaxbox">
                                             <p>Content Designer</p>
                                             Keshlan Chinia
                                           </div>
                                         
                                         </body>
                                         ''')

        # Part of the horrible hack!!
        self.ui.queryTextArea.textChanged.connect(self.reset_font_query_edit)

        if not first_run:
            self.main_win.restoreGeometry(self.app_settings.get_geometry())
            self.ui.splitter.setSizes(self.app_settings.get_splitter_1_geometry())
            self.ui.splitter_2.setSizes(self.app_settings.get_splitter_2_geometry())
        else:
            self.splash_screen.show()
            self.ui.splitter.setSizes([393, 161])
            self.ui.splitter_2.setSizes([206, 565])

        self.splash_screen.finish(self.main_win)
        self.ui.questionTextArea.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, True)

    def __del__(self):
        if not self.settings_cancelled:
            self.app_settings.set_geometry(self.main_win.saveGeometry(),
                                           self.ui.splitter.sizes(),
                                           self.ui.splitter_2.sizes()
                                           )

    @staticmethod
    def initial_checks():
        db_ctrl = DatabaseController()
        db_ctrl.connect()
        return db_ctrl

    def show(self):
        self.main_win.show()

    def reset_font_query_edit(self):
        """
        Horrible, Horrible, Horrible Hack!
        Necessary to get around the font resetting if the current text is deleted
        Every time something changes, the font size is set
        """
        self.ui.queryTextArea.setFontPointSize(15)
        self.ui.queryTextArea.setFontWeight(-1)

    def show_erd(self):
        if self.question != '':
            image_dialog = QDialog()
            image_dialog.setModal(False)

            if self.erd is None:
                image_label = QLabel("No Diagram set for Question")
            else:
                image_label = QLabel(self.erd)
                image = QPixmap(os.path.join(self.dir_path, "images", self.erd))
                image_label.setPixmap(image.scaled(1024, 768, Qt.KeepAspectRatio))
            layout = QBoxLayout(QBoxLayout.LeftToRight)
            layout.addWidget(image_label)
            image_label.setScaledContents(True)
            image_label.setMinimumHeight(100)
            image_label.setMinimumWidth(100)
            image_dialog.setLayout(layout)
            image_dialog.setModal(False)
            image_dialog.exec()

    def run_query_clicked(self):
        query = self.ui.queryTextArea.toPlainText()
        if query != '':

            self.ui.syncButton.setText("Sync with server")
            self.ui.syncButton.setStyleSheet(" QPushButton { background-color : lightsalmon; color : black }")

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

            result_dialog = ExpectedResult(self.main_win, self.question, column_names, row_data, result_color)
            result_dialog.setModal(False)
            result_dialog.ui.textBrowser.setHtml(query_comparison_html)
            result_dialog.show()

    def expected_result_clicked(self):
        if self.question != '':
            query = self.db_ctrl.get_question_query(self.question_id)
            if query != '':
                column_names, row_data = self.db_ctrl.run_query(query)

                answer_dialog = ExpectedResult(
                    self.main_win,
                    'Expected Result for ' + self.question,
                    column_names,
                    row_data
                )

                answer_dialog.setModal(False)
                answer_dialog.ui.label_correct.setText('')
                answer_dialog.ui.textBrowser.deleteLater()
                answer_dialog.show()
    
    def help_clicked(self):
        if not self.topic == '':
            lesson = self.db_ctrl.get_lesson(self.topic)
            lesson_dialog = LessonDialog(self.main_win, self.topic, lesson)
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

        self.question_id, description, self.erd = self.db_ctrl.get_question(self.topic, self.question)

        global installer_building
        # Replace relative path to absolute
        soup = BeautifulSoup(description, "html.parser")
        for img in soup.findAll('img'):
            img['src'] = self.dir_path + os.sep + "images" + os.sep + img['src']

        for style in soup.find('style'):
            style_str = str(style)
            finds = re.findall('url\(.+?\)', style_str)
            for find in finds:
                sub_str = find[5:-2]
                if installer_building:
                    directory_path = self.dir_path[2:]
                    directory_path = directory_path.replace('\\', '/')
                    directory_path = 'C:' + directory_path
                else:
                    directory_path = self.dir_path
                new_url = 'url("file://' + directory_path + '/images/' + sub_str + '")'
                style_str = style_str.replace(find, new_url)
            style.replaceWith(BeautifulSoup(style_str))
        description = str(soup)

        self.ui.questionTextArea.setHtml(description)

        # Load last query attempted for this question if on exists
        last_query = self.db_ctrl.get_last_query(self.topic, self.question)
        self.ui.queryTextArea.setText(last_query)

    def show_progress(self):
        questions_map, questions_list = self.db_ctrl.get_questions_list()

        progress_dialog = ProgressDialog(self.main_win, questions_map, questions_list, self.db_ctrl)

        progress_dialog.setModal(False)
        progress_dialog.ui.label_correct.setText('')
        progress_dialog.ui.textBrowser.deleteLater()
        progress_dialog.show()

    def sync_progress(self):

        server_addr, class_key, ssl_set = self.app_settings.get_server_details()
        firstname, surname, email = self.app_settings.get_user_details()
        if ssl_set:
            protocol = "https"
            port = "443"
        else:
            protocol = "http"
            port = "80"

        if len(server_addr) == 0:
            self.update_server_settings(server_addr, class_key, ssl_set)
            return

        request_str = "{}://{}:{}/api/test?classcode={}".format(protocol, server_addr, port, class_key)
        try:
            request_data = requests.get(request_str)
            request_data.raise_for_status()
        except requests.HTTPError as http_err:
            print('HTTP ERROR: {http_err}')
            self.update_server_settings(server_addr, class_key, ssl_set)
            return
        except Exception as err:
            print('Error: {err}')
            self.update_server_settings(server_addr, class_key, ssl_set)
            return
        print("Test call successfull")

        sync_up_data = self.db_ctrl.get_sync_up_data(firstname, surname, email, self.app_settings.get_time_stamp())
        print(sync_up_data)

        # Send all rows that are not marked as sync'd, send last sync time stamp (empty if never sync'd)
        # On success, mark all entries in database as sync'd, then add all returned entries into the database (sync'd)
        request_str = "{}://{}:{}/api/sync?classcode={}".format(protocol, server_addr, port, class_key)
        try:
            request_data = requests.post(request_str, json=sync_up_data)
            request_data.raise_for_status()
        except requests.HTTPError as http_err:
            print('HTTP ERROR: {}'.format(http_err))
            self.update_server_settings(server_addr, class_key, ssl_set)
            return
        except Exception as err:
            print('Error: {}'.format(err))
            self.update_server_settings(server_addr, class_key, ssl_set)
            return

        # Add rows to the database.
        synced_down_data = request_data.json()
        print(synced_down_data)

        # Update timestamp from returned json
        self.app_settings.set_time_stamp(synced_down_data["timestamp"])
        # Mark all entries at synced
        self.db_ctrl.mark_synced()
        # insert new records.
        self.db_ctrl.insert_synced_records(synced_down_data["results"])
        # Change sync button to green if all completes successfully
        self.ui.syncButton.setText("In Sync")
        self.ui.syncButton.setStyleSheet(" QPushButton { background-color : lightgreen; color : black }")

    def update_server_settings(self, server_address, class_key, ssl):
        # Show dialog with server settings, test settings and return true on success, false on fail
        settings_dialog = SettingsDialog(self.main_win, self.app_settings, server_address, class_key, ssl)
        settings_dialog.exec()
        self.ui.syncButton.setText("Sync with server")
        self.ui.syncButton.setStyleSheet(" QPushButton { background-color : lightsalmon; color : black }")

    @staticmethod
    def compare_queries(exemplar_query, user_query):

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

        exemplar_list = exemplar_query.split()
        query_list = user_query.split()
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
