from flask import Flask, jsonify

app = Flask(__name__)

user = [
    {
        "name": "betty",
        "email": "betty@email.com",
        "password": "qwe123",
        "confirm_password": "qwe123"
        "request": [
            {
                "title": "Leaking pipe"
                "type": "Repair"
                "description": "Rusty pipe"
                "category": "plumbing"
                "area": "Block A"
            }
        ]
    }
]


@app.route('/user', method=['POST'])
def create(user):
    get


    # @app.route('user/<string:name>')
    # def get_user(name):
    #     pass

    # @app.route('/user')
    # def get_users():
    #     pass

    # @app.route('/user/<string:name>/request', method=['POST'])
    # def create_request():
    #     pass

    # @app.route('/user/<string:name>/request')
    # def get_requests():
    #     pass

    # @app.route('/user/<string:name>/request/<string:id>')
    # def get_request():
    #     pass
