from flask import Flask, jsonify, request

app = Flask(__name__)


requests = {}

users = {}


# POST a user
@app.route('/users', methods=['POST'])
def create_user():
    user = {
        "username": request.json.get("username"),
        "email": request.json.get('email'),
        "password": request.json.get("password"),
        "cconfirm_password": request.json.get('cconfirm_password'),
    }
    users.update(user)
    return jsonify({"users": users}), 201


# GET a user
@app.route('/users/<string:userId>')
def get_user(userId):
    user = [user for user in users if user["id"] == userId]
    if len(user) == 0:
        return jsonify({"message": "Not Found"}), 404

    else:
        return jsonify({"user": user}), 200


# POST a request
@app.route('/users/requests', methods=['POST'])
def create_request():
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
    # for id in requests:
    #     if id == requestId:
    #         request_data = requests[id]
    request_data = requests[requestId]

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
