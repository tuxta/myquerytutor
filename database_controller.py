import sqlite3
import os


class DatabaseController:
    def __init__(self):
        self.app_file_path = None
        self.ex_file_path = None
        self.app_db = None
        self.ex_db = None
        self.app_cursor = None
        self.ex_cursor = None

    def connect(self):
        self.app_file_path = os.path.join(os.path.dirname(__file__), 'MQT_APP.sqlite')
        self.ex_file_path = os.path.join(os.path.dirname(__file__), 'MQT_EX.sqlite')
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
                SELECT Question.id, description 
                FROM Topic, Question 
                WHERE Question.topicId = Topic.id
                AND Topic.name = :topic
                AND Question.title = :question
            """,
            {'topic': topic, 'question': question}
        )
        result = self.app_cursor.fetchone()
        return result[0], result[1]

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
                    SET query = :query, success = :success
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
        return "We have some progress \o/"
