from marshmallow import Schema, fields


class ItemSchema(Schema):
    # user can not access the item id
    vid = fields.Str(dump_only=True)

    # we need data from user by JSON file, those data will be validated
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    sid = fields.Str(required=True)


class ItemUpdateSchema(Schema):
    # only price and name
    price = fields.Float()
    name = fields.Str()


class StoreSchema(Schema):
    sid = fields.Str(dump_only=True)
    name = fields.Str(required=True)
