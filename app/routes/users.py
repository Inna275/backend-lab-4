from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from app.models import db
from app.models.user import UserModel
from app.models.currency import CurrencyModel
from app.schemas.user_schema import UserSchema


users_bp = Blueprint("users", __name__)


@users_bp.post("/register")
def register():
    schema = UserSchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    if "default_currency_id" in data:
        currency_id = data["default_currency_id"]
    else:
        default_currency = CurrencyModel.query.filter_by(code="UAH").first()
        if not default_currency:
            default_currency = CurrencyModel(code="UAH")
            db.session.add(default_currency)
            db.session.commit()
        currency_id = default_currency.id

    user = UserModel(
        name=data["name"],
        password=pbkdf2_sha256.hash(data["password"]),
        default_currency_id=currency_id,
    )
    db.session.add(user)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Resource conflict"}), 409

    return jsonify(schema.dump(user)), 201


@users_bp.post("/login")
def login():
    schema = UserSchema(only=("name", "password"))
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    user = UserModel.query.filter_by(name=data["name"]).first()

    if not user or not pbkdf2_sha256.verify(data["password"], user.password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": access_token}), 200


@users_bp.get("/users")
def get_users():
    schema = UserSchema(many=True)
    users = UserModel.query.all()
    return jsonify(schema.dump(users)), 200


@users_bp.get("/user/<int:user_id>")
def get_user(user_id):
    user = UserModel.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    schema = UserSchema()
    return jsonify(schema.dump(user)), 200


@users_bp.delete("/user/<int:user_id>")
@jwt_required()
def delete_user(user_id):
    current_user_id = int(get_jwt_identity())
    if current_user_id != user_id:
        return jsonify({"error": "You can delete only your own account"}), 403

    user = UserModel.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200
