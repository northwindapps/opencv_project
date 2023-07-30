import base64
import io
import os
import cv2 as cv
import numpy as np
from flask import Flask, request
from flask_cors import CORS
from imageio.v2 import imread
import pytesseract

app = Flask(__name__)
CORS(app)

@app.get("/hello")
def hello():
    return {"result", True}

@app.post("/dictionary")
def create_dictionary():
    request_data = request.get_json()
    #b64_bytes = base64.b64encode(request_data)
    #b64_string = request_data.decode()

    # reconstruct image as an numpy array
    img = imread(io.BytesIO(base64.b64decode(request_data)))
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    large = cv.resize(gray, None, fx = 2.0, fy = 2.0, interpolation= cv.INTER_CUBIC)
    adaptive_gaussian = cv.adaptiveThreshold(large, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,11,9)
    value, thre = cv.threshold(adaptive_gaussian, 110,255,cv.THRESH_BINARY)
    text2 = pytesseract.image_to_string(thre)
    array = text2.splitlines()
    filtered = []
    for item in array:
        if bool(item and item.strip()):
            filtered.append(item)
    print(filtered)

    cv.imwrite("reconstructed.jpg", gray)
    # cv.imshow('img', gray)
    # with open("compare.jpg", "wb") as file:
    #     file.write(base64.b64decode(request_data))
    return {"result": filtered}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)