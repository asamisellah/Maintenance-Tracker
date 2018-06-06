from app import app
import unittest
import json


class TestRequests(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        self.session = {}
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
                "type": "Repair",
                "description": "Some description",
                "category": "Plumbing",
                "area": "Block A"
            },
            "newrequest": {
                "title": "MakeMe",
                "type": "Repair",
                "description": "Some description",
                "category": "Plumbing",
                "area": "Block A"
            }
        }

    def signup_and_signin_user(self):
        # Sign up user
        self.client.post(
            '/api/v1/users',
            data=json.dumps(dict(self.data["user"])),
            content_type='application/json'
        )

        # Sign in user
        self.client.post(
            '/api/v1/users/signin',
            data=json.dumps(dict(self.data["auth"])),
            content_type='application/json'
        )

    def test_create_request(self):
        self.signup_and_signin_user()
        res = self.client.post(
            '/api/v1/users/requests',
            data=json.dumps(dict(self.data["request"])),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 201)

    def test_get_requests(self):
        res = self.client.get('/api/v1/users/requests')
        self.assertEqual(res.status_code, 200)

    def test_get_request(self):
        self.signup_and_signin_user()
        res = self.client.post(
            '/api/v1/users/requests',
            data=json.dumps(dict(self.data["request"])),
            content_type='application/json'
        )

        self.assertEqual(res.status_code, 201)

        request_id = json.loads(res.data.decode())['message']['id']
        res = self.client.get('/api/v1/users/requests/{}'.format(request_id))
        self.assertEqual(res.status_code, 200)

    def test_update_request(self):
        self.signup_and_signin_user()
        res = self.client.post(
            '/api/v1/users/requests',
            data=json.dumps(dict(self.data["request"])),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 201)
        request_id = json.loads(res.data.decode())['message']['id']
        res = self.client.put(
            '/api/v1/users/requests/{}'.format(request_id),
            data=json.dumps(dict(self.data['newrequest'])),
            content_type='application/json')
        title = json.loads(res.data.decode())['requests']['title']
        id = json.loads(res.data.decode())['requests']['id']

        self.assertEqual(title, 'MakeMe')
        self.assertEqual(id, request_id)
        self.assertEqual(res.status_code, 200)

    def test_delete_request(self):
        self.signup_and_signin_user()
        res = self.client.post(
            '/api/v1/users/requests',
            data=json.dumps(dict(self.data["request"])),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 201)
        request_id = json.loads(res.data.decode())['message']['id']

        res = self.client.delete(
            '/api/v1/users/requests/{}'.format(request_id))
        self.assertEqual(res.status_code, 200)

    # Edge Cases
    def test_unexisting_request(self):
        res = self.client.get('/api/v1/users/requests/747429723')
        self.assertEqual(res.status_code, 404)

    def test__request(self):
        # Sign-up, Sign-in and Create a request
        self.signup_and_signin_user()
        res = self.client.post(
            '/api/v1/users/requests',
            data=json.dumps(dict(self.data["request"])),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 201)
        request_id = json.loads(res.data.decode())['message']['id']

        # Sign-out
        res = self.client.post('/api/v1/users/signout')
        self.assertEqual(res.status_code, 200)

        # Get the request
        res = self.client.get('/api/v1/users/requests/{}'.format(request_id))
        self.assertEqual(res.status_code, 403)


if __name__ == "__main__":
    unittest.main()
