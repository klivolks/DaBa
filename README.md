# daba by Klivolks

The `daba` library, developed by Klivolks, is a Python package designed to simplify the process of interacting with MongoDB databases. It provides convenient and easy-to-use methods for carrying out common database operations such as querying, inserting, updating, and deleting data.

## Installation

This package can be installed using pip:

```bash
pip install daba
```

## Environment Variables

Two environment variables need to be set:

- `MONGO_URL`: This is the URL of the MongoDB server.
- `MONGO_DB`: This is the name of the MongoDB database to interact with.

These can be set in an `.env` file that can be loaded with `python-dotenv`. Remember not to commit sensitive data (like your database URLs) to version control!

## Example usage

In this example, the `collection` class from the `daba.Mongo` module is being used to interact with a MongoDB collection. 

You can create a collection object using the `collection` method:
```python
db_obj = collection('test')
```
The `collection` object has several methods to interact with the MongoDB collection.

### Methods

Below are the methods available in the `daba` library's `collection` class, along with brief descriptions of what they do:

- `init_db()`: Initializes the MongoDB database.
- `close_db()`: Closes the MongoDB database connection.
- `get(query)`: Returns documents that match the query.
- `put(data)`: Inserts a single document into the collection.
- `putMany(data)`: Inserts multiple documents into the collection.
- `set(query, new_data)`: Updates a single document that matches the query.
- `inc(query, data_to_increment)`: Increments the value of specific fields in a document that matches the query.
- `setMany(query, new_data)`: Updates multiple documents that match the query.
- `getOne(query)`: Returns a single document that matches the query.
- `getAfterCount(query, field)`: Returns a document after incrementing the value of a specific field.
- `deleteOne(query)`: Deletes a single document that matches the query.
- `deleteMany(query)`: Deletes multiple documents that match the query.
- `removeElement(query, element)`: Removes an element from an array in the documents that match the query.
- `count(query)`: Counts the documents that match the query.

## Running Tests

This library includes a suite of unit tests. To run the tests, execute the script with a Python interpreter. Ensure the `.env` file is in the same directory as the script.

```bash
python test_daba.py
```

## Note

This README is not exhaustive, and is intended to be a brief introduction to the functionality provided by the `daba` library. For a full list of functionality and options, please refer to the official documentation.