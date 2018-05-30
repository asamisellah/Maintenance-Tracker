from flask import Flask, jsonify, request

app = Flask(__name__)


requests = [{}]

users = [{}]


# POST a user that belongs to logged in user
@app.route('/users', methods=['POST'])
def create_user():
    user = {
        "username": request.json.get("username"),
        "email": request.json.get('email'),
        "password": request.json.get("password"),
        "cconfirm_password": request.json.get('cconfirm_password'),
    }
    users.append(user)
    return jsonify({"users": users}), 201


# GET a user
@app.route('/users/<string:userId>')
def get_user(userId):
    user = [user for user in users if user["id"] == userId]
    if len(user) == 0:
        return jsonify({"message": "Not Found"}), 404

    else:
        return jsonify({"user": user})


# GET all requests that belong to a logged in user
@app.route('/requests')
def get_requests():
    return jsonify({"request": requests})


# GET a request that belong to a logged in user
@app.route('/users/requests/<string:requestId>')
def get_request(requestId):
    request = [request for request in requests if request["id"] == requestId]
    if len(request) == 0:
        return jsonify({"message": "Not Found"}), 404

    else:
        return jsonify({"request": request})


# GET a request that belongs to a logged in user
@app.route('/users/requests/<string:requestId>')
def get_request(requestId):
    request = [request for request in requests if request["id"] == requestId]
    if len(request) == 0:
        return jsonify({"message": "Not Found"}), 404

    else:
        return jsonify({"request": request})


# POST a request that belongs to logged in user
@app.route('/users/requests', methods=['POST'])
def create_request():
    request_data = {
        "title": request.json.get("title"),
        "type": request.json.get('type'),
        "description": request.json.get("description"),
        "category": request.json.get('category'),
    }
    requests.append(request)
    return jsonify({"requests": requests}), 201


# UPDATE(PUT) a request that belongs to logged in user
@app.route('/users/requests/<string:requestId>', methods=['PUT'])
def modify_request(requestId):
    request = [request for request in requests if requests["id"] == requestId]
    if len(request) == 0:
        return jsonify({"message": "Not Found"})
    else:
        request = {
            "title": request.json.get("title"),
            "type": request.json.get('type'),
            "description": request.json.get("description"),
            "category": request.json.get('category'),
            "area": request.json.get('area')
        }
        
        requests.append(request)
        return jsonify({"request": request}), 201


# DELETE a request made by a logged in user
@app.route('/users/requests/<string:requestId>', methods=['DELETE'])
def delete_request(requestId):
    request = [request for request in requests if request["id"] == requestId]
    print(request[0])
    requests.remove(request[0])
    return jsonify({"request": requests}), 204