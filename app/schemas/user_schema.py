from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    password = fields.Str(load_only=True, required=True)
    default_currency_id = fields.Int(required=False)
