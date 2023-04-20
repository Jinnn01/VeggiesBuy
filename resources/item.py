import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("item", __name__, description="Operation on items")


@blp.route("/item/<string:item_id>")
class item(MethodView):

    @blp.response(200, ItemSchema)
    # get an item
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found")

    # delete an item
    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted."}
        except KeyError:
            abort(404, message="Item not found.")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    # update an item
    def put(self, item_new_data, item_id):
        item_new_data = request.get_json(force=True)

        try:
            item = items[item_id]
            # in place, means update data in pairs
            item["price"] = item_new_data["price"]
            item["name"] = item_new_data["name"]
            return item, 201
        except KeyError:
            abort(404, message="Item not found.")


@blp.route("/item")
class itemlist(MethodView):
    @blp.response(200, ItemSchema(many=True))
    # get item list
    def get(self):
        return items.values()

    # create a new item
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    # item_dara is in json value validated by itemschema
    def post(self, item_data):
        item_data = request.get_json(force=True)
        # validate the data to ensure, the item can be added twice
        for item in items.values():
            if (item_data["name"] == item["name"] and item_data["sid"] == item["sid"]):
                abort(400, message="Item already exists.")

        item_id = uuid.uuid4().hex
        item = {**item_data, "vid": item_id}
        items[item_id] = item

        return item
