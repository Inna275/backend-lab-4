from marshmallow import Schema, fields

class RecordSchema(Schema):
    id = fields.Str(dump_only=True)
    user_id = fields.Str(required=True)
    category_id = fields.Str(required=True)
    amount = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
