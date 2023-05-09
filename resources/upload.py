# handle upload
import uuid
# from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import UploadModel, ItemModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas1 import PlainUploadSchema

blp = Blueprint("upload", __name__, description="Uploading")


@blp.route("/upload/<int:uploadid>")
class Uploads(MethodView):
    # get a store
    @blp.response(200, PlainUploadSchema)
    def get(self, uploadid):
        upload = UploadModel.query.get_or_404(uploadid)
        return upload

    # @blp.arguments(PlainUploadSchema)
    # @blp.response(200, PlainUploadSchema)
    # def post(self, upload_data):
    #     upload = UploadModel(**upload_data)
    #     # try:
    #     # not in db yet
    #     db.session.add(upload)
    #     # in the db
    #     db.session.commit()


@blp.route("/upload/<string:vname>")
class Uploads(MethodView):
    # get a store
    @blp.response(200, PlainUploadSchema)
    def get(self, vname):
        item = ItemModel.query.filter(ItemModel.vname == vname)
        return item


@blp.route("/upload")
class UploadList(MethodView):
    # create a store
    @blp.arguments(PlainUploadSchema)
    @blp.response(200, PlainUploadSchema)
    def post(self, upload_data):
        upload = UploadModel(**upload_data)
        # try:
        # not in db yet
        db.session.add(upload)
        # in the db
        db.session.commit()
        # except IntegrityError:
        # abort(400, message="A store with that name already exists")

        return upload

    # @blp.arguments(ItemUpdateSchema)
    # @blp.response(200, ItemSchema)
    # # update an item, item_data from input
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

    @blp.arguments(PlainUploadSchema)
    @blp.response(200, PlainUploadSchema)
    def put(self, upload_data):
        item = ItemModel.query.filter(
            ItemModel.vname == upload_data["vname"]).all()
        return item

        # if item:
        #     if item.price != upload_data["vprice"]:
        #         item.price = upload_data["vprice"]

        #     db.session.add(item)
        #     db.session.commite()

        # return {"message": "Item has been updated"}

    # @blp.arguments(ItemUpdateSchema)
    # @blp.response(200, ItemSchema)
    # # update an item, item_data from input
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


# @blp.route("/upload/item")
# class UploadList(MethodView):
#     # create a store
#     @blp.arguments(PlainUploadSchema)
#     @blp.response(200, PlainUploadSchema)
#     def post(self, upload_data):
#         upload = UploadModel(**upload_data)
#         # try:
#         # not in db yet
#         db.session.add(upload)
#         # in the db
#         db.session.commit()
#         # except IntegrityError:
#         # abort(400, message="A store with that name already exists")

#         return upload
