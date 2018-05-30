from app import app
import unittest


class TestRequests(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def create_request(self, title, type, description, category, area):
        request = {"title": "Leaking Pipe",
                   "type": "Repair",
                   "description": "Some description",
                   "category": "Plumbing",
                   "area": "Block A"}

        return self.client.post('/users/1/request', data=request)

    def test_create_request(self):
        res = client.post('/users/requests', data=request)
        self.assertEqual(res.status_code, 201)

    def test_update_request(self):
        res = client.put('/users/requests/1', data=request)
        self.assertEqual(res.status_code, 200)

    def test_all_requests(self):
        res = client.get('/users/requests')
        self.assertEqual(res.status_code, 200)

    def test_get_request(self):
        res = client.get('/users/requests/1')
        self.assertEqual(res.status_code, 200)

    def test_delete_request(self):
        res = client.delete('/users/request/1')
        self.assertEqual(res.status_code, 200)


if __name__ == "__main__":
    unittest.main()
