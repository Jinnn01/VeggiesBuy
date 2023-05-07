# handle upload
import uuid
# from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import UploadModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas1 import PlainUploadSchema

blp = Blueprint("upload", __name__, description="Uploading")


@blp.route("/upload/<string:uploadid>")
class Uploads(MethodView):
    # get a store
    @blp.response(200, PlainUploadSchema)
    def get(self, uploadid):
        upload = UploadModel.query.get_or_404(uploadid)
        return upload


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
