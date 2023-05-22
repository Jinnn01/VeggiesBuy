from db import db
from datetime import datetime


# mapping between row in a table to a python class
class ItemModel(db.Model):
    # use a table called items
    __tablename__ = "items"
    # columns should be in this table
    vid = db.Column(db.Integer, primary_key=True)
    # can not insert null value as a name, unique = True => items have different name, if there is no unique, means, multiplate item name can be the same
    vname = db.Column(db.String(80), unique=False, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    unit = db.Column(db.String(80),unique=False)
    # store id as a foreignkey
    sname = db.Column(db.String(80), db.ForeignKey(
        "stores.sname"), unique=False, nullable=False)
    updateTime = db.Column(db.DateTime, default=datetime.now)

    # store variable with storemodel object, whose id will match the foreignkey
    # link item with stores, sid as a foreign key

    # TODO: 单位
    stores = db.relationship("StoreModel", back_populates="items")

    # vdescr = db.Column(db.String, nullable=True)

    # upload
    # upload = db.relationship(
    #   "UploadModel", back_populates="items", lazy="dynamic", cascade="all,delete")
