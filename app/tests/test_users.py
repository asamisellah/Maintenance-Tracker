import unittest

from app import app


class TestUsers(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        users = {
            "name": "Betty",
            "email": "betty@email.com",
            "password": "qwe123",
            "confirm_password": "qwe123"
        }

    def tearDown(self):
        users.clear()

    def register_user(self, name, email, password, confirm_password):
        return self.client.post('/register', data=users)

    def test_registration(self):
        res = client.post('/register', data=users)
        self.assertEqual(res.status_code, 201)

    
    def signin_user(self, email, password):
        users = {email: "betty@email.com", password: "qwe123"}
        return self.client.post('/sign_in', data=user)

    def test_sign_in(self):
        res = client.post('/sign_in', data=user_account)
        self.assertEqual(res.status_code, 200)

    def test_all_users(self):
        res = client.get('/users')
        self.assertEqual(res.status_code, 200)
    
    def test_get_user(self):
        res = client.get('/users/1')
        self.assertEqual(res.status_code, 200)

    def test_delete_user(self):
        res = client.delete('/users/1')
        self.assertEqual(res.status_code, 200)

    
    # Tests for edge cases

    # def test_all_requests(self):
    #     res = client.get('/users/requests')
    #     self.assertEqual(res.status_code, 200)
    
    # def test_get_request(self):
    #     res = client.get('/users/requests/1')
    #     self.assertEqual(res.status_code, 200)

    # def test_delete_request(self):
    #     res = client.delete('/users/request/1')
    #     self.assertEqual(res.status_code, 200)
