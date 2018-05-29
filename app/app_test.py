from app import app
import unittest


class RequestsTest(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_requests_creation(self):
        res = self.client.post('api/v1/users/requests', data = {
            "title": "Leaking Pipe",
            "type": "Repair",
            "description": "Some description",
            "category": "Plumbing",
            "area": "Block A"
        })

        self.assertEqual(res.status_code, 201)

    def test_requests_updating(self):
        res = self.client.put('api/v1/users/requests/1', data = {
            "title": "Leaking Pipe",
            "type": "Repair",
            "description": "Some description",
            "category": "Plumbing",
            "area": "Block A"
        })

        self.assertEqual(res.status_code, 200)

    def test_requests_get(self):
        res = self.client.put('api/v1/users/requests')
        self.assertEqual(res.status_code, 200)

if __name__ == "__main__":
    unittest.main()
