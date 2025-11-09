from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required

from app.models import db
from app.models.category import CategoryModel
from app.schemas.category_schema import CategorySchema


categories_bp = Blueprint("categories", __name__)


@categories_bp.post("/category")
@jwt_required()
def create_category():
    schema = CategorySchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    category = CategoryModel(name=data["name"])
    db.session.add(category)
    
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Resource conflict"}), 409

    return jsonify(schema.dump(category)), 201


@categories_bp.get("/category")
def get_categories():
    schema = CategorySchema(many=True)
    categories = CategoryModel.query.all()
    return jsonify(schema.dump(categories)), 200


@categories_bp.delete("/category")
@jwt_required()
def delete_category():
    category_id = request.args.get("id")
    if not category_id:
        return jsonify({"error": "Category ID is required"}), 400
        
    category = CategoryModel.query.get(category_id)
    if not category:
        return jsonify({"error": "Category not found"}), 404

    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category deleted"}), 200
