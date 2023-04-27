# handle upload
import uuid
# from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import UserModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas1 import UserSchema

blp = Blueprint("user", __name__, description="Operations on users")


@blp.route("/user/<string:uid>")
class Users(MethodView):
    # get a store
    @blp.response(200, UserSchema)
    def get(self, uid):
        user = UserModel.query.get_or_404(uid)
        return user


@blp.route("/upload")
class UserList(MethodView):
    # create a store
    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    def post(self, user_data):
        user = UserModel(**user_data)
        # try:
        # not in db yet
        db.session.add(user)
        # in the db
        db.session.commit()
        # except IntegrityError:
        # abort(400, message="A store with that name already exists")

        return user
