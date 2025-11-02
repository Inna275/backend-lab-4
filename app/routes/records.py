from app import app
from flask import request, jsonify
from app.data import records
from datetime import datetime
from app.schemas.record_schema import RecordSchema
from marshmallow import ValidationError
import uuid


@app.post("/record")
def create_record():
    schema = RecordSchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    record_id = uuid.uuid4().hex
    record = {
        "id": record_id,
        "user_id": data["user_id"],
        "category_id": data["category_id"],
        "amount": data["amount"],
        "created_at": datetime.utcnow()
    }
    records[record_id] = record
    return jsonify(schema.dump(record)), 201


@app.get("/record/<record_id>")
def get_record(record_id):
    record = records.get(record_id)
    if not record:
        return jsonify({"error": "Record not found"}), 404
    schema = RecordSchema()
    return jsonify(schema.dump(record)), 200


@app.get("/record")
def get_records():
    user_id = request.args.get("user_id")
    category_id = request.args.get("category_id")

    if not user_id and not category_id:
        return jsonify({"error": "Provide user_id or category_id"}), 400

    filtered = []
    for r in records.values():
        if user_id and category_id:
            if r["user_id"] == user_id and r["category_id"] == category_id:
                filtered.append(r)
        elif user_id and r["user_id"] == user_id:
            filtered.append(r)
        elif category_id and r["category_id"] == category_id:
            filtered.append(r)

    schema = RecordSchema(many=True)
    return jsonify(schema.dump(filtered)), 200


@app.delete("/record/<record_id>")
def delete_record(record_id):
    if record_id not in records:
        return jsonify({"error": "Record not found"}), 404
    records.pop(record_id)
    return jsonify({"message": "Record deleted"}), 200
