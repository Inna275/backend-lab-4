from flask import Flask
from flask_migrate import Migrate

from .models import db

from .routes.general import general_bp
from .routes.users import users_bp
from .routes.categories import categories_bp
from .routes.records import records_bp
from .routes.currencies import currencies_bp


app = Flask(__name__)

app.config.from_pyfile('config.py', silent=True)

db.init_app(app)

migrate = Migrate(app, db)
migrate.init_app(app, db)

app.register_blueprint(general_bp)
app.register_blueprint(users_bp)
app.register_blueprint(categories_bp)
app.register_blueprint(records_bp)
app.register_blueprint(currencies_bp)
