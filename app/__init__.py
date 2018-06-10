from flask import Flask, jsonify, request
from psycopg2.extras import RealDictCursor
from .model import *
import os
import re
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET')

jwt = JWTManager(app)


# POST a user
@app.route('/api/v1/auth/signup', methods=['POST'])
def create_user():
    # Ensure input is in json format
    if not request.is_json:
        return jsonify({"msg": "Invalid data format"}), 400
    for key in request.json:
        # Ensure input contains data
        if request.json[key] == "":
            return jsonify({"message": "All Fields Required"}), 400
        # Ensure input data is a string
        elif type(request.json[key]) != str:
            return jsonify({"message": "Input Must be a String"}), 400
    match = re.search(r'\w+@\w+', request.json.get("email"))
    if match is None:
        return return jsonify({"message": "Your Passwords Don't Match"}), 400
    new_user = User(
        request.json.get("username").lower(),
        request.json.get("email").lower(),
        request.json.get("password")
    )
    # Confirm password
    if new_user.password != request.json.get("confirm_password"):
        return jsonify({"message": "Your Passwords Don't Match"}), 400
    # Check if user already exists
    users = get_users()

    if len(users) != 0:
        for user in users:
            if user["username"] == new_user.username:
                return jsonify({"message": "User already exists"}), 400
    new_user.create_user()
    return jsonify({"message": "Sign Up Successful"}), 201


# Sign in a user
@app.route('/api/v1/auth/login', methods=['POST'])
def signin_user():
    # Ensure input is in json format
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    # Get input
    _username = request.json.get("username").lower()
    _password = request.json.get("password")
    # Confirm user exists
    user = get_user(_username)
    if user is not None:
        # Validate user credentials
        if user["username"] == _username and verify_hash(_password, user["password"]):
            # Login user and generate Access Token
            access_token = create_access_token(identity=user["id"])
            return jsonify({
                "message": "Sign in Successful!", "token": access_token}), 202
        return jsonify({"message": "Wrong username or password"}), 401
    return jsonify({"message": "Not Found. Sign up to create an account"}), 404


# POST a request
@app.route('/api/v1/users/requests', methods=['POST'])
@jwt_required
def create_request():
    # pass user_id from token
    user_id = get_jwt_identity()
    # Ensure input is in json format
    if not request.is_json:
        return jsonify({"msg": "Invalid data format"}), 400
    for key in request.json:
        # Ensure input contains data
        if request.json[key] == "":
            return jsonify({"message": "All Fields Required"}), 400
        # Ensure input data is a string
        elif type(request.json[key]) != str:
            return jsonify({"message": "Input Must be a String"}), 400
    # create new request
    request_data = UserRequest(
        user_id,
        request.json.get("title").lower(),
        request.json.get("description").lower(),
        request.json.get("_type").lower(),
        request.json.get("category").lower(),
        request.json.get("area").lower()
    )
    new_request = request_data.create_request()
    return jsonify({"message": "Request Created Successfully",
                    "data": new_request}), 201


# GET all requests of logged in user
@app.route('/api/v1/users/requests')
@jwt_required
def user_get_requests():
    user_id = get_jwt_identity()
    requests = get_user_requests(user_id)
    # Check if request exists
    if len(requests) == 0:
        return jsonify({
            "message": "You have no requests. Create a request"
        }), 404
    # Return if exists
    return jsonify({"requests": requests}), 200


# GET a request of logged in user
@app.route('/api/v1/users/requests/<request_id>')
@jwt_required
def user_get_request(request_id):
    user_id = get_jwt_identity()
    user_request = get_user_request(request_id, user_id)
    if user_request is not None:
        return jsonify({"request": user_request}), 200
    return jsonify({
        "message": "Request Not Found"}), 404


