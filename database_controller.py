import os
import json
import sqlite3
import collections
from PyQt5.QtCore import QStandardPaths


class DatabaseController:
    def __init__(self):
        self.app_file_path = None
        self.ex_file_path = None
        self.app_db = None
        self.ex_db = None
        self.app_cursor = None
        self.ex_cursor = None

    def connect(self):
        dir_path = QStandardPaths.writableLocation(QStandardPaths.AppLocalDataLocation)
        self.app_file_path = os.path.join(dir_path, 'MQT_APP.sqlite')
        self.ex_file_path = os.path.join(dir_path, 'MQT_EX.sqlite')
        self.app_db = sqlite3.connect(self.app_file_path)
        self.ex_db = sqlite3.connect(self.ex_file_path)
        self.app_cursor = self.app_db.cursor()
        self.ex_cursor = self.ex_db.cursor()

    def close_databases(self):
        self.app_db.close()
        self.ex_db.close()

    def get_questions_list(self):
        self.app_cursor.execute(
            """
                SELECT Topic.name, Question.title, Topic.position
                FROM Topic, Question 
                WHERE Question.topicId = Topic.id
                ORDER BY Topic.position ASC
            """
        )
        questions_list = self.app_cursor.fetchall()
        questions_map = {}

        for question in questions_list:
            if question[0] in questions_map:
                questions_map[question[0]].append(question[1])
            else:
                questions_map[question[0]] = [question[1]]

        questions = []
        for item in questions_list:
            if item[0] not in questions:
                questions.append(item[0])

        return questions_map, questions

    def get_lesson(self, topic):
        self.app_cursor.execute(
            """
                SELECT lesson
                FROM Topic
                WHERE name = :topic
            """,
            {'topic': topic}
        )
        return self.app_cursor.fetchone()[0]

    def get_question(self, topic, question):
        self.app_cursor.execute(
            """
                SELECT Question.id, description, ERD
                FROM Topic, Question 
                WHERE Question.topicId = Topic.id
                AND Topic.name = :topic
                AND Question.title = :question
            """,
            {'topic': topic, 'question': question}
        )
        result = self.app_cursor.fetchone()
        return result[0], result[1], result[2]

    def run_query(self, query_string):
        try:
            self.ex_cursor.execute(query_string)
            col_names = self.ex_cursor.description
            data = self.ex_cursor.fetchall()
        except sqlite3.Error as e:
            col_names = [['Query Error']]
            data = [[e.args[0]]]

        columns = []
        for row in col_names:
            columns.append(row[0])

        return columns, data

    def get_question_query(self, qid):
        self.app_cursor.execute(
            """
                SELECT resultQuery 
                FROM Question 
                WHERE id = :qid
            """,
            {'qid': qid}
        )
        return self.app_cursor.fetchone()[0]

    def get_last_query(self, topic, question):
        self.app_cursor.execute(
            """
                Select query 
                FROM Queries
                WHERE Queries.topic_id = (
                    SELECT Topic.id
                    FROM Topic
                    WHERE Topic.name = :topic
                )
                AND Queries.question_id = (
                    SELECT Question.id
                    FROM Question
                    WHERE Question.title = :question
                )
            """,
            {'topic': topic, 'question': question}
        )
        result = self.app_cursor.fetchone()

        if result is None:
            return ''
        else:
            return result[0]

    def set_question_query(self, query_string, topic, question, success):

        # Check for insert or update
        exists = self.get_last_query(topic, question)
        if exists == '':
            self.app_cursor.execute(
                """
                    INSERT INTO Queries (question_id, topic_id, query, success)
                    VALUES (
                        (
                            SELECT Question.id
                            FROM Question
                            WHERE Question.title = :question
                        ),
                        (
                            SELECT Topic.id
                            FROM Topic
                            WHERE Topic.name = :topic
                        ),
                        :query, :success
                    )
                """,
                {'question': question, 'topic': topic, 'query': query_string, 'success': success}
            )
        else:
            self.app_cursor.execute(
                """
                    UPDATE Queries
                    SET query = :query, success = :success, attempts = (attempts + 1), synced = 0
                    WHERE question_id = (
                        SELECT Question.id
                        FROM Question
                        WHERE Question.title = :question
                    )
                    AND topic_id = (
                        SELECT Topic.id
                        FROM Topic
                        WHERE Topic.name = :topic
                    )
                """,
                {'question': question, 'topic': topic, 'query': query_string, 'success': success}
            )

        self.app_db.commit()

    def is_successful(self, topic, question):
        self.app_cursor.execute(
            """
                SELECT success
                FROM Queries
                WHERE question_id = (
                        SELECT Question.id
                        FROM Question
                        WHERE Question.title = :question
                    )
                    AND topic_id = (
                        SELECT Topic.id
                        FROM Topic
                        WHERE Topic.name = :topic
                    )
            """,
            {'question': question, 'topic': topic}
        )
        result = self.app_cursor.fetchone()

        if result is None:
            return -1
        else:
            return result[0]

    def get_progress_json(self):
        self.app_cursor.execute(
            """
                SELECT topic.name, q.title, qry.success
                FROM topic, Question AS q, Queries AS qry
                WHERE qry.topic_id = topic.id
                AND qry.question_id = q.id
                ORDER BY topic.name
            """
        )
        result = self.app_cursor.fetchall()
        progress_map = {}
        for attempt in result:
            if attempt[0] in progress_map:
                progress_map[attempt[0]][attempt[1]] = attempt[2]
            else:
                progress_map[attempt[0]] = {attempt[1]: attempt[2]}

        json_str = json.dumps(progress_map)

        return json_str

    def get_sync_up_data(self, firstname, surname, email, timestamp):
        self.app_cursor.execute(
            """
                SELECT name, title, query, success, attempts
                FROM topic, Question, Queries
                WHERE Queries.question_id = Question.id
                AND Queries.topic_id = topic.id
                AND synced = 0
                ORDER BY name
            """
        )
        result = self.app_cursor.fetchall()
        results_list = []
        for row in result:
            results_list.append(
                {"topic": row[0], "pass": row[3], "query": row[2], "question": row[1], "attempts": row[4]}
            )

        send_data = {
            "student":
                {
                    "firstname": "{}".format(firstname),
                    "lastname": "{}".format(surname),
                    "email": "{}".format(email)
                },
            "timestamp": timestamp,
            "results": results_list
        }

        return send_data

    def mark_synced(self):
        self.app_cursor.execute(
            """
                UPDATE Queries
                SET synced = 1
                WHERE synced = 0
            """
        )

    def insert_synced_records(self, records):
        for record in records:
            self.app_cursor.execute(
                """
                    INSERT INTO Queries (question_id, topic_id, query, success, attempts, synced)
                    VALUES (
                        (
                            SELECT Question.id
                            FROM Question
                            WHERE Question.title = :question
                        ),
                        (
                            SELECT Topic.id
                            FROM Topic
                            WHERE Topic.name = :topic
                        ),
                        :query, :success, :attempts, 1
                    )
                """,
                {
                    'question': record["question"],
                    'topic': record["topic"],
                    'query': record["query"],
                    'success': record["pass"],
                    'attempts': record["attempts"]
                }
            )
        self.app_db.commit()
