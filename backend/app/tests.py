import json
from unittest.mock import MagicMock
from django.http import HttpRequest
from backend.controllers.users import signup
import unittest
from django.test import TestCase
from django.test import TestCase, RequestFactory



class TestSignUpUser(TestCase):
    def test_signup_user_success(self):

        factory = RequestFactory()
        request = factory.post('/users/signup/', data=json.dumps({
            'username': 'test_user',
            'email': 'test@example.com',
            'password': 'password'
        }), content_type='application/json')

        # Call the function
        response = signup(request)

        # Assertions
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertEqual(data['message'], 'User created successfully')


    # def test_signup_user_failure(self):
    #       # Create a mock POST request
    #     factory = RequestFactory()
    #     request = factory.post('/users/signup/', data=json.dumps({
    #         'username': 'test_user',
    #         'email': 'test@example.com',
    #         'password': 'password'
    #     }), content_type='application/json')

    #     # Call the function
    #     response = signup(request)

    #     # Assertions
    #     self.assertEqual(response.status_code, 405)



