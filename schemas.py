from marshmallow import Schema, fields
from models import StoreModel
from marshmallow.decorators import post_dump


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
    sname = fields.Str(required=True)
    slatitude = fields.Str(dump_only=True)
    slongitude = fields.Str(dump_only=True)
    
    @post_dump(pass_many=True)
    def add_store_coordinates(self, data, many, **kwargs):
        if many:
            store_names = [item.get("sname") for item in data]
        else:
            store_names = [data.get("sname")]

        store_names = [name for name in store_names if name is not None]  # Filter out None values

        stores = StoreModel.query.filter(StoreModel.sname.in_(store_names)).all()
        store_coordinates = {store.sname: {"slatitude": store.slatitude, "slongitude": store.slongitude} for store in stores}

        if many:
            for item in data:
                store_name = item.get("sname")
                coordinates = store_coordinates.get(store_name)
                if coordinates:
                    item.update(coordinates)
        else:
            store_name = data.get("sname")
            coordinates = store_coordinates.get(store_name)
            if coordinates:
                data.update(coordinates)

        return data

    # @post_dump(pass_many=True)
    # def add_store_coordinates(self, data, many, **kwargs):
    #     if many:
    #         store_names = [item["sname"] for item in data]
    #     else:
    #         store_names = [data["sname"]]

    #     stores = StoreModel.query.filter(StoreModel.sname.in_(store_names)).all()
    #     store_coordinates = {store.sname: {"slatitude": store.slatitude, "slongitude": store.slongitude} for store in stores}

    #     if many:
    #         for item in data:
    #             store_name = item["sname"]
    #             coordinates = store_coordinates.get(store_name)
    #             if coordinates:
    #                 item.update(coordinates)
    #     else:
    #         store_name = data["sname"]
    #         coordinates = store_coordinates.get(store_name)
    #         if coordinates:
    #             data.update(coordinates)

    #     return data


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



