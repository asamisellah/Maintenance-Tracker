from app import app
import unittest

class TestUsers(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def tearDown(self):
        self.users.clear()

    def register_user(self, name, email, password, confirm_password):
        users = {name: "Betty",
                email: "betty@email.com", 
                password: "qwe123",
                confirm_password: "qwe123"}
        
        return self.client.post('/register', data = users)

    def test_registration(self):
        res = client.post('/register', data = users)
        self.assertEqual(res.status_code, 201)

    
    def signin_user(self, email, password):
        user_account = {email: "betty@email.com", password: "qwe123"}

        return self.client.post('/sign_in', data = user_account)

    def test_sign_in(self):
        res = client.post('/sign_in', data = user_account)
        self.assertEqual(res.status_code, 200)

    
    def test_update_user(self):
        res = client.put('/users/1', data = request)
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

    # Test for edge-cases    

    def test_blank_registration(self):
        res = client.post('/register', data = register_user("", "", "", ""))
        self.assertEqual(res.status_code, 400)

    def test_signin_unregistered_user(self):
        res = client.post('/sign_in', data = signin_user("Betty", "qwe123"))
        self.assertEqual(res.status_code, 401)

        
if __name__ == "__main__":
    unittest.main()