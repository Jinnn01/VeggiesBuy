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


# get a specific store
''''
/store/sid based on the store id find the store
'''


@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not found")


# create new store
# /store create new store
@app.post("/store")
def create_store():
    # get data from user input: input a new store
    store_data = request.get_json()

    # name must be provided
    if "name" not in store_data:
        abort(
            400,
            message="Bad request. Ensure 'name' is included in the JSON payload."
        )
    # check store already exist or not
    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(400, message="Store already exists")
    # set store a unique id
    store_id = uuid.uuid4().hex
    # stores = { sid: new_store }
    new_store = {**store_data, "sid": store_id}
    # add new store to existing stores list
    stores[store_id] = new_store
    # 201, i acept the data and create a store
    return new_store, 201

# Delete store


@app.delete("/store/<string:store_id>")
def detele_store(store_id):
    try:
        del stores[store_id]
        return {"message": "store deleted"}
    except KeyError:
        abort(404, message="Store not found.")


# this name will be passed to the function
# user upload a new product-price in a particular store
# enter store id to check item in that store


# ITEM

# 1. get all the items
'''
/item get all items in item dictionary
'''


@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}


# 2. get an item from an item list
'''
/item/iid based on itemid to find that item
'''


@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Item not found")

# 3. create a new item
# /item create new items


@app.post("/item")
def create_item():
    item_data = request.get_json(force=True)
    if (
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        abort(400, message="Bad request. Ensure 'price','store_id',and 'name' are included in the JSON payload")

    # validate the data to ensure, the item can be added twice
    for item in items.values():
        if (item_data["name"] == item["name"] and item_data["store_id"] == item["store_id"]):
            abort(400, message="Item already exists.")

    if item_data["store_id"] not in stores:
        abort(404, message="Store not found")

    item_id = uuid.uuid4().hex
    item = {**item_data, "vid": item_id}
    items[item_id] = item

    return item, 201

# 4. Delete an item


@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted."}
    except KeyError:
        abort(404, message="Item not found.")


# 5. Update an item
@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_new_data = request.get_json(force=True)
    if "price" not in item_new_data:
        abort(400, message="Bad request. Ensure 'price' is included in the JSON payload")
    try:
        item = items[item_id]
        # in place, means update data in pairs
        item["price"] = item_new_data["price"]
        # item["name"] = item_new_data["name"]
        return item, 201
    except KeyError:
        abort(404, message="Item not found.")
