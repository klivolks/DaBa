"""
Mongo database is handled here
Improved db class.
"""

import pymongo
import os
from dotenv import load_dotenv
import logging

load_dotenv()
mongo_url = os.environ.get('MONGO_URL')
pool_size = int(os.getenv('MONGO_POOL_SIZE') or 100)
client = pymongo.MongoClient(mongo_url, maxPoolSize=pool_size)

logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    handler = logging.FileHandler('daba-error.log')
    handler.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def new_client(connection_string):
    global client
    global pool_size
    client.close()
    client = pymongo.MongoClient(connection_string, maxPoolSize=pool_size)


def reset_client():
    global client
    global mongo_url
    global pool_size
    client.close()
    client = pymongo.MongoClient(mongo_url, maxPoolSize=pool_size)


class collection:
    # Setting database
    def __init__(self, collection_name, db=None):
        self.collection = self.init_db(collection_name, db)

    def init_db(self, collection_name, db=None):
        mongo_db = db if db else os.environ.get('MONGO_DB')
        database = client[mongo_db]
        return database[collection_name]

    def close_db(self):
        self.collection.database.client.close()

    def get(self, condition=None, limiter=None):
        # Get all values from defined collection
        if condition is None:
            condition = {}
        return self.exec_operation(self.collection.find, condition, limiter)

    def find(self, condition=None):
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
        """
        Count the number of documents in the collection
        :param condition: The query
        :return: Total count of the document
        """
        if condition is None:
            condition = {}
        return self.exec_operation(self.collection.count_documents, condition)

    def createIndex(self, field, unique=False, **kwargs):
        """
        Create an index on the specified field using exec_operation.

        :param field: The field to index (str or list of tuples for compound indexes).
        :param unique: Whether the index should enforce uniqueness (default: False).
        :param kwargs: Additional parameters to pass to the create_index method.
        :return: The name of the created index.
        """
        index_options = {"unique": unique, **kwargs}
        # Ensure the index creation passes unique by default
        return self.collection.create_index(field, **index_options)

    def exec_operation(self, operation, *args):
        try:
            response = operation(*args)
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise
        return response
