import sqlite3


class DatabaseController:
    def __init__(self):
        self.app_db = sqlite3.connect('MQT_APP.sqlite')
        self.ex_db = sqlite3.connect('MQT_EX.sqlite')

        self.app_cursor = self.app_db.cursor()
        self.ex_cursor = self.ex_db.cursor()

    def close_databases(self):
        self.app_db.close()
        self.ex_db.close()

    def get_questions_list(self):
        self.app_cursor.execute(
            """
                SELECT Topic.name, Question.title 
                FROM Topic, Question 
                WHERE Question.topicId = Topic.id
            """
        )
        questions_list = self.app_cursor.fetchall()
        questions_map = {}

        for question in questions_list:
            if question[0] in questions_map:
                questions_map[question[0]].append(question[1])
            else:
                questions_map[question[0]] = [question[1]]

        return questions_map

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

    def set_question_query(self, query_string, topic, question):

        # Check for insert or update
        exists = self.get_last_query(topic, question)
        if exists == '':
            self.app_cursor.execute(
                """
                    INSERT INTO Queries (question_id, topic_id, query)
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
                        :query
                    )
                """,
                {'question': question, 'topic': topic, 'query': query_string}
            )
        else:
            self.app_cursor.execute(
                """
                    UPDATE Queries
                    SET query = :query
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
                {'question': question, 'topic': topic, 'query': query_string}
            )

        self.app_db.commit()
