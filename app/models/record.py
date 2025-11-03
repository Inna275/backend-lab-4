from . import db
from sqlalchemy.sql import func

class RecordModel(db.Model):
    __tablename__ = "records"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, 
        db.ForeignKey("users.id"), 
        unique=False, 
        nullable=False,
    )
    category_id = db.Column(
        db.Integer, 
        db.ForeignKey("categories.id"), 
        unique=False, 
        nullable=False,
    )
    currency_id = db.Column(
        db.Integer, 
        db.ForeignKey("currencies.id", ondelete="RESTRICT"), 
        nullable=False, 
    )
    amount = db.Column(db.Float(precision=2), unique=False, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=func.now())

    user = db.relationship("UserModel", back_populates="records")
    category = db.relationship("CategoryModel", back_populates="records")
    currency = db.relationship("CurrencyModel", foreign_keys=[currency_id])
