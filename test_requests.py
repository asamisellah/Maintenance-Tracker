from app import app
import unittest
import json


class TestRequests(unittest.TestCase):
    request = {
        "id": "1",
        "title": "Leaking Pipe",
        "type": "Repair",
        "description": "Some description",
        "category": "Plumbing",
        "area": "Block A"

    }

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_create_request(self):
        res = self.client.post('/api/v1/users/requests',
                               data=json.dumps(dict(TestRequests.request)),
                               content_type='application/json')
        self.assertEqual(res.status_code, 201)

    def test_get_requests(self):
        res = self.client.get('/api/v1/users/requests')
        self.assertEqual(res.status_code, 200)

    def test_get_request(self):
        res = self.client.get('/api/v1/users/requests/1')
        self.assertEqual(res.status_code, 200)

    # def test_update_request(self):
    #     res = self.client.put('/users/requests/1', data=self.request)
    #     self.assertEqual(res.status_code, 200)


    # def test_delete_request(self):
    #     res = self.client.delete('/users/request/1')
    #     self.assertEqual(res.status_code, 200)


if __name__ == "__main__":
    unittest.main()
