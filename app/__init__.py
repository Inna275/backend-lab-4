import os
import time

from flask import Flask
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

JWTManager(app)

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
