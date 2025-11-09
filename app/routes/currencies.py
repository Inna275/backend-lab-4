from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required

from app.models import db
from app.models.currency import CurrencyModel
from app.schemas.currency_schema import CurrencySchema


currencies_bp = Blueprint("currencies", __name__)


@currencies_bp.post("/currency")
@jwt_required()
def create_currency():
    schema = CurrencySchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    currency = CurrencyModel(code=data["code"])
    db.session.add(currency)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Resource conflict"}), 409

    return jsonify(schema.dump(currency)), 201


@currencies_bp.get("/currencies")
def get_currencies():
    schema = CurrencySchema(many=True)
    currencies = CurrencyModel.query.all()
    return jsonify(schema.dump(currencies)), 200


@currencies_bp.get("/currency/<int:currency_id>")
def get_currency(currency_id):
    currency = CurrencyModel.query.get(currency_id)
    if not currency:
        return jsonify({"error": "Currency not found"}), 404
    schema = CurrencySchema()
    return jsonify(schema.dump(currency)), 200


@currencies_bp.delete("/currency/<int:currency_id>")
@jwt_required()
def delete_currency(currency_id):
    currency = CurrencyModel.query.get(currency_id)
    if not currency:
        return jsonify({"error": "Currency not found"}), 404
    
    try:
        db.session.delete(currency)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Currency is used"}), 400

    return jsonify({"message": "Currency deleted"}), 200
