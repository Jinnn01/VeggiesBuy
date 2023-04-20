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
        # Base on the item id to retrive data, item id is a primary key
        item = ItemModel.query.get_or_404(item_id)
        return item
    # delete an item

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        raise NotImplementedError("Deleting an item is not implemented")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    # update an item
    def put(self, item_data, item_id):
        item = ItemModel.query.get_or_404(item_id)
        raise NotImplementedError("Deleting an item is not implemented")


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

    @blp.response(200, ItemSchema(many=True))
    # get item list
    def get(self):
        return items.values()
