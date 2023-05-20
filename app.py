import os
import threading

import schedule
from flask import Flask
from flask_smorest import Api
from sqlalchemy import create_engine
from db import db
from models import StoreModel, ItemModel
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.user import blp as UserBlueprint
from datetime import datetime
# from processdata import processdata
from resources.ocr_endpoint import  blp as ocr_endpoint
from models import scrape_scheduler
from resources.batch_upload import blp as batch_upload
from models.scrape_scheduler import blp as web_scrap, c_conn, w_conn


def create_app(db_url=None):
    app = Flask(__name__, instance_path=os.getcwd())
    # app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    # database url connect to database, environment variable for secert info
    # app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
    #    "DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///data.db"
    # app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///newdata.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    

    db.init_app(app)
    api = Api(app)

    # @app.before_request
    # @app.before_first_request
    with app.app_context():
        # def create_tables():
        db.create_all()
        # tables in models folder

        store_data = [
            {
                "slatitude": "-34.3938",
                "saddress": "102/110 Princes Hwy, Fairy Meadow NSW 2519",
                "slongitude": "150.8932",
                "sname": "ALDI Fairy Meadow"
            },
            {
                "slatitude": "-34.4280",
                "saddress": "25 Stewart St, Wollongong NSW 2500",
                "slongitude": "150.8991",
                "sname": "ALDI Wollongong"
            },
            {
                "slatitude": "-34.3947",
                "saddress": "The New Ambience, Elliotts Rd, Fairy Meadow NSW 2519",
                "slongitude": "150.8932",
                "sname": "Coles Fairy Meadow"
            },
            {
                "slatitude": "-34.4243",
                "saddress": "200 Crown St, Wollongong NSW 2500",
                "slongitude": "150.8926",
                "sname": "Coles Wollongong"
            },
            {
                "slatitude": "-34.3917",
                "saddress": "66 Princes Hwy, Fairy Meadow NSW 2519",
                "slongitude": "150.8937",
                "sname": "Woolworths Fairy Meadow"
            },
            {
                "slatitude": "-34.42703",
                "saddress": "63 Burelli St, Wollongong NSW 2500",
                "slongitude": "150.89611",
                "sname": "Woolworths Wollongong"
            },
            {
                "slatitude": "-34.3968",
                "saddress": "75 Princes Hwy, Fairy Meadow NSW 2519",
                "slongitude": "150.8919",
                "sname": "Leisure Coast Fruit Market & Deli"
            }

        ]

        for store in store_data:
            sname = store['sname']
            saddress = store['saddress']
            slatitude = store['slatitude']
            slongitude = store['slongitude']

            # Check if the store already exists in the database
            existing_store = StoreModel.query.filter_by(sname=sname).first()
            if existing_store:
                # Update the store details
                existing_store.saddress = saddress
                existing_store.slatitude = slatitude
                existing_store.slongitude = slongitude
            else:
                # Create a new store
                new_store = StoreModel(
                    sname=sname, saddress=saddress, slatitude=slatitude, slongitude=slongitude)
                db.session.add(new_store)

        db.session.commit()


        # starting webscraping scheduler
        scrape_scheduler.scrape_thread()
        # scrape_scheduler.all_scheduled_job()



    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(UserBlueprint)
    # api.register_blueprint(UploadBlueprint)
    api.register_blueprint(ocr_endpoint)
    api.register_blueprint(batch_upload)
    api.register_blueprint(web_scrap)

    return app
