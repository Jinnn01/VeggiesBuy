import threading
import time

import requests
import schedule
import logging

from flask import jsonify, redirect
from flask_smorest import Blueprint

from models import c_webscraper as CS, StoreModel
from models import w_webscraper as WS
from resources.batch_upload import batch_upload_data
blp = Blueprint("web_scrap", __name__, description="Batch upload of items")


# Create a lock for synchronization
lock = threading.Lock()

# coles webscraping
@blp.route('/coles_scrap', methods=['POST'])
def c_job():
    try:
        # make sure complet chrome with display is installed inside the container
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


# scheduling job
def all_scheduled_job():
    #actual jobs
    schedule.every().day.at("00:00").do(c_conn)
    schedule.every().day.at("00:30").do(w_conn)

    while True:
        schedule.run_pending()
        if not schedule.jobs:
            time.sleep(3)
            break


# Create a new thread for running the scheduled job
def scrape_thread():
    thread1 = threading.Thread(target=all_scheduled_job)

    # Start the thread
    thread1.start()


def c_conn():
    lock.acquire()
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
    lock.release()

def w_conn():
    lock.acquire()
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
    lock.release()
