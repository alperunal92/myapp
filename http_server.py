# -*- coding: utf-8 -*-

from flask import Flask
from flask_cors import CORS
import json
import numpy as np
import random
import time
import os

global example_data, config

app = Flask(__name__)
cors = CORS(app)

app.config['JSON_AS_ASCII'] = True


def make_row(config):
    product = random.choice(config['products'])
    provider = random.choice(config['providers'])
    cash = np.random.randint(low=3000, high=5000)
    saleClosed = random.choice([True, False])

    row = {
        "ProductDesc": product['title'],
        "FirmName": provider['FirmName'],
        "Cash": cash,
        "QuotaInfo": {
            "HasDiscount": product['discountRate'] > 0,
            "PremiumWithDiscount": np.round(cash * (1 - product['discountRate']), 2) if product[
                                                                                            'discountRate'] > 0 else 0
        },
        "SaleClosed": saleClosed,
        "ImagePath": provider["ImagePath"]
    }

    if product.get("popoverContent") is not None:
        row['popoverContent'] = product.get("popoverContent")
    return row


def create_response_data(config, num_min=4, num_max=9):
    num_offers = np.random.randint(num_min, num_max)
    offerList = {
        "offerList": [make_row(config) for x in range(num_offers)]
    }
    return offerList


@app.route("/")
def home():
    return "Please use one of the following endpoints described in the task list: /example, /case1, /case2, /get_offer_count, /case3"


@app.route("/example")
def example():
    return example_data


@app.route("/case1")
def case1():
    return create_response_data(config, 4, 9)


@app.route("/case2")
def case2():
    sleep_duration_sec = np.random.randint(7, 15)
    time.sleep(sleep_duration_sec)
    # return response after waiting for some time to simulate offer collection
    return create_response_data(config, 4, 9)


@app.route("/get_offer_count")
def get_offer_count():
    return {"num_offers": np.random.randint(4, 9)}


@app.route("/case3")
def case3():
    sleep_duration_sec = np.random.randint(5, 10)
    time.sleep(sleep_duration_sec)
    return make_row(config)

if __name__ == "__main__":
    with open('listing-data.json') as json_file:
        example_data = json.load(json_file)

    with open('config.json', encoding='utf-8') as json_file:
        config = json.load(json_file)
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
