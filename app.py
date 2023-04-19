from flask import Flask, request
from db import items, stores
from flask_smorest import abort
# for document
import uuid

app = Flask(__name__)

'''
json style
stores = [
    {
        "sname": "My store",
        "item": [
            {
                "vname": "sweet corn",
                "price": 3.99
            },
            {
                "vname": "Tomato",
                "price": 2.99
            },
            {
                "vname": "Potato",
                "price": 4.50
            }
        ]
    }
]
'''

# create an endpoint, return data when user request

# /store get all stores data


@app.get("/store")  # http://127.0.0.1:5000/store
# function related to the endpoint
def get_stores():
    return {"stores": list(stores.values())}

# create new store

# /store create new store


@app.post("/store")
def create_store():
    # get data from user input: input a new store
    store_data = request.get_json()
    # set store a unique id
    store_id = uuid.uuid4().hex
    # stores = { sid: new_store }
    new_store = {**store_data, "sid": store_id}
    # add new store to existing stores list
    stores[store_id] = new_store
    # 201, i acept the data and create a store
    return new_store, 201


# this name will be passed to the function

# user upload a new product-price in a particular store
# enter store id to check item in that store
'''
/item create new items
'''


@app.post("/item")
def create_item(name):
    item_data = request.get_json(force=True)
    if item_data["store_id"] not in stores:
        abort(404, message="Store not found")

    item_id = uuid.uuid4().hex
    item = {**item_data, "vid": item_id}
    items[item_id] = item

    return item, 201


# get all the items
'''
/item get all items in item dictionary
'''


@app.get("/item")
def get_all_items():
    return {"items": list(items.value())}

# how to get a specific store and its items
# 1. get a specific store


''''
/store/sid based on the store id find the store
'''


@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not found")


# 2. get items from a specific store
'''
/item/iid based on itemid to find that item
'''


@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Item not found")


# 3. list items from a store
'''
@app.get("/store/<string:sname>/item")
# name is the store name
def get_all_item(sname):
    for store in stores:
        if store["sname"] == sname:
            return {"item": store["item"]}
    return {"Message": "Store not found"}, 404
'''
# 4. get a item from a store
