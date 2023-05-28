import os
import unittest
from unittest.mock import patch, MagicMock
from daba.Mongo import collection
from dotenv import load_dotenv


class TestDb(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mongo_url = os.getenv('MONGO_URL')
        cls.mongo_db = os.getenv('MONGO_DB')

    @patch('daba.Mongo.pymongo.MongoClient')
    def test_init_db(self, mock_client):
        mock_db = MagicMock()
        mock_client.return_value.__getitem__.return_value = mock_db
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
        self.assertTrue(mock_close_db.called)

    @patch.object(collection, 'close_db')
    @patch('pymongo.collection.Collection.insert_one')
    def test_put(self, mock_insert_one, mock_close_db):
        mock_insert_one.return_value = {'_id': 'sample_id', 'data': 'sample data'}
        db_obj = collection('test')
        result = db_obj.put({'data': 'sample data'})
        self.assertEqual(result, {'_id': 'sample_id', 'data': 'sample data'})
        self.assertTrue(mock_close_db.called)

    @patch.object(collection, 'close_db')
    @patch('pymongo.collection.Collection.insert_many')
    def test_putMany(self, mock_insert_many, mock_close_db):
        mock_insert_many.return_value = [{'_id': 'sample_id', 'data': 'sample data'}]
        db_obj = collection('test')
        result = db_obj.putMany([{'data': 'sample data'}])
        self.assertEqual(result, [{'_id': 'sample_id', 'data': 'sample data'}])
        self.assertTrue(mock_close_db.called)

    @patch.object(collection, 'close_db')
    @patch('pymongo.collection.Collection.update_one')
    def test_set(self, mock_update_one, mock_close_db):
        mock_update_one.return_value = {'_id': 'sample_id', 'data': 'sample data'}
        db_obj = collection('test')
        result = db_obj.set({'condition': 'sample'}, {'$set': {'data': 'new data'}})
        self.assertEqual(result, {'_id': 'sample_id', 'data': 'sample data'})
        self.assertTrue(mock_close_db.called)

    @patch.object(collection, 'close_db')
    @patch('pymongo.collection.Collection.update_one')
    def test_inc(self, mock_update, mock_close_db):
        mock_update.return_value = {"n": 1, "nModified": 1, "ok": 1.0, 'updatedExisting': True}
        db_obj = collection('test')
        result = db_obj.inc({'Status': 1}, {'$inc': {'count': 1}})
        self.assertEqual(result, {"n": 1, "nModified": 1, "ok": 1.0, 'updatedExisting': True})
        self.assertTrue(mock_close_db.called)

    @patch.object(collection, 'close_db')
    @patch('pymongo.collection.Collection.update_many')
    def test_setMany(self, mock_update_many, mock_close_db):
        mock_update_many.return_value = {"n": 1, "nModified": 1, "ok": 1.0, 'updatedExisting': True}
        db_obj = collection('test')
        result = db_obj.setMany({'condition': 'sample'}, {'$set': {'data': 'new data'}})
        self.assertEqual(result, {"n": 1, "nModified": 1, "ok": 1.0, 'updatedExisting': True})
        self.assertTrue(mock_close_db.called)

    @patch.object(collection, 'close_db')
    @patch('pymongo.collection.Collection.find_one')
    def test_getOne(self, mock_find_one, mock_close_db):
        mock_find_one.return_value = {'_id': 'sample_id', 'data': 'sample data'}
        db_obj = collection('test')
        result = db_obj.getOne({'condition': 'sample'})
        self.assertEqual(result, {'_id': 'sample_id', 'data': 'sample data'})
        self.assertTrue(mock_close_db.called)

    @patch.object(collection, 'close_db')
    @patch('pymongo.collection.Collection.find_one_and_update')
    def test_getAfterCount(self, mock_find_one_and_update, mock_close_db):
        mock_find_one_and_update.return_value = {'_id': 'sample_id', 'count': 1}
        db_obj = collection('test')
        result = db_obj.getAfterCount({'condition': 'sample'}, 'count')
        self.assertEqual(result, {'_id': 'sample_id', 'count': 1})
        self.assertTrue(mock_close_db.called)

    @patch.object(collection, 'close_db')
    @patch('pymongo.collection.Collection.delete_one')
    def test_deleteOne(self, mock_delete_one, mock_close_db):
        mock_delete_one.return_value = {"n": 1, "ok": 1.0}
        db_obj = collection('test')
        result = db_obj.deleteOne({'condition': 'sample'})
        self.assertEqual(result, {"n": 1, "ok": 1.0})
        self.assertTrue(mock_close_db.called)

    @patch.object(collection, 'close_db')
    @patch('pymongo.collection.Collection.delete_many')
    def test_deleteMany(self, mock_delete_many, mock_close_db):
        mock_delete_many.return_value = {"n": 2, "ok": 1.0}
        db_obj = collection('test')
        result = db_obj.deleteMany({'condition': 'sample'})
        self.assertEqual(result, {"n": 2, "ok": 1.0})
        self.assertTrue(mock_close_db.called)

    @patch.object(collection, 'close_db')
    @patch('pymongo.collection.Collection.update_many')
    def test_removeElement(self, mock_update_many, mock_close_db):
        mock_update_many.return_value = {"n": 2, "nModified": 2, "ok": 1.0, 'updatedExisting': True}
        db_obj = collection('test')
        result = db_obj.removeElement({'condition': 'sample'}, {'field': 'element'})
        self.assertEqual(result, {"n": 2, "nModified": 2, "ok": 1.0, 'updatedExisting': True})
        self.assertTrue(mock_close_db.called)

    @patch.object(collection, 'close_db')
    @patch('pymongo.collection.Collection.count_documents')
    def test_count(self, mock_count_documents, mock_close_db):
        mock_count_documents.return_value = 10
        db_obj = collection('test')
        result = db_obj.count({'condition': 'sample'})
        self.assertEqual(result, 10)
        self.assertTrue(mock_close_db.called)


if __name__ == '__main__':
    load_dotenv()
    unittest.main()
