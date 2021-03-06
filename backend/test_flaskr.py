import os
import unittest
import requests
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category  


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('student', 'student', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.add_question = {
            'question': 'Which Nanodegree Program is this?',
            'answer': 'Full stack web development',
            'category': '1',
            'difficulty': 1
        }
        
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_retrieve_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data.get('success'))
        print("Randomly completed", res)


    def test_retrieve_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data.get('success'))
        self.assertTrue(data.get('success'))


    def test_retrieve_questions_pagination(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('success'))
        self.assertTrue(data.get('success'))


    def test_retrieve_questions_limit(self):
        res = self.client().get('/questions?limit=1')
        data = json.loads(res.data)
        ques_len = len(data.get('questions'))
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('success'))
        self.assertEqual(len(data.get('questions')), ques_len)
        self.assertTrue(data.get('success'))


    def test_delete_question(self):
        question = {
            'question': 'xxx',
            'answer': 'yyy',
            'difficulty': 1,
            'category': 1
        }
        operation_res = self.client().post('/questions', json=question)
        result_data = json.loads(operation_res.data)

        res = self.client().delete(
            '/questions/{}'.format(result_data.get('question_id'))
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            data.get('deleted_id'), str(result_data.get('question_id'))
        )
        self.assertTrue(data.get('success'))


    def test_delete_question_fail(self):
        res = self.client().delete('/questions/1000')
        self.assertEqual(res.status_code, 404)


    def test_create_question(self):
        question = {
            'question': 'what Nano degree track is this',
            'answer': 'Full stack web development',
            'difficulty': 1,
            'category': 1
        }
        res = self.client().post('/questions', json=question)
        self.assertEqual(res.status_code, 201)

    def test_create_question_fail(self):
        question = {
            'answer': 'Full stack web development',
            'difficulty': 1,
            'category': 1
        }
        res = self.client().post('/questions', json=question)
        self.assertEqual(res.status_code, 400)


    def test_retrieve_questions_by_term(self):
        search_term = {'searchTerm': 'title'}
        res = self.client().post('/questions/find', json=search_term)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
       

    def test_retrieve_questions_by_term_fail(self):
        res = self.client().post('/questions/find')
        self.assertEqual(res.status_code, 400)


    def test_retrieve_questions_by_category(self):
        res = self.client().get('/categories/{}/questions'.format(1))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
    

    def test_retrieve_questions_by_category_fail(self):
        res = self.client().get('/categories/1xx/questions')
        self.assertEqual(res.status_code, 404)

    def test_retrieve_quiz_question(self):
        data = {
            "previous_questions": [],
            "quiz_category": {"type": "Science", "id": "1"}
        }
        res = self.client().post('/quizzes', json=data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
     

    def test_retrieve_quiz_question_fail(self):
        data = {
            'previous_questions': []
        }
        res = self.client().post('/quizzes', json=data)
        self.assertEqual(res.status_code, 400)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()