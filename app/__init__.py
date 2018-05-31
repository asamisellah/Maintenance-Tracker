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
    return jsonify({"users": users}), 201


# Sign in a user
@app.route('/api/v1/users/signin', methods=['POST'])
def signin_user():
    username = request.json.get("username")
    password = request.json.get("password")
    user = [user for user in users if user["username"] == username]
    if len(user) == 0:
        return({"message": "User Not Found"}), 404
    else:
        if user["password"] == password:
            return({"message": "User Successfully Logged in"})
        else:
            return({"message": "Wrong Username or Password"})

    # user = [user for user in users if user["username"] == userId]
    # if len(user) == 0:
    #     return jsonify({"message": "Not Found"}), 404

    # else:
    #     return jsonify({"user": user}), 200


# POST a request
@app.route('/users/requests', methods=['POST'])
def create_request():
    # "id" = request.json.get("id")
    request_data = {request.json.get("id"): {
        "title": request.json.get("title"),
        "type": request.json.get('type'),
        "description": request.json.get("description"),
        "category": request.json.get('category'),
        "area": request.json.get('area')
    }}
    requests.update(request_data)
    return jsonify({"requests": requests}), 201


# GET a request
@app.route('/users/requests/<string:requestId>')
def get_request(requestId):
    for id in requests:
        if id == requestId:
            request_data = requests[id]
    if len(request_data) == 0:
        return jsonify({"message": "Not Found"}), 404

    else:
        return jsonify({"request": request_data}), 200


# GET all requests
@app.route('/users/requests')
def get_requests():
    return jsonify({"requests": requests})


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
