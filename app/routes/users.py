from app import app
from flask import request, jsonify
from app.data import users
from app.schemas.user_schema import UserSchema
from marshmallow import ValidationError
import uuid


@app.post("/user")
def create_user():
    schema = UserSchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    user_id = uuid.uuid4().hex
    user = {
        "id": user_id,
        "name": data["name"]
    }
    users[user_id] = user
    return jsonify(schema.dump(user)), 201


@app.get("/users")
def get_users():
    schema = UserSchema(many=True)
    return jsonify(schema.dump(list(users.values()))), 200


@app.get("/user/<user_id>")
def get_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    schema = UserSchema()
    return jsonify(schema.dump(user)), 200


@app.delete("/user/<user_id>")
def delete_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    users.pop(user_id)
    return jsonify({"message": "User deleted"}), 200
