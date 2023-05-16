from marshmallow import Schema, fields


class PlainItemSchema(Schema):
    # user can not access the item id
    vid = fields.Int(dump_only=True)
    # we need data from user by JSON file, those data will be validated
    vname = fields.Str(required=True)
    # vdescr = fields.Str()
    price = fields.Float(required=True)
    sname = fields.Str(required=True)
    unit = fields.Str()


class PlainStoreSchema(Schema):
    sid = fields.Int(dump_only=True)
    sname = fields.Str(required=True)
    saddress = fields.Str()
    slatitude = fields.Str()
    slongitude = fields.Str()


class ItemSchema(PlainItemSchema):
    # pass store id when we are receiving data from the client
    # sid = fields.Int(required=True, load_only=True)
    sname = fields.Str(required=True)
    # dump_only = True, only give data to client, not receive data from client
    # store = fields.Nested(PlainStoreSchema(), dump_only=True)
    store = fields.List(fields.Nested(PlainStoreSchema()), dump_only=True)


class ItemUpdateSchema(Schema):
    # only price and name
    price = fields.Float(required=True)
    vname = fields.Str(required=True)
    sname = fields.Str(required=True)
    unit = fields.Str()
    updateTime = fields.DateTime()
    updateTime = fields.DateTime(dump_only=True)


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)


# Upload & User schema


class UserSchema(Schema):
    # user can not access the item id
    uid = fields.Int(dump_only=True)
    # we need data from user by JSON file, those data will be validated
    uname = fields.Str(required=True)
    email = fields.Email(required=True)


# class PlainUploadSchema(Schema):
#     uploadid = fields.Int(dump_only=True)
#     uid = fields.Int()
#     vname = fields.Str(required=True)
#     vprice = fields.Str(required=True)
#     sname = fields.Str(required=True)
#     insertTime = fields.DateTime()
#     insertTime = fields.DateTime(dump_only=True)
