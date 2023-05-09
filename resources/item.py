import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import ItemModel, UploadModel
from db import db
from sqlalchemy import select
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError
from schemas1 import ItemSchema, ItemUpdateSchema, PlainUploadSchema

blp = Blueprint("item", __name__, description="Operation on items")


@blp.route("/item/<int:item_id>")
class item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        # Base on the item id to retrive data, item id is a *primary key*
        # not found return 404 error
        item = ItemModel.query.get_or_404(item_id)
        return item
    # delete an item

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted"}

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    # update an item, item_data from input
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            # what if the item does not exist?
            # if exist, update; if not create it
            item.price = item_data["price"]
        else:
            # item = ItemModel(**item_data)
            item = ItemModel(vid=item_id, **item_data)

            # ; not working, set the

        db.session.add(item)
        db.session.commit()


@blp.route("/item")
class itemlist(MethodView):

    # create a new item
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    # item_dara is in json value validated by itemschema
    def post(self, item_data):
        # turn dict into key word arguments, not put into database yet
        item = ItemModel(**item_data)
        try:
            # not in db yet
            db.session.add(item)
            # in the db
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting a item")

        return item
    # many = True -> return an item list

    @blp.response(200, ItemSchema(many=True))
    # get item list
    def get(self):
        return ItemModel.query.all()


# test get item name return value
# @blp.route("/item/<string:vname>")
# class itemView(MethodView):
#     @blp.response(200, ItemSchema(many=True))
#     def get(self, vname):
#         # Base on the item name to retrieve data, item name is a *unique field*
#         # not found; return 404 error
#         item = ItemModel.query.filter(ItemModel.vname == vname).all()
#         if item:
#             return item
#         else:
#             abort(404, message="Veggies not found")
        # item = ItemModel.query.get(vname)


# working ⬆️
# update price test ⬇️
    # # upload veggies
    # @blp.arguments(ItemUpdateSchema)
    # @blp.response(200, ItemSchema)
    # # update an item, item_data from input
    # def put(self, item_data, vname):
    #     # item = ItemModel.query.filter(
    #     #     ItemModel.vname == vname and ItemModel.sname == item_data["sname"]).update({"price": item_data["price"]})
    #     item = ItemModel.query.filter(
    #         ItemModel.vname == vname and ItemModel.sname == item_data["sname"])

    #     return item


@blp.route("/item/<string:vname>")
class itemStore(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self, vname):
        # Base on the item name to retrieve data, item name is a *unique field*
        # not found; return 404 error
        item = ItemModel.query.filter(ItemModel.vname == vname).all()
        if item:
            return item
        else:
            abort(404, message="Veggies not found")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    # update an item, item_data from input
    def put(self, item_data, vname):
        # Find the item based on vname and sname
        item = ItemModel.query.filter_by(
            vname=vname, sname=item_data["sname"]).first()

        if item:
            # Check if the input price is different from the price in the database
            if item_data["price"] != item.price:
                # Update the item's price and updatetime
                item.price = item_data["price"]
                item.updateTime = datetime.now()  # Update with the current timestamp
                db.session.commit()

                return {"message": "Item price has been updated", "item": item}
            else:
                return {"message": "Item price is already up to date", "item": item}
        else:
            abort(404, message="Veggies not found")


@blp.route("/item/<string:vname>/<string:sname>")
class itemStore(MethodView):
    @blp.response(200, ItemSchema)
    # update an item, item_data from input
    def get(self, vname, sname):
        items = ItemModel.query.filter(
            ItemModel.vname == vname, ItemModel.sname == sname).all()
        # for item in items:
        #     if item.sname == item_data["sname"]:
        #         item.price = item_data["price"]
        #     else:
        #         pass

        return items


# @blp.route("/item/update")
# class item(MethodView):
#     @blp.arguments(ItemUpdateSchema)
#     @blp.response(200, ItemSchema)
#     # update an item, item_data from input
#     def put(self,vname,sname):
#         # get from upload table
#         upload
        # get from item table
        # compare
        # update

    # def put(self, item_data, item_id):
    #     item = ItemModel.query.get(item_id)
    #     if item:
    #         # what if the item does not exist?
    #         # if exist, update; if not create it
    #         item.price = item_data["price"]
    #     else:
    #         # item = ItemModel(**item_data)
    #         item = ItemModel(vid=item_id, **item_data)
    #         # ; not working, set the

    #     db.session.add(item)
    #     db.session.commit()
