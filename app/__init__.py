from flask import Flask, jsonify

app = Flask(__name__)

user = [
    {
        "name": "betty",
        "email": "betty@email.com",
        "password": "qwe123",
        "confirm_password": "qwe123",
        "request": [
            {
                "title": "Leaking pipe",
                "type": "Repair",
                "description": "Rusty pipe",
                "category": "plumbing",
                "area": "Block A"
            }
        ]
    }
]


# Create user
@app.route('/user', method=['POST'])
def create(user):
    pass


# # Get user
# @app.route('/user/<string:name>')
# def get_user(user):
#     return jsonify({"user": user})


# Get all users
@app.route('/user')
def get_users(user):
    return jsonify({"user": user})


# # Create user request
# @app.route('/user/<string:name>/request', method=['POST'])
# def create_request():
#     pass


# # Get user request
# @app.route('/user/<string:name>/request/<string:title>')
# def get_request():
#     pass


# # Get all user requests
# @app.route('/user/<string:name>/request')
# def get_requests():
#     pass

