import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import StoreModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas1 import StoreSchema

blp = Blueprint("store", __name__, description="Operation on stores")


@blp.route("/store/<string:store_id>")
class Stores(MethodView):
    # get a store
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store
    # delete a store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        raise NotImplementedError("Deleting a store is not implemented")


@blp.route("/store")
class StoreList(MethodView):
    # create a store
    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        Store = StoreModel(**store_data)
        try:
            # not in db yet
            db.session.add(Store)
            # in the db
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with that name already exists")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting a item")

        return Store

    @blp.response(200, StoreSchema(many=True))
    def get(self):
        # get store list all info
        return stores.values()
