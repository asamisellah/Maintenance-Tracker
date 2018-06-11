from app import app
import unittest
import json
from config import config
from app.model import drop, init, db


class TestUsers(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.config.from_object(config['testing'])
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.init_app(self.app)
        self.client = self.app.test_client()
        init()
        self.data = {
            "user": {
                "username": "Betty",
                "email": "betty@email.com",
                "password": "qwe123",
                "confirm_password": "qwe123"
            },
            "auth": {
                "username": "Betty",
                "password": "qwe123"
            },
            "non_user": {
                "username": "Larry",
                "password": "qwe123"
            }
        }

    def tearDown(self):
        drop()

    def test_create_user(self):
        res = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps(dict(self.data["user"])),
            content_type='application/json'
        )

        self.assertEqual(res.status_code, 201)

    def test_signin_user(self):
        res = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps(dict(self.data["user"])),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 201)

        res = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps(dict(self.data["auth"])),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 202)

    def test_empty_field(self):
        self.data["user"]["username"] = ""
        res = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps(dict(self.data["user"])),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 400)

    def test_whitespace_passed_as_input(self):
        self.data["user"]["username"] = " "
        res = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps(dict(self.data["user"])),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 400)

    def test_input_not_string(self):
        self.data["user"]["username"] = 18347
        res = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps(dict(self.data["user"])),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 400)

    def test_wrong_email_format(self):
        self.data["user"]["email"] = "betty.com"
        res = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps(dict(self.data["user"])),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 400)

    def test_confirm_password(self):
        self.data["user"]["confirm_password"] = "random"
        res = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps(dict(self.data["user"])),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 400)

    def test_signin_unregistered_user(self):
        res = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps(dict(self.data["non_user"])),
            content_type='application/json'
        )

        res = self.client.post('/api/v1/signin', data=self.data["auth"])
        self.assertEqual(res.status_code, 404)

    def test_same_user_registration(self):
        self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps(dict(self.data["user"])),
            content_type='application/json'
        )

        res = self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps(dict(self.data["user"])),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 400)


if __name__ == "__main__":
    unittest.main()
