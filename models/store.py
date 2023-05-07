from db import db


# mapping between row in a table to a python class
class StoreModel(db.Model):
    # use a table called items
    __tablename__ = "stores"

    # sid = db.Column(db.Integer, primary_key=True)
    sname = db.Column(db.String(80), unique=True,
                      nullable=False, primary_key=True)
    # TODO: Store location or phone number
    saddress = db.Column(db.String, nullable=False)
    # TODO:经纬度: latitude and longitude
    slatitude = db.Column(db.String, nullable=False)
    slongitude = db.Column(db.String, nullable=False)

    # relationship with items, link store with items
    # if store is deleted, then all the items will be deleted
    items = db.relationship(
        "ItemModel", back_populates="stores", lazy="dynamic", cascade="all,delete")
    # upload = db.relationship(
    #     "UploadModel", back_populates="stores", lazy="dynamic", cascade="all,delete")
