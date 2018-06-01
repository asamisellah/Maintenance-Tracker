from app import app
import unittest
import json


class TestUsers(unittest.TestCase):
    user = {
        "username": "Betty",
        "email": "betty@email.com",
        "password": "qwe123",
        "confirm_password": "qwe123"
        }

    def setUp(self):
        self.client = app.test_client()

    def test_create_user(self):
        res = self.client.post('/api/v1/users',
                               data=json.dumps(dict(TestUsers.user)),
                               content_type='application/json')
        self.assertEqual(res.status_code, 201)

    def test_signin_user(self):
        res = self.client.post('/api/v1/users/signin',
                               data=json.dumps(dict(TestUsers.user)),
                               content_type='application/json')
        self.assertEqual(res.status_code, 202)

    # Test for edge-cases
    def test_blank_registration(self):
        res = self.client.post('/register', data="")
        self.assertEqual(res.status_code, 400)

    def test_signin_unregistered_user(self):
        res = self.client.post('/sign_in', data=self.users)
        self.assertEqual(res.status_code, 401)


if __name__ == "__main__":
    unittest.main()
