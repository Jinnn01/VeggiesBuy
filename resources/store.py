import uuid
# from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import StoreModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas1 import StoreSchema

blp = Blueprint("store", __name__, description="Operation on stores")


@blp.route("/store/<string:sid>")
class Stores(MethodView):
    # get a store
    @blp.response(200, StoreSchema)
    def get(self, sid):
        store = StoreModel.query.get_or_404(sid)
        return store

    # delete a store
    def delete(self, sid):
        store = StoreModel.query.get_or_404(sid)
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
