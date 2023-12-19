import unittest

from unittest.mock import patch, Mock
from flask import Flask, request
from main import visitor_count 

class TestVisitorCount(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)

    @patch('google.cloud.firestore.Client')
    def test_post_request(self, mock_firestore):
        with self.app.test_request_context('/path', method='POST'):
            mock_firestore.return_value.collection.return_value.document.return_value.get.return_value = Mock(exists=True, to_dict=lambda: {'count': 5})
            response = visitor_count(request)

        self.assertEqual(response.status_code, 200)

    def test_options_request(self):
        with self.app.test_request_context('/path', method='OPTIONS'):
            response = visitor_count(request)

        self.assertEqual(response.status_code, 204)
        

    def test_invalid_method(self):
        with self.app.test_request_context('/path', method='GET'):
            response = visitor_count(request)

        self.assertEqual(response.status_code, 405)

if __name__ == '__main__':
    unittest.main()
