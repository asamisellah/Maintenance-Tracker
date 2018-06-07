from flask import Blueprint, jsonify, request
from flask.views import MethodView
from model import User

users = Blueprint('users', __name__)


@users.route('/api/v1/users')
def create_user():
    user = User(

    )
    return user.create_user()


# class User(MethodView):
#     def get(self):
#         return jsonify({"message": "working"})
#     def post(self)
# users_view = User.as_view('user_api')
# users.add_url_rule(
#     '/signup',
#     view_func=users_view,
#     methods=['GET']
# )
