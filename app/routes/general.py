from app import app
from flask import jsonify
from datetime import datetime


@app.route("/")
def greeting():
    return jsonify({
        "message": "Hello!"
    }), 200


@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    return jsonify({
        "status": "ok", 
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }), 200
    