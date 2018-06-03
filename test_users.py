from app import app
import unittest
import json


class TestUsers(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.data = {
            "user": {
                "username": "Betty",
                "email": "betty@email.com",
                "password": "qwe123",
                "confirm_password": "qwe123"
            },
            "auth": {
                "username": "Betty",
                "password": "qwe123",
            }

        }

    def test_create_user(self):
        res = self.client.post(
            '/api/v1/users',
            data=json.dumps(dict(self.data["user"])),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 201)

    def test_signin_user(self):
        res = self.client.post(
            '/api/v1/users/signin',
            data=json.dumps(dict(self.data["auth"])),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 202)

    def test_empty_field(self):
        self.data["user"]["username"] = ""
        res = self.client.post(
            '/api/v1/users',
            data=json.dumps(dict(self.data["user"])),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)

    # Test if
    def test_confirm_password(self):
        self.data["user"]["confirm_password"] = "random"
        res = self.client.post(
            '/api/v1/users',
            data=json.dumps(dict(self.data["user"])),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 400)

    def test_signin_unregistered_user(self):
        res = self.client.post('/api/v1/signin', data=self.data["auth"])
        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()
