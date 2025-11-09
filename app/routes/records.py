from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models import db
from app.models.user import UserModel
from app.models.record import RecordModel
from app.schemas.record_schema import RecordSchema


records_bp = Blueprint("records", __name__)


@records_bp.post("/record")
@jwt_required()
def create_record():
    schema = RecordSchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    current_user_id = int(get_jwt_identity())
    if data["user_id"] != current_user_id:
        return jsonify({"error": "Cannot create record for another user"}), 403

    user = UserModel.query.get(data["user_id"])
    if not user:
        return jsonify({"error": "User not found"}), 404

    currency_id = data.get("currency_id") or user.default_currency_id

    record = RecordModel(
        user_id=data["user_id"],
        category_id=data["category_id"],
        currency_id=currency_id,
        amount=data["amount"],
    )
    db.session.add(record)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Related resource not found"}), 400

    return jsonify(schema.dump(record)), 201


@records_bp.get("/record/<int:record_id>")
@jwt_required()
def get_record(record_id):
    record = RecordModel.query.get(record_id)
    if not record:
        return jsonify({"error": "Record not found"}), 404
    schema = RecordSchema()
    return jsonify(schema.dump(record)), 200


@records_bp.get("/record")
@jwt_required()
def get_records():
    user_id = request.args.get("user_id", type=int)
    category_id = request.args.get("category_id", type=int)

    if not user_id and not category_id:
        return jsonify({"error": "Provide user_id or category_id"}), 400

    query = RecordModel.query
    if user_id:
        query = query.filter_by(user_id=user_id)
    if category_id:
        query = query.filter_by(category_id=category_id)

    records = query.all()
    schema = RecordSchema(many=True)
    return jsonify(schema.dump(records)), 200


@records_bp.delete("/record/<int:record_id>")
@jwt_required()
def delete_record(record_id):
    current_user_id = int(get_jwt_identity())
    
    record = RecordModel.query.get(record_id)
    if not record:
        return jsonify({"error": "Record not found"}), 404

    if record.user_id != current_user_id:
        return jsonify({"error": "Cannot delete record of another user"}), 403
    
    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "Record deleted"}), 200
