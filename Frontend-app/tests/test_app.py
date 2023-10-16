import unittest
import requests
from flask import Flask
from app import app  

class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_index_route(self):
        # Mock the response for the requests.get method
        class MockResponse:
            def json(self):
                return [{'id': 1, 'task': 'Sample Task'}]

        def mock_get(*args, **kwargs):
            return MockResponse()

        # Monkey-patch requests.get with the mock_get function
        requests.get = mock_get

        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sample Task', response.data)

if __name__ == '__main__':
    unittest.main()
