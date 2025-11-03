from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import UserModel
from .category import CategoryModel
from .record import RecordModel
from .currency import CurrencyModel
