import base64
import io
from flask import Flask, request
from flask_cors import CORS
from imageio import imread

app = Flask(__name__)
CORS(app)
stores = [{"name": "My Store", "items": [{"name": "Chair", "price": 15.99}]}]

@app.post("/dictionary")
def create_dictionary():
    request_data = request.get_json();
    print(request_data);
    #b64_bytes = base64.b64encode(request_data)
    #b64_string = request_data.decode()

    # reconstruct image as an numpy array
    img = imread(io.BytesIO(base64.b64decode(request_data)))
    return {"result": True}

@app.get("/store")
def get_stores():
    return {"stores": stores}


@app.post("/store")
def create_store():
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)
    return new_store, 201


@app.post("/store/<string:name>/item")
def create_item(name):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {"name": request_data["name"], "price": request_data["price"]}
            store["items"].append(new_item)
            return new_item, 201
    return {"message": "Store not found"}, 404


@app.get("/store/<string:name>")
def get_store(name):
    for store in stores:
        if store["name"] == name:
            return store
    return {"message": "Store not found"}, 404


@app.get("/store/<string:name>/item")
def get_item_in_store(name):
    for store in stores:
        if store["name"] == name:
            return {"items": store["items"]}
    return {"message": "Store not found"}, 404
