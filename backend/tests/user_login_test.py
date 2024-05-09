import unittest
from unittest.mock import patch, MagicMock

# Manually configure Django settings
import django
from django.conf import settings

settings.configure(
    JWT_SECRET=""
)

# settings.configure(
#     DEBUG=True,
#     DATABASES={
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': ':memory:'
#         }
#     }
# )

# Import your Django components after configuring settings
from django.http import JsonResponse
from backend.controllers.users import login, generate_token

class TestLogin(unittest.TestCase):

    @patch('backend.controllers.users.get_db_handle')
    def test_login_success(self, mock_get_db_handle):
        # Mock database response
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_collection.find_one.return_value = {'_id': 'user_id', 'password': 'password', 'email': 'test@example.com'}
        mock_db.__getitem__.return_value = mock_collection
        mock_get_db_handle.return_value = (mock_db, MagicMock())

        # Mock request
        request = MagicMock(method='POST')
        request.body = '{"email": "test@example.com", "password": "password"}'

        # Call the login function
        response = login(request)

        # Check response status code and content
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.content.decode())
        self.assertIn('user_id', response.content.decode())
        self.assertIn('token', response.content.decode())

    @patch('backend.controllers.users.get_db_handle')
    def test_login_user_not_found(self, mock_get_db_handle):
        # Mock database response
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_collection.find_one.return_value = None
        mock_db.__getitem__.return_value = mock_collection
        mock_get_db_handle.return_value = (mock_db, MagicMock())

        # Mock request
        request = MagicMock(method='POST')
        request.body = '{"email": "nonexistent@example.com", "password": "password"}'

        # Call the login function
        response = login(request)

        # Check response status code and content
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.content.decode())

    @patch('backend.controllers.users.get_db_handle')
    def test_login_password_incorrect(self, mock_get_db_handle):
        # Mock database response
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_collection.find_one.return_value = {'_id': 'user_id', 'password': 'hashed_password'}
        mock_db.__getitem__.return_value = mock_collection
        mock_get_db_handle.return_value = (mock_db, MagicMock())

        # Mock request
        request = MagicMock(method='POST')
        request.body = '{"email": "test@example.com", "password": "incorrect_password"}'

        # Call the login function
        response = login(request)

        # Check response status code and content
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.content.decode())

    # Additional tests for method not allowed, exception cases, etc.

if __name__ == '__main__':
    unittest.main()
