from flask_smorest import Blueprint, abort
from db import db
from flask import request, jsonify
from models import StoreModel, ItemModel

import logging
import datetime
import re

from sqlalchemy import *


logging.basicConfig(level=logging.DEBUG)
blp = Blueprint("batch_upload", __name__, description="Batch upload of items")


def date_locator(date_str):
    """
    takes str(datetime) and return dates in y-m-d format
    :param date_str:
    :return: dates in y-m-d format
    """
    date_str = str(date_str)
    date = re.search(r'\d{2}[-/]\d{2}[-/]\d{4}', date_str)
    if date:
        pattern = r"/|-"
        res = re.split(pattern, date.group(0))
        d, m, y = int(res[0]), int(res[1]), int(res[2])
        converted_date_string = datetime.datetime(y, m, d)
        return converted_date_string

    date = re.search(r'\d{4}[-/]\d{2}[-/]\d{2}', date_str)
    if date:
        pattern = r"/|-"
        res = re.split(pattern, date.group(0))
        y, m, d = int(res[0]), int(res[1]), int(res[2])
        converted_date_string = datetime.datetime(y, m, d)
        return converted_date_string

"""\
{ sname, timestamp
    item -> array of { item, price, unit}
"""

@blp.route('/batch_upload', methods=['POST'])
def batch_upload_data(sname, items, timestamp_dt=datetime.datetime.now()):
    logging.debug("batch_upload function")

    # for each vegetable
    for each_veg in items:
        vname = str(each_veg['item']).lower()
        vprice = each_veg['price']
        unit = each_veg['unit']

        # item = ItemModel.query.filter_by(sname=sname).first()
        sql_item = ItemModel.query.filter(and_(ItemModel.sname == sname, ItemModel.vname == vname)).first()

        # if veg exists in DB -> update the item , else -> create a item

        if sql_item:
            if timestamp_dt < sql_item.updateTime:
                logging.debug(timestamp_dt)
                logging.debug('provided entries are old')
                continue
            logging.debug(f'updating item: {vname}')
            sql_item.vname = vname
            sql_item.price = vprice
            if sql_item.unit:
                sql_item.unit = unit
            else:
                sql_item.unit = 'kg'
            sql_item.updateTime = timestamp_dt
        else:
            logging.debug(f'creating item: {vname}')
            item = ItemModel(vname=vname, price=vprice, unit=unit,
                        sname=sname, updateTime=timestamp_dt)
            db.session.add(item)


    # Commit the changes to the database
    db.session.commit()

    logging.debug("batch_upload success")

    return


@blp.route('/ocr_upload', methods=['POST'])
def ocr_upload():
    logging.debug("/ocr_upload")

    # Get the JSON data from the request body
    data = request.json

    store = data["store"]
    address = data["location"]
    timestamp = str(data["timestamp"])
    timestamp = timestamp.split(" ")[0]
    timestamp_dt = date_locator(timestamp)
    items = data["items"]

    store_row = StoreModel.query.filter_by(saddress=address).first()

    if not store_row:
        logging.debug("store not found - abort")
        return jsonify({'message': 'OCR upload unsuccessfull'})
    sname = store_row.sname

    logging.debug("passed to batch upload function")
    batch_upload_data(sname, items, timestamp_dt)

    return jsonify({'message': 'OCR upload successful'})



