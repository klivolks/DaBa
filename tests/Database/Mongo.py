import os
import unittest
from unittest import TestCase
from unittest.mock import patch, MagicMock
from daba.Mongo import collection, new_client, reset_client
from dotenv import load_dotenv


class TestDbFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mongo_url = os.getenv('MONGO_URL')
        cls.pool_size = int(os.getenv('MONGO_POOL_SIZE') or 100)

    @patch('daba.Mongo.pymongo.MongoClient.close')
    @patch('daba.Mongo.pymongo.MongoClient.__init__', return_value=None)
    def test_new_client(self, mock_client_init, mock_client_close):
        new_client("new_mongo_url")
        mock_client_close.assert_called_once()
        mock_client_init.assert_called_once_with("new_mongo_url", maxPoolSize=int(self.pool_size))

    @patch('daba.Mongo.pymongo.MongoClient.close')
    @patch('daba.Mongo.pymongo.MongoClient.__init__', return_value=None)
    def test_reset_client(self, mock_client_init, mock_client_close):
        reset_client()
        mock_client_close.assert_called_once()
        mock_client_init.assert_called_once_with(self.mongo_url, maxPoolSize=int(self.pool_size))


class TestDb(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mongo_url = os.getenv('MONGO_URL')
        cls.mongo_db = os.getenv('MONGO_DB')
        cls.pool_size = os.getenv('MONGO_POOL_SIZE')

    @patch('daba.Mongo.client')
    def test_init_db(self, mock_client):
        mock_database = MagicMock()
        mock_collection = MagicMock()

        # Setting up the mock to return our mock_database and mock_collection
        mock_client.__getitem__.return_value = mock_database
        mock_database.__getitem__.return_value = mock_collection

        db_obj = collection('test')
        self.assertIsInstance(db_obj.collection, MagicMock)

    @patch.object(collection, 'init_db')
    def test_close_db(self, mock_init):
        db_obj = collection('test')
        db_obj.close_db()
        self.assertTrue(mock_init.called)

    @patch.object(collection, 'close_db')
    @patch('daba.Mongo.pymongo.collection.Collection.find')
    def test_get(self, mock_find, mock_close_db):
        mock_find.return_value = [{'data': 'sample data'}]
        db_obj = collection('test')
        result = db_obj.get({'condition': 'sample'})
        self.assertEqual(result, [{'data': 'sample data'}])

    @patch.object(collection, 'close_db')
    @patch('pymongo.collection.Collection.insert_one')
    def test_put(self, mock_insert_one, mock_close_db):
        mock_insert_one.return_value = {'_id': 'sample_id', 'data': 'sample data'}
        db_obj = collection('test')
        result = db_obj.put({'data': 'sample data'})
        self.assertEqual(result, {'_id': 'sample_id', 'data': 'sample data'})

    @patch.object(collection, 'close_db')
    @patch('pymongo.collection.Collection.insert_many')
    def test_putMany(self, mock_insert_many, mock_close_db):
        mock_insert_many.return_value = [{'_id': 'sample_id', 'data': 'sample data'}]
        db_obj = collection('test')
        result = db_obj.putMany([{'data': 'sample data'}])
        self.assertEqual(result, [{'_id': 'sample_id', 'data': 'sample data'}])

    @patch.object(collection, 'close_db')
    @patch('pymongo.collection.Collection.update_one')
    def test_set(self, mock_update_one, mock_close_db):
        mock_update_one.return_value = {'_id': 'sample_id', 'data': 'sample data'}
        db_obj = collection('test')
        result = db_obj.set({'condition': 'sample'}, {'$set': {'data': 'new data'}})
        self.assertEqual(result, {'_id': 'sample_id', 'data': 'sample data'})

    @patch.object(collection, 'close_db')
    @patch('pymongo.collection.Collection.update_one')
    def test_inc(self, mock_update, mock_close_db):
        mock_update.return_value = {"n": 1, "nModified": 1, "ok": 1.0, 'updatedExisting': True}
        db_obj = collection('test')
        result = db_obj.inc({'Status': 1}, {'$inc': {'count': 1}})
        self.assertEqual(result, {"n": 1, "nModified": 1, "ok": 1.0, 'updatedExisting': True})

    @patch.object(collection, 'close_db')
    @patch('pymongo.collection.Collection.update_many')
    def test_setMany(self, mock_update_many, mock_close_db):
        mock_update_many.return_value = {"n": 1, "nModified": 1, "ok": 1.0, 'updatedExisting': True}
        db_obj = collection('test')
        result = db_obj.setMany({'condition': 'sample'}, {'$set': {'data': 'new data'}})
        self.assertEqual(result, {"n": 1, "nModified": 1, "ok": 1.0, 'updatedExisting': True})

    @patch.object(collection, 'close_db')
    @patch('pymongo.collection.Collection.find_one')
    def test_getOne(self, mock_find_one, mock_close_db):
        mock_find_one.return_value = {'_id': 'sample_id', 'data': 'sample data'}
        db_obj = collection('test')
        result = db_obj.getOne({'condition': 'sample'})
        self.assertEqual(result, {'_id': 'sample_id', 'data': 'sample data'})

    @patch.object(collection, 'close_db')
    @patch('pymongo.collection.Collection.find_one_and_update')
    def test_getAfterCount(self, mock_find_one_and_update, mock_close_db):
        mock_find_one_and_update.return_value = {'_id': 'sample_id', 'count': 1}
        db_obj = collection('test')
        result = db_obj.getAfterCount({'condition': 'sample'}, 'count')
        self.assertEqual(result, {'_id': 'sample_id', 'count': 1})

    @patch.object(collection, 'close_db')
    @patch('pymongo.collection.Collection.delete_one')
    def test_deleteOne(self, mock_delete_one, mock_close_db):
        mock_delete_one.return_value = {"n": 1, "ok": 1.0}
        db_obj = collection('test')
        result = db_obj.deleteOne({'condition': 'sample'})
        self.assertEqual(result, {"n": 1, "ok": 1.0})

    @patch.object(collection, 'close_db')
    @patch('pymongo.collection.Collection.delete_many')
    def test_deleteMany(self, mock_delete_many, mock_close_db):
        mock_delete_many.return_value = {"n": 2, "ok": 1.0}
        db_obj = collection('test')
        result = db_obj.deleteMany({'condition': 'sample'})
        self.assertEqual(result, {"n": 2, "ok": 1.0})

    @patch.object(collection, 'close_db')
    @patch('pymongo.collection.Collection.update_many')
    def test_removeElement(self, mock_update_many, mock_close_db):
        mock_update_many.return_value = {"n": 2, "nModified": 2, "ok": 1.0, 'updatedExisting': True}
        db_obj = collection('test')
        result = db_obj.removeElement({'condition': 'sample'}, {'field': 'element'})
        self.assertEqual(result, {"n": 2, "nModified": 2, "ok": 1.0, 'updatedExisting': True})

    @patch.object(collection, 'close_db')
    @patch('pymongo.collection.Collection.count_documents')
    def test_count(self, mock_count_documents, mock_close_db):
        mock_count_documents.return_value = 10
        db_obj = collection('test')
        result = db_obj.count({'condition': 'sample'})
        self.assertEqual(result, 10)


class TestDatabaseOperations(TestCase):

    @patch.object(collection, 'create_index')
    def test_create_index(self, mock_create_index):
        # Define the expected return value
        mock_create_index.return_value = 'index_name'

        # Create a db_obj (assuming collection is a class for managing MongoDB operations)
        db_obj = collection('test')

        # Call the method to test
        field = "username"
        unique = True
        index_name = db_obj.createIndex(field, unique=unique)

        # Assert the mock was called with the correct parameters
        mock_create_index.assert_called_once_with(field, unique=True)

        # Assert the result is as expected
        self.assertEqual(index_name, 'index_name')

    @patch.object(collection, 'create_index')
    def test_create_compound_index(self, mock_create_index):
        # Define the expected return value for a compound index
        mock_create_index.return_value = 'compound_index_name'

        # Create a db_obj (assuming collection is a class for managing MongoDB operations)
        db_obj = collection('test')

        # Call the method to test for a compound index
        compound_field = [("first_name", 1), ("last_name", 1)]
        index_name = db_obj.createIndex(compound_field, unique=False)

        # Assert the mock was called with the correct parameters (including default unique=False)
        mock_create_index.assert_called_once_with(compound_field, unique=False)

        # Assert the result is as expected
        self.assertEqual(index_name, 'compound_index_name')


if __name__ == '__main__':
    load_dotenv()
    unittest.main()
