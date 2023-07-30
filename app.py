import base64
import io
import os
import cv2 as cv
import numpy as np
from flask import Flask, request
from flask_cors import CORS
from imageio import imread
import matplotlib.pyplot as plt
import pytesseract

os.putenv('TESSDATA_PREFIX',r"C:\Users\user\Downloads\fra.traineddata")

app = Flask(__name__)
CORS(app)
stores = [{"name": "My Store", "items": [{"name": "Chair", "price": 15.99}]}]
pytesseract.pytesseract.tesseract_cmd = "C:\Program Files\Tesseract-OCR\\tesseract.exe"

@app.post("/dictionary")
def create_dictionary():
    request_data = request.get_json()
    #b64_bytes = base64.b64encode(request_data)
    #b64_string = request_data.decode()

    # reconstruct image as an numpy array
    img = imread(io.BytesIO(base64.b64decode(request_data)))
    #plt.figure()
    #plt.imshow(img, cmap="gray")
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    large = cv.resize(gray, None, fx = 2.0, fy = 2.0, interpolation= cv.INTER_CUBIC)
    adaptive_gaussian = cv.adaptiveThreshold(large, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,11,9)
    value, thre = cv.threshold(adaptive_gaussian, 110,255,cv.THRESH_BINARY)
    text2 = pytesseract.image_to_string(thre)
    print(text2)
    cv.imwrite("reconstructed.jpg", gray)
    cv.imshow('img', gray)
    # with open("compare.jpg", "wb") as file:
    #     file.write(base64.b64decode(request_data))
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
