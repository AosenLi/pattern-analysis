import argparse, urllib, json
from datetime import datetime
from pymongo import MongoClient, GEOSPHERE
from pymongo.errors import (PyMongoError, BulkWriteError)
import generate_FoodList
import csv
import matplotlib.pyplot as plt


client = MongoClient('localhost',27017)
db = client['testdb']
filter_collection = db['picture']
suburbs = db['suburbs']


def draw_pie_chart(statistics):
    for suburb in statistics.keys():
        plt.title(suburb)
        plt.pie([float(v) for v in statistics[suburb].values()], labels = [k for k in statistics[suburb].keys()], autopct='%1.1f%%')
        plt.show()
    return


def get_suburb(location):
    suburb_info = suburbs.find_one({"geometry":{"$geoIntersects":{"$geometry":location}}})
    suburb = 'None'
    if suburb_info:
        suburb = suburb_info['properties']['SA2_NAME16']
    return suburb


def suburb_statistics():
    statistics = {}

    for item in filter_collection.find():
        classification = item['pic_pred']
        location = item['pic_loc']
        print(classification)
        suburb = get_suburb(location)
        print(suburb)

        if suburb != 'None':
            if suburb in statistics.keys():
                if classification in statistics[suburb].keys():
                    statistics[suburb][classification] += 1
                else:
                    statistics[suburb][classification] = 1
            else:
                statistics[suburb] = {}
                statistics[suburb][classification] = 1
    return statistics


def analysis():

    statistics = suburb_statistics()
    draw_pie_chart(statistics)


if __name__ == '__main__':
    analysis()