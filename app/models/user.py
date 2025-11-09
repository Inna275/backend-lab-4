from . import db

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    default_currency_id = db.Column(
        db.Integer, 
        db.ForeignKey("currencies.id", ondelete="RESTRICT"), 
        nullable=False,
    )

    records = db.relationship(
        "RecordModel", 
        back_populates="user", 
        lazy="dynamic", 
        cascade="all, delete-orphan",
    )
    
    default_currency = db.relationship("CurrencyModel", foreign_keys=[default_currency_id])
