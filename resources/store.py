import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores
from schemas import StoreSchema

blp = Blueprint("store", __name__, description="Operation on stores")


@blp.route("/store/<string:store_id>")
class Stores(MethodView):
    # get a store
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found")

    # delete a store
    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "store deleted"}
        except KeyError:
            abort(404, message="Store not found.")


@blp.route("/store")
class StoreList(MethodView):
    # create a store
    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        # get data from user input: input a new store
        # store_data = request.get_json()

        # name must be provided
        # if "name" not in store_data:
        #     abort(
        #         400,
        #         message="Bad request. Ensure 'name' is included in the JSON payload."
        #     )
        # check store already exist or not
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message="Store already exists")
        # set store a unique id
        store_id = uuid.uuid4().hex
        # stores = { sid: new_store }
        new_store = {**store_data, "sid": store_id}
        # add new store to existing stores list
        stores[store_id] = new_store
        # 201, i acept the data and create a store
        return new_store

    @blp.response(200, StoreSchema(many=True))
    def get(self):
        # get store list all info
        return stores.values()
