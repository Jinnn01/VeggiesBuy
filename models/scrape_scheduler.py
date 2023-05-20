
import time

import requests
from apscheduler.schedulers.background import BackgroundScheduler
import logging

from flask import jsonify, redirect
from flask_smorest import Blueprint

from models import c_webscraper as CS, StoreModel
from models import w_webscraper as WS
from resources.batch_upload import batch_upload_data
blp = Blueprint("web_scrap", __name__, description="Batch upload of items")


# Create a lock for synchronization

# coles webscraping
@blp.route('/coles_scrap', methods=['POST'])
def c_job():
    try:
        # make sure complete chrome with display is installed inside the container
        output = CS.c_scrape()
        # output = [[['coles wollongong', '200 crown street, wollongong'],
        #            [{'lebanese cucumbers': '5.90'}, {'fresh brown onions loose': '3.70'}, {'broccoli': '4.50'},
        #             {'red capsicum': '7.90'}, {'sweet gold potatoes loose': '4.90'}]],
        #           [['coles fairy meadow', '118-126 princes hwy, fairy meadow'],
        #            [{'broccoli': '4.50'}, {'lebanese cucumbers': '5.90'}, {'red capsicum': '7.90'},
        #             {'fresh brown onions loose': '3.70'}, {'sweet gold potatoes loose': '4.90'}]]]
        for each_store_info in output:
            sname = each_store_info[0][0].title()

            store_row = StoreModel.query.filter_by(sname=sname).first()

            if not store_row:
                logging.debug("store not found - abort")
                return jsonify({'message': 'OCR upload unsuccessfull'})

            items = []
            for each in each_store_info[1]:
                item_dict = {
                    "item": None,
                    "price": None,
                    "unit": "kg"
                }
                for key, val in each.items():
                    item_dict["item"] = key
                    item_dict["price"] = val
                    items.append(item_dict)

            batch_upload_data(sname, items)

        return jsonify({'message': 'OCR upload successfull'})

    except Exception as e:
        logging.exception(e)

    return jsonify({'message': 'OCR upload unsuccessfull'})


# woolworths web scraping
@blp.route('/wools_scrap', methods=['POST'])
def w_job():
    try:
        output = WS.w_scrape()
        # output = [{'solanato tomato punnet': '17.50'}, {'baby leaf spinach': '25.00'}, {'baby spinach spinach': '17.86'},
        #  {'cherry tomatoes punnet': '12.00'}, {'baby spinach 60g': '33.33'},
        #  {'the odd bunch zucchini prepacked': '6.27'}, {'tomato truss punnet': '13.80'},
        #  {'gourmet tomatoes punnet 1kg': '10.70'}, {'select gourmet tomatoes punnet': '14.38'},
        #  {'perfection mix a mato mini tomatoes': '20.31'}, {'truss cocktail tomato punnet': '18.00'}]

        sname = 'Woolworths Wollongong'


        store_row = StoreModel.query.filter_by(sname=sname).first()

        if not store_row:
            logging.debug("store not found - abort")
            return jsonify({'message': 'OCR upload unsuccessfull'})

        items = []
        for each in output:
            item_dict = {
                "item": None,
                "price": None,
                "unit": "kg"
            }
            for key, val in each.items():
                item_dict["item"] = key
                item_dict["price"] = val
                items.append(item_dict)

        batch_upload_data(sname, items)

        return jsonify({'message': 'OCR upload successfull'})

    except Exception as e:
        logging.exception(e)

    return jsonify({'message': 'OCR upload unsuccessfull'})

def c_conn():
    try:
        # make sure proper docker network config is set
        # Make the request to the desired endpoint - make sure url is right for the hosted container and port
        response = requests.post('http://172.17.0.1:5001/coles_scrap')

        # Process the response as needed
        if response.status_code == 200:
            # Request successful
            logging.debug('Request succeeded')
        else:
            # Request failed
            logging.debug('Request failed')
    except Exception as e:
        logging.debug(e)

def w_conn():
    try:
        # make sure proper docker network config is set
        # Make the request to the desired endpoint - make sure url is right for the hosted container and port
        response = requests.post('http://172.17.0.1:5001/wools_scrap')

        # Process the response as needed
        if response.status_code == 200:
            # Request successful
            logging.debug('Request succeeded')
            data = response.json()
            # Process the response data as needed
        else:
            # Request failed
            logging.debug('Request failed')
    except Exception as e:
        logging.debug(e)


# scheduling job
@blp.route('/start_schedule', methods=['POST'])
def all_scheduled_job():

    scheduler = BackgroundScheduler()

    # Schedule the w_conn job to run at 12 am every day
    scheduler.add_job(func=w_conn, trigger="cron", hour=0, minute=5)

    # Schedule the c_conn job to run at 12 am every day
    scheduler.add_job(func=c_conn, trigger="cron", hour=0, minute=25)

    scheduler.start()
