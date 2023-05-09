import uuid
# from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import StoreModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas import StoreSchema

from sqlalchemy import create_engine

blp = Blueprint("store", __name__, description="Operation on stores")


@blp.route("/store/<string:sname>")
class Stores(MethodView):
    # get a store
    @blp.response(200, StoreSchema)
    def get(self, sname):
        store = StoreModel.query.get_or_404(sname)
        return store

    # delete a store
    def delete(self, sname):
        store = StoreModel.query.get_or_404(sname)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted"}


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

        return Store

    @blp.response(200, StoreSchema(many=True))
    def get(self):
        # get store list all info
        return StoreModel.query.all()


# test: based on the sname return store list
# @blp.route("/store/<string:sname>")
# class Stores(MethodView):
#     @blp.response(200, StoreSchema(many=True))
#     def get(self, sname):
#         # Base on the item name to retrieve data, item name is a *unique field*
#         # not found return 404 error
#         # stores = StoreModel.query
#         stores = StoreModel.query.filter(StoreModel.sname == sname).all()
#         if not stores:
#             abort(404, message="Store not found")
#         return stores
