from flask import Flask, jsonify, request
from psycopg2.extras import RealDictCursor
import uuid
from .model import User

from db_connect import TrackerDB

app = Flask(__name__)


# GET users
@app.route('/api/v1/users')
def get_users():
    return jsonify({"users": model.get_users()})


# POST a user
@app.route('/api/v1/users', methods=['POST'])
def create_user():
    new_user = model.User(
        str(uuid.uuid4),
        request.json.get("username"),
        request.json.get("email"),
        request.json.get("password")
    )
    # Confirm user input has data
    if new_user.username is None:
        return jsonify({"message": "All Fields Required"}), 400
    elif new_user.email is None:
        return jsonify({"message": "All Fields Required"}), 400
    elif new_user.email is None:
        return jsonify({"message": "All Fields Required"}), 400
    # Confirm password
    if new_user.password != request.json.get("confirm_password"):
        return jsonify({"message": "Your Passwords Don't Match"}), 400
    # Check if user already exists
    users = model.get_users()

    if len(users) != 0:
        for user in users:
            # print(user)
            if user["username"] == new_user.username:
                return jsonify({"message": "User already exists"}), 400
    new_user.create_user()
    return jsonify({"message": "Sign Up Successful"}), 201


# Sign in a user
@app.route('/api/v1/users/signin', methods=['POST'])
def signin_user():
    username = request.json.get("username")
    password = request.json.get("password")
    user = model.get_user(username)

    if user is not None:
        if user["username"] == username and user["password"] == password:
            return jsonify({"message": "Sign in Successful!"}), 202
        return jsonify({"message": "Wrong username or password"}), 401
    return jsonify({"message": "User Not Found"}), 404


# Sign out User
@app.route('/api/v1/users/signout', methods=['POST'])
def signout_user():
    """Check if session is empty"""
    if len(session) == 0:
        return jsonify({"message": "You must be Signed in to Sign out"}), 403
    session.pop("user_id", None)
    return jsonify({"message": "Sign out Successful"}), 200


# POST a request
@app.route('/api/v1/users/requests', methods=['POST'])
def create_request():
    if len(session) != 0:
        user_id = session["user_id"]
        request_data = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "title": request.json.get("title"),
            "type": request.json.get('type'),
            "description": request.json.get("description"),
            "category": request.json.get('category'),
            "area": request.json.get('area')
        }
        requests.append(request_data)
        return jsonify({"message": request_data}), 201
    return jsonify({"message": "Sign In to make a requests"}), 401


# GET all requests
@app.route('/api/v1/users/requests')
def get_requests():
    if len(session) != 0:
        user_id = session["user_id"]
        request_data = []
        for request in requests:
            if request["user_id"] == user_id:
                request_data.append(request)
        if len(request_data) == 0:
            return jsonify({
                "message": "You have no requests. Create a request"
            }), 200
        return jsonify({"requests": request_data}), 200
    return jsonify({"message": "Sign In to view requests"}), 403


# GET a request
@app.route('/api/v1/users/requests/<request_id>')
def get_request(request_id):
    if len(session) != 0:
        user_id = session["user_id"]
        request_data = []
        for request in requests:
            if request["id"] == request_id:
                request_data.append(request)
        if not request_data:
            return jsonify({"message": "Not found"}), 404

        if request_data[0]["user_id"] == user_id:
            if len(request_data) != 0:
                return jsonify({"request": request_data[0]}), 200
    return jsonify({"message": "Sign In to view requests"}), 403


# UPDATE(PUT) a request
@app.route('/api/v1/users/requests/<request_id>', methods=['PUT'])
def update_request(request_id):
    if len(session) != 0:
        user_id = session["user_id"]
        request_data = []
        for r in requests:
            if r["id"] == request_id:
                request_data.append(r)
        if request_data[0]["user_id"] == user_id:
            if len(request_data) != 0:
                request_data[0]["title"] = request.json.get(
                    "title", request_data[0]["title"])
                request_data[0]["type"] = request.json.get(
                    "type", request_data[0]["type"])
                request_data[0]["description"] = request.json.get(
                    "description", request_data[0]["description"])
                request_data[0]["category"] = request.json.get(
                    "category", request_data[0]["category"])
                request_data[0]["area"] = request.json.get(
                    "area", request_data[0]["area"])

                return jsonify({"requests": request_data[0]}), 200
            return jsonify({"message": "Request Not Found"}), 404
        return jsonify({"message": "Cannot Access Request"}), 403
    return jsonify({"message": "Sign In to view requests"}), 403


# DELETE a request
@app.route('/api/v1/users/requests/<request_id>', methods=['DELETE'])
def delete_request(request_id):
    if len(session) != 0:
        user_id = session["user_id"]
        request_data = []
        for request in requests:
            if request["id"] == request_id:
                request_data.append(request)
        if len(request_data) != 0:
            if request_data[0]["user_id"] == user_id:
                requests.remove(request_data[0])
                return jsonify({
                    "requests": "Request Successfully Deleted"
                }), 200
            return jsonify({"message": "Cannot Access Request"}), 403
        return jsonify({"message": "Not Found"}), 404
    return jsonify({"message": "Sign In to view requests"}), 403
