from flask import Flask, jsonify, request

app = Flask(__name__)


requests = []
users = []
session_requests = []
session = []
user_id = ""


# GET users
@app.route('/api/v1/users')
def get_users():
    return jsonify({"users": users})


# POST a user
@app.route('/api/v1/users', methods=['POST'])
def create_user():
    new_user = {
        "user_id": len(users)+1,
        "username": request.json.get("username", "username"),
        "email": request.json.get('email'),
        "password": request.json.get("password"),
    }
    # Confirm user input has data
    for key in new_user:
        if new_user[key] == "":
            return jsonify({"message": "All Fields Required"})
    # Confirm password
    if request.json.get("password") != request.json.get("confirm_password"):
        return jsonify({"message": "Your Passwords Don't Match"}), 400
    if len(users) == 0:
        users.append(new_user)
        return jsonify({"message": "Sign Up Successful"}), 201
    for user in users:
        if user["username"] != new_user["username"]:
            users.append(new_user)
            return jsonify({"message": "Sign Up Successful"}), 201
        return jsonify({"message": "User already exists"}), 400


# Sign in a user
@app.route('/api/v1/users/signin', methods=['POST'])
def signin_user():
    username = request.json.get("username")
    password = request.json.get("password")
    current_user = []

    for user in users:
        if user["username"] == username:
            current_user.append(user)
    if len(current_user) != 0:
        if current_user[0]["password"] == password:
            # Create user session
            user_id = current_user[0]["username"]
            session.append(user_id)
            print(session)
            return jsonify({"message": "Sign in Successful!"}), 202
        else:
            return jsonify({"message": "Wrong username or password"}), 401
    return jsonify({"message": "User Not Found"}), 404


# POST a request
@app.route('/api/v1/users/requests', methods=['POST'])
def create_request():
    for user in session:
        if user == user_id:
            print(session)
            request_data = {
                "id": len(requests)+1,
                "user_id": user_id,
                "title": request.json.get("title"),
                "type": request.json.get('type'),
                "description": request.json.get("description"),
                "category": request.json.get('category'),
                "area": request.json.get('area')
            }
            requests.append(request_data)
            return jsonify({"message": "Request Created Successfully!"}), 201
        return jsonify({"message": "Sign In to view requests"})


# GET all requests
@app.route('/api/v1/users/requests')
def get_requests():
    if len(session) == 0:
        return jsonify({"message": "Sign in to view requests"}), 403
    for user in session:
        if user == user_id:
            for request in requests:
                if request["user_id"] == user_id:
                    session_requests.append(request)
            print(session_requests)
            if len(session_requests) == 0:
                return jsonify({"message": "No requests to display "})
            return jsonify({"requests": session_requests})
        return jsonify({"message": "Sign In to view requests"}), 403


# GET a request
@app.route('/api/v1/users/requests/<int:request_id>')
def get_request(request_id):
    user_id = session["user_id"]
    if user_id in session["user_id"]:
        current_request = []
        for request in session_requests:
            if request["id"] == request_id:
                current_request.append(request)
        if len(current_request) != 0:
            return jsonify({"request": current_request[0]}), 200
        return jsonify({"message": "Request not found"}), 404
    return jsonify({"message": "Sign In to view requests"})


# UPDATE(PUT) a request
@app.route('/api/v1/users/requests/<int:request_id>', methods=['PUT'])
def update_request(request_id):
    user_id = session["user_id"]
    if user_id in session["user_id"]:
        request_data = []
        for user_request in requests:
            if user_request["id"] == request_id:
                request_data.append(user_request)

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

            return jsonify({"requests": requests}), 200
        return jsonify({"message": "Not Found"})
    return jsonify({"message": "Sign In to view requests"})


# DELETE a request
@app.route('/api/v1/users/requests/<int:request_id>', methods=['DELETE'])
def delete_request(request_id):
    user_id = session["user_id"]
    if user_id in session["user_id"]:
        print(request_id)
        request_data = [
            request for request in requests if request["id"] == request_id]
        print(request_data)
        if len(request_data) != 0:
            requests.remove(request_data[0])
            return jsonify({"message": "Successfully deleted"}), 204
        return jsonify({"message": "Not Found"}), 404
    return jsonify({"message": "Sign In to view requests"})
