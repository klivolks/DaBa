"""
Mongo database is handled here
Improved db class.
"""

import pymongo
import os
from dotenv import load_dotenv


class collection:
    # Setting database
    def __init__(self, collection):
        self.collection = self.init_db(collection)

    def init_db(self, collection):
        load_dotenv()
        mongo_url = os.environ.get('MONGO_URL')
        mongo_db = os.environ.get('MONGO_DB')
        client = pymongo.MongoClient(mongo_url)
        database = client[mongo_db]
        return database[collection]

    def close_db(self):
        self.collection.database.client.close()

    def get(self, condition=None, limiter=None):
        # Get all values from defined collection
        if condition is None:
            condition = {}
        return self.exec_operation(self.collection.find, condition, limiter)

    def find(self, condition=None, limiter=None):
        # Get all values from defined collection
        if condition is None:
            condition = {}
        return self.exec_operation(self.collection.aggregate, condition)

    def put(self, data):
        # Put data into collection
        return self.exec_operation(self.collection.insert_one, data)

    def putMany(self, data):
        # Put many data into collection
        return self.exec_operation(self.collection.insert_many, data)

    def set(self, condition, data, upsert=False):
        # Update data
        return self.exec_operation(self.collection.update_one, condition, {"$set": data}, upsert)

    def inc(self, condition, data, upsert=False):
        # Update data
        return self.exec_operation(self.collection.update_one, condition, {"$inc": data}, upsert)

    def setMany(self, condition, data, upsert=False):
        # Update many data
        return self.exec_operation(self.collection.update_many, condition, {"$set": data}, upsert)

    def getOne(self, condition, limiter=None):
        # Returns only one value
        return self.exec_operation(self.collection.find_one, condition, limiter)

    def getAfterCount(self, condition, counter):
        # Get data after updating the count
        countElement = {"$inc": {counter: 1}}
        return self.exec_operation(self.collection.find_one_and_update, condition, countElement)

    def deleteOne(self, condition):
        # Delete one data from the collection
        return self.exec_operation(self.collection.delete_one, condition)

    def deleteMany(self, condition):
        # Delete many data from the collection
        return self.exec_operation(self.collection.delete_many, condition)

    def removeElement(self, condition, data):
        # Remove specific element from the collection
        return self.exec_operation(self.collection.update_many, condition, {"$unset": data}, False)

    def count(self, condition=None):
        # Count the number of documents in the collection
        if condition is None:
            condition = {}
        return self.exec_operation(self.collection.count_documents, condition)

    def exec_operation(self, operation, *args):
        try:
            response = operation(*args)
            self.close_db()
            return response
        except Exception as e:
            print(f"An error occurred: {e}")
            self.close_db()
