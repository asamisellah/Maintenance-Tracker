from app import app
import unittest
import json
from config import config
from app.model import drop, init, db, make_user_admin, update_status


class TestRequests(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.config.from_object(config['testing'])
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
            "request": {
                "title": "Leaking Pipe",
                "_type": "Repair",
                "description": "Some description",
                "category": "Plumbing",
                "area": "Block A"
            }
        }

    def tearDown(self):
        drop()

    def signup_and_signin_user(self):
        # Sign up user
        self.client.post(
            '/api/v1/auth/signup',
            data=json.dumps(dict(self.data["user"])),
            content_type='application/json'
        )

        # Sign in user
        res = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps(dict(self.data["auth"])),
            content_type='application/json'
        )
        access_token = json.loads(res.data.decode())["token"]
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        return headers

    def test_approve_request(self):
        header = self.signup_and_signin_user()
        res_post = self.client.post(
            '/api/v1/users/requests', headers=header,
            data=json.dumps(dict(self.data["request"])),
            content_type='application/json',
        )
        self.assertEqual(res_post.status_code, 201)
        request_id = json.loads(res_post.data.decode())["data"]["id"]
        make_user_admin()

        res = self.client.put(
            '/api/v1/requests/{}/approve'.format(request_id), headers=header)
        self.assertEqual(res.status_code, 200)

    def test_disapprove_request(self):
        header = self.signup_and_signin_user()
        res_post = self.client.post(
            '/api/v1/users/requests', headers=header,
            data=json.dumps(dict(self.data["request"])),
            content_type='application/json',
        )
        self.assertEqual(res_post.status_code, 201)
        request_id = json.loads(res_post.data.decode())["data"]["id"]
        make_user_admin()

        res = self.client.put(
            '/api/v1/requests/{}/disapprove'.format(request_id),
            headers=header)
        self.assertEqual(res.status_code, 200)

    def test_resolve_request(self):
        header = self.signup_and_signin_user()
        res_post = self.client.post(
            '/api/v1/users/requests', headers=header,
            data=json.dumps(dict(self.data["request"])),
            content_type='application/json',
        )
        self.assertEqual(res_post.status_code, 201)
        request_id = json.loads(res_post.data.decode())["data"]["id"]
        make_user_admin()

        update_status(1, "approved")
        res = self.client.put(
            '/api/v1/requests/{}/resolve'.format(request_id), headers=header)
        self.assertEqual(res.status_code, 200)

    def test_get_all_request(self):
        header = self.signup_and_signin_user()
        res_post = self.client.post(
            '/api/v1/users/requests', headers=header,
            data=json.dumps(dict(self.data["request"])),
            content_type='application/json',
        )
        self.assertEqual(res_post.status_code, 201)
        make_user_admin()

        res = self.client.get(
            '/api/v1/requests', headers=header)
        self.assertEqual(res.status_code, 200)
