from flask import Flask, jsonify, request

app = Flask(__name__)


requests = []

users = []


# POST a user
@app.route('/api/v1/users', methods=['POST'])
def create_user():
    user = {
        "username": request.json.get("username"),
        "email": request.json.get('email'),
        "password": request.json.get("password"),
        "confirm_password": request.json.get('confirm_password')
    }
    users.append(user)
    return jsonify({"message": "Sign up successful!"}), 201


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
            return jsonify({"message": "Sign in Successful!"}), 202
        else:
            return jsonify({"message": "Wrong username or password"}), 401
    else:
        return jsonify({"message": "username does not exist"}), 404


# POST a request
@app.route('/api/v1/users/requests', methods=['POST'])
def create_request():
    request_data = {
        "id": len(requests)+1,
        "title": request.json.get("title"),
        "type": request.json.get('type'),
        "description": request.json.get("description"),
        "category": request.json.get('category'),
        "area": request.json.get('area')
    }
    requests.append(request_data)
    return jsonify({"message": "Request Created Successfully!"}), 201


# GET all requests
@app.route('/api/v1/users/requests')
def get_requests():
    return jsonify({"requests": requests})


# GET a request
@app.route('/api/v1/users/requests/<int:requestId>')
def get_request(requestId):
    request = [request for request in requests if request["id"] == requestId]
    if len(request) != 0:
        return jsonify({"request": request[0]})
    return({"message": "Request Not Found"})


# UPDATE(PUT) a request
@app.route('/users/requests/<int:requestId>', methods=['PUT'])
def modify_request(requestId):
    for id in requests:
        if id == requestId:
            request_data = requests[id]

    # if len(request_data) == 0:
    #     return jsonify({"message": "Not Found"})

    else:
        request_data = {
            "title": request.json.get("title"),
            "type": request.json.get('type'),
            "description": request.json.get("description"),
            "category": request.json.get('category'),
            "area": request.json.get('area')
        }
        return jsonify({"request": request_data}), 201


# DELETE a request
@app.route('/users/requests/<string:requestId>', methods=['DELETE'])
def delete_request(requestId):
    for id in requests:
        if id == requestId:
            request_data = requests[id]
    # print(request[0])
    requests.pop(request_data)
    return jsonify({"request": requests}), 204
