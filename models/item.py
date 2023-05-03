from db import db


# mapping between row in a table to a python class
class ItemModel(db.Model):
    # use a table called items
    __tablename__ = "items"
    # columns should be in this table
    vid = db.Column(db.Integer, primary_key=True)
    # can not insert null value as a name, unique = True => items have different name, if there is no unique, means, multiplate item name can be the same
    vname = db.Column(db.String(80), unique=False, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    # store id as a foreignkey
    sid = db.Column(db.Integer, db.ForeignKey(
        "stores.sid"), unique=False, nullable=False)
    # store variable with storemodel object, whose id will match the foreignkey
    # link item with stores
    stores = db.relationship("StoreModel", back_populates="items")
    # TODO:1.the time of inserting price
    # updateTime = db.Column(db.TIMESTAMP, nullable=False)
    # TODO:2. description of veggies
    vdescr = db.Column(db.String, nullable=True)


# itemsearch = ItemModel.query.filter(ItemModel.vname == "Tomato").all()

# for item in itemsearch:
#     print(item)
