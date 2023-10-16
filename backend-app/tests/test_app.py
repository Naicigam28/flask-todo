import unittest

from flask import Flask
import app
from app import app, db, Todo

class FlaskTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory SQLite database for testing
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_create_todo(self):
        response = self.app.post('/todos', data={'description': 'Test todo'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_get_todos(self):
        # Create a test todo
        with app.app_context():
            db.session.add(Todo(description='Test todo'))
            db.session.commit()

        response = self.app.get('/todos')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test todo', response.data)

if __name__ == '__main__':
    unittest.main()
