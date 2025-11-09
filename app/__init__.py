import os
import time

from flask import Flask, jsonify
from flask_migrate import Migrate, init, stamp, migrate as fmigrate, upgrade
from flask_jwt_extended import JWTManager

from .models import db

from .routes.general import general_bp
from .routes.users import users_bp
from .routes.categories import categories_bp
from .routes.records import records_bp
from .routes.currencies import currencies_bp


app = Flask(__name__)

app.config.from_pyfile('config.py', silent=True)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

db.init_app(app)

migrate = Migrate()
migrate.init_app(app, db)

jwt = JWTManager(app)

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        "message": "The token has expired.", 
        "error": "token_expired"
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        "message": "Signature verification failed.", 
        "error": "invalid_token"
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": "Request does not contain an access token.",
        "error": "authorization_required",
    }), 401

app.register_blueprint(general_bp)
app.register_blueprint(users_bp)
app.register_blueprint(categories_bp)
app.register_blueprint(records_bp)
app.register_blueprint(currencies_bp)

time.sleep(5)

with app.app_context():
    if not os.path.exists('migrations'):
        init()
        stamp()
        fmigrate(message="Initial migration")
        upgrade()
