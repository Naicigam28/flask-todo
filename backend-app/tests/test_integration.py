import unittest
from flask import Flask
from app.app import app, db, Todo
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class IntegrationTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://usr:pwd@0.0.0.0:5432/todos"
        self.app = app.test_client()
        self.engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()
        self.session.close()
        self.engine.dispose()

    def test_create_and_get_todo(self):
        # Create a new todo
        response = self.app.post('/todos', data={'description': 'Test todo'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Retrieve the created todo from the database
        with app.app_context():
            todo = self.session.query(Todo).filter_by(description='Test todo').first()
            self.assertIsNotNone(todo)

        # Check if the response contains the created todo
        response = self.app.get('/todos')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test todo', response.data)

if __name__ == '__main__':
    unittest.main()
