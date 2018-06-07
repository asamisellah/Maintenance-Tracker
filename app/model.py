

class User():
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def create_user(self):
        users.append(self)

    def retrieve_user(self, username):
        for user in users:
            if user.username == username:
                return user.serialize()

    def serialize(self):
        return {
            "username": self.username
            "email": self.email
            "password": self.password
        }
