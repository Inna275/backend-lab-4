from app import app
from flask import request, jsonify
from app.data import categories
from app.schemas.category_schema import CategorySchema
from marshmallow import ValidationError
import uuid


@app.post("/category")
def create_category():
    schema = CategorySchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    category_id = uuid.uuid4().hex
    category = {
        "id": category_id,
        "name": data["name"]
    }
    categories[category_id] = category
    return jsonify(schema.dump(category)), 201


@app.get("/category")
def get_categories():
    schema = CategorySchema(many=True)
    return jsonify(schema.dump(list(categories.values()))), 200


@app.delete("/category")
def delete_category():
    category_id = request.args.get("id")

    if not category_id:
        return jsonify({"error": "Category ID is required"}), 400
        
    if category_id not in categories:
        return jsonify({"error": "Category not found"}), 404

    categories.pop(category_id)
    return jsonify({"message": "Category deleted"}), 200