# UPDATE(PUT) a request
@app.route('/api/v1/users/requests/<request_id>', methods=['PUT'])
@jwt_required
def user_update_request(request_id):
    user_id = get_jwt_identity()
    user_request = get_user_request(request_id, user_id)

    # Ensure input is in json format
    if not request.is_json:
        return jsonify({"msg": "Invalid data format"}), 400
    for key in request.json:
        # Ensure input contains data
        if request.json[key] == "":
            return jsonify({"message": "All Fields Required"}), 400
        # Ensure input data is a string
        elif type(request.json[key]) != str:
            return jsonify({"message": "Input Must be a String"}), 400

    # Ensure request has been fetched
    if user_request is not None:
        update_request(request_id,
                       user_id,
                       request.json.get("title").lower(),
                       request.json.get("description").lower(),
                       request.json.get("_type").lower(),
                       request.json.get("category").lower(),
                       request.json.get("area").lower()
                       )
        return jsonify({"message": "Updated Successfully",
                        "data": user_request}), 200
    return jsonify({"message": "Request Not Found"}), 404


# DELETE a request
@app.route('/api/v1/users/requests/<request_id>', methods=['DELETE'])
@jwt_required
def user_delete_request(request_id):
    user_id = get_jwt_identity()
    user_request = get_user_request(request_id, user_id)
    if len(user_request) != 0:
        delete_request(request_id, user_id)
        return jsonify({"message": "Delete Successful"}), 200
    return jsonify({"message": "Request Not Found"}), 404


# Admin Priviledges


# Admin GET all requests
@app.route('/api/v1/requests')
@jwt_required
def get_requests():
    user_id = get_jwt_identity()
    user = get_user_by_id(user_id)
    print(user)
    # Check if user exists
    if len(user) != 0:
        # Check if user is admin
        if user["admin_role"] is True:
            all_requests = get_all_requests()
            # Check if requests contains data
            if len(all_requests) != 0:
                return jsonify({"requests": all_requests}), 200
            return jsonify({"message": "No requests to display"}), 404
        return jsonify({"message": "Sorry, Can't Grant You Access"}), 403
    return jsonify({"message": "Not Found. Sign up to create an account"}), 404


# Admin Approve Requests
@app.route('/api/v1/requests/<request_id>/approve', methods=['PUT'])
@jwt_required
def approve_request(request_id):
    user_id = get_jwt_identity()
    user = get_user_by_id(user_id)
    # Check if user exists
    if len(user) != 0:
        # Check if user is admin
        if user["admin_role"] is True:
            user_request = get_request(request_id)
            # Check request status
            if user_request["status"] == "pending":
                return jsonify({
                    "message": update_status(request_id, "approved")}), 200
            return jsonify({"message":
                            "The request has been {}".format(
                                user_request["status"])
                            }), 400
        return jsonify({"message": "Sorry, Can't Grant You Access"}), 403
    return jsonify({
        "message": "Not Found. Sign up to create an account"}), 404


# Admin Disapprove Requests
@app.route('/api/v1/requests/<request_id>/disapprove', methods=['PUT'])
@jwt_required
def disapprove_request(request_id):
    user_id = get_jwt_identity()
    user = get_user_by_id(user_id)
    # Check if user exists
    if len(user) != 0:
        # Check if user is admin
        if user["admin_role"] is True:
            user_request = get_request(request_id)
            # Check request status
            if user_request["status"] == "pending":
                return jsonify({
                    "message": update_status(request_id, "diapproved")}), 200
            return jsonify({"message":
                            "The request has been {}".format(
                                user_request["status"])
                            }), 400
        return jsonify({"message": "Sorry, Can't Grant You Access"}), 403
    return jsonify({
        "message": "Not Found. Sign up to create an account"}), 404


# Admin Resolve Requests
@app.route('/api/v1/requests/<request_id>/resolve', methods=['PUT'])
@jwt_required
def resolve_request(request_id):
    user_id = get_jwt_identity()
    user = get_user_by_id(user_id)
    # Check if user exists
    if len(user) != 0:
        # Check if user is admin
        if user["admin_role"] is True:
            user_request = get_request(request_id)
            # Check request status
            if user_request["status"] == "approved":
                return jsonify({
                    "message": update_status(request_id, "resolve")}), 200
            return jsonify({"message":
                            "The request has been {}".format(
                                user_request["status"])
                            }), 400
        return jsonify({"message": "Sorry, Can't Grant You Access"}), 403
    return jsonify({
        "message": "Not Found. Sign up to create an account"}), 404
