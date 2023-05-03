from db import db

# mapping between row in a table to a python class


class UserModel(db.Model):
    # use a table called items
    __tablename__ = "users"
    # columns should be in this table
    uid = db.Column(db.Integer, primary_key=True)
    # can not insert null value as a name, unique = True => items have different name, if there is no unique, means, multiplate item name can be the same
    uname = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    # users = db.relationship("UserModel", back_populates="upload")
