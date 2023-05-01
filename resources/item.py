import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import ItemModel
from db import db

from sqlalchemy.exc import SQLAlchemyError
from schemas1 import ItemSchema, ItemUpdateSchema

blp = Blueprint("item", __name__, description="Operation on items")


@blp.route("/item/<string:item_id>")
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
