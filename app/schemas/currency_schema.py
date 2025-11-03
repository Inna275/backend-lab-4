from marshmallow import Schema, fields, validate

class CurrencySchema(Schema):
    id = fields.Int(dump_only=True)
    code = fields.Str(required=True, validate=validate.Length(equal=3))
