# from db import db


# # mapping between row in a table to a python class
# class UploadModel(db.Model):
#     # use a table called items
#     __tablename__ = "Upload"

#     userid = db.Column(db.Integer, primary_key=True)
#     vname = db.Column(db.String(80), unique=False, nullable=False)
#     sname = db.Column(db.String(80), unique=False, nullable=False)
    

#     # relationship with items, link store with items
#     items = db.relationship(
#         "ItemModel", back_populates="stores", lazy="dynamic")