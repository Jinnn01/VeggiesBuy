from db import db
from datetime import datetime


class UploadModel(db.Model):
    # use a table called items
    __tablename__ = "upload"
    uploadid = db.Column(db.Integer, primary_key=True)
    # uid = db.Column(db.Integer, db.ForeignKey(
    #     "users.uid"), unique=False, nullable=False)
    vname = db.Column(db.String(80), unique=False, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    # sname = db.Column(db.String(80), db.ForeignKey(
    #     "stores.sname"), unique=False, nullable=False)

    insertTime = db.Column(db.DateTime, default=datetime.now)
#     # relationship with items, link store with items
    # stores = db.relationship(
    #     "StoreModel", foreign_keys="stores.sname", back_populates="upload",)
    # items = db.relationship(
    #     "ItemModel", back_populates="items")
    # users = db.relationship(
    #     "UserModel", foreign_keys="users.uid", back_populates="users")
