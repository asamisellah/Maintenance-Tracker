from flask import Flask, jsonify, request, render_template
from psycopg2.extras import RealDictCursor
from flask_cors import CORS
from .model import *
import os
import re
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from config import config

app = Flask(__name__)
RUN_MODE = os.getenv('APP_SETTINGS') if os.getenv(
    'APP_SETTINGS') else 'development'
app.config.from_object(config[RUN_MODE])
jwt = JWTManager(app)
db.init_app(app)
CORS(app)


@app.route("/")
def index():
    return render_template("index.html")
# POST a user


@app.route('/api/v1/auth/signup', methods=['POST'])
def create_user():
    try:
        # Ensure input is in json format
        if not request.is_json:
            return jsonify({"message": "Missing JSON in request"}), 400
        for key in request.json:
            # Ensure key is valid
            if key is None:
                return jsonify({"message": "Invalid"}), 400
            # Ensure input contains data
            elif request.json[key] == "":
                return jsonify({"message": "All Fields Required"}), 400
            # Ensure input data is a string
            elif type(request.json[key]) != str:
                return jsonify({"message": "Input Must be a String"}), 400
            # Ensure string is not whitespace
            elif request.json[key].strip() == "":
                print(request.json[key])
                return jsonify({"message": "Input Must be Valid Data"}), 400
        match = re.search(r'\w+@\w+', request.json.get("email"))
        if match is None:
            return jsonify({"message": "Invalid email address"}), 400
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
    except:
        return jsonify({"message": "Not allowed"})


# Sign in a user
@app.route('/api/v1/auth/login', methods=['POST'])
def signin_user():
    # Ensure input is in json format
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400
    for key in request.json:
        # Ensure key is not empty
        if key == "":
            return jsonify({"message": "Invalid format"}), 400
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
    return jsonify({"message":
                    "User Not Found. Create an Account to Sign In"}), 404


# POST a request
@app.route('/api/v1/users/requests', methods=['POST'])
@jwt_required
def create_request():
    # pass user_id from token
    user_id = get_jwt_identity()
    # Ensure input is in json format
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400
    for key in request.json:
        # Ensure key is not empty
        if key == "":
            return jsonify({"message": "Invalid format"}), 400
        # Ensure input contains data
        elif request.json[key] == "":
            return jsonify({"message": "All Fields Required"}), 400
        # Ensure input data is a string
        elif type(request.json[key]) != str:
            return jsonify({"message": "Input Must be a String"}), 400
        # Ensure string is not whitespace
        elif request.json[key].strip() == "":
            print(request.json[key])
            return jsonify({"message": "Input Must be Valid Data"}), 400

    # create new request
    request_data = UserRequest(
        user_id,
        request.json.get("title").lower(),
        request.json.get("description").lower(),
        request.json.get("_type").lower(),
        request.json.get("category").lower(),
        request.json.get("area").lower()
    )

    if request_data is not None:
        new_request = request_data.create_request()
        return jsonify({"message": "Request Created Successfully",
                        "data": new_request}), 201
    return jsonify({"message": "Invalid input"}), 400


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
        return jsonify({"message": "Missing JSON in request"}), 400
    for key in request.json:
        # Ensure key is not empty
        if key == "":
            return jsonify({"message": "Invalid format"}), 400
        # Ensure input contains data
        if request.json[key] == "":
            return jsonify({"message": "All Fields Required"}), 400
        # Ensure input data is a string
        elif type(request.json[key]) != str:
            return jsonify({"message": "Input Must be a String"}), 400
        # Ensure string is not whitespace
        elif request.json[key].strip() == "":
            print(request.json[key])
            return jsonify({"message": "Input Must be Valid Data"}), 400

    # Ensure request has been fetched
    if user_request is not None:
        if user_request["status"] == "pending":
            update_request(request_id,
                           user_id,
                           request.json.get("title").lower(),
                           request.json.get("description").lower(),
                           request.json.get("_type").lower(),
                           request.json.get("category").lower(),
                           request.json.get("area").lower()
                           )
            return jsonify({"message": "Request Updated Successfully",
                            "data": user_request}), 200
        return jsonify({"message":
                        "Cannot Update, Your Request is Already {}".
                        format(user_request["status"])}), 400
    return jsonify({"message": "Request Not Found"}), 404


# DELETE a request
@app.route('/api/v1/users/requests/<request_id>', methods=['DELETE'])
@jwt_required
def user_delete_request(request_id):
    user_id = get_jwt_identity()
    user_request = get_user_request(request_id, user_id)
    print(user_request)
    if user_request is not None:
        delete_request(request_id, user_id)
        return jsonify({"message": "Request Deleted Successfully"}), 200
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
        return jsonify({"message": "Sorry, Only Admin can Access"}), 403
    return jsonify({"message": "User Not Found. Sign up to create an account"}), 404


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
                    "message": "Request Successfully {}".
                    format(update_status(request_id, "approved"))}), 200
            return jsonify({"message":
                            "Failed, The request has been {}".format(
                                user_request["status"])
                            }), 400
        return jsonify({"message": "Sorry, Only Admin can Access"}), 403
    return jsonify({
        "message": "User Not Found. Sign up to create an account"}), 404


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
        return jsonify({"message": "Sorry, Only Admin can Access"}), 403
    return jsonify({
        "message": "User Not Found. Sign up to create an account"}), 404


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
                    "message": update_status(request_id, "resolved")}), 200
            return jsonify({"message":
                            "The request has been {}".format(
                                user_request["status"])
                            }), 400
        return jsonify({"message": "Sorry, Can't Grant You Access"}), 403
    return jsonify({
        "message": "User Not Found. Sign up to create an account"}), 404
