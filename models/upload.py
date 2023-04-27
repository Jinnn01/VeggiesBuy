from db import db


class UploadModel(db.Model):
    # use a table called items
    __tablename__ = "upload"

    uploadid = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.ForeignKey(
        "users.uid"), unique=False, nullable=False)
    uname = db.Column(db.String(80), unique=False, nullable=False)
    vid = db.Column(db.ForeignKey(
        "items.vid"), unique=False, nullable=False)
    sid = db.Column(db.ForeignKey(
        "stores.sid"), unique=False, nullable=False)
    # insertTime = db.Column(db.TIMESTAMP)
#     # relationship with items, link store with items
    # upload = db.relationship(
    #     "StoreModel", back_populates="stores", lazy="dynamic")
    # upload = db.relationship(
    #      "ItemModel", back_populates="items", lazy="dynamic")
    # upload = db.relationship(
    #     "UserModel", back_populates="users", lazy="dynamic")
