from app import app
import unittest


class TestUsers(unittest.TestCase):
    users = {"name": "Betty", "email": "betty@email.com",
             "password": "qwe123", "confirm_password": "qwe123"}

    def setUp(self):
        self.client = app.test_client()

    def signin_user(self, email, password):
        user_account = {email: "betty@email.com", password: "qwe123"}

        return self.client.post('/sign_in', data=self.users)

    def test_sign_in(self):
        res = self.client.post('/sign_in', data=self.users)
        self.assertEqual(res.status_code, 200)  

    # Test for edge-cases    
    def test_blank_registration(self):
        res = self.client.post('/register', data="")
        self.assertEqual(res.status_code, 400)

    def test_signin_unregistered_user(self):
        res = self.client.post('/sign_in', data=self.users)
        self.assertEqual(res.status_code, 401)

        
if __name__ == "__main__":
    unittest.main()