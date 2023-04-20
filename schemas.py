from marshmallow import Schema, fields


class PlainItemSchema(Schema):
    # user can not access the item id
    vid = fields.Int(dump_only=True)
    # we need data from user by JSON file, those data will be validated
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    # sid = fields.Str(required=True)


class PlainStoreSchema(Schema):
    sid = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class ItemUpdateSchema(Schema):
    # only price and name
    price = fields.Float()
    name = fields.Str()


class ItemSchema(PlainItemSchema):
    # pass store id when we are receiving data from the client
    sid = fields.Int(required=True, load_only=True)
    # dump_only = True, only give data to client, not receive data from client
    store = fields.Nested(PlainStoreSchema(), dump_only=True)


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
