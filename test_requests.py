from app import app
import unittest
import json


class TestRequests(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        self.request = {
            "id": "1",
            "title": "Leaking Pipe",
            "type": "Repair",
            "description": "Some description",
            "category": "Plumbing",
            "area": "Block A"
        }

    def test_create_request(self):
        res = self.client.post(
            '/api/v1/users/requests',
            data=json.dumps(dict(self.request)),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 201)

    def test_get_requests(self):
        res = self.client.get('/api/v1/users/requests')
        self.assertEqual(res.status_code, 200)

    def test_get_request(self):
        res = self.client.post(
            '/api/v1/users/requests',
            data=json.dumps(dict(self.request)),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 201)
        res = self.client.get('/api/v1/users/requests/0')
        self.assertEqual(res.status_code, 200)

    def test_delete_request(self):
        res = self.client.delete('/api/v1/users/requests/0')
        self.assertEqual(res.status_code, 204)


if __name__ == "__main__":
    unittest.main()
