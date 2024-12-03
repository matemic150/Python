"""
Transaction Management API with immudb

This module is designed to interact with the immudb database for handling transactions.
It provides functions for generating transactions, adding them to the database, retrieving
all transactions, and deleting collections.

Functions included:
1. generate_transaction: Generates a fake transaction with random data.
2. put_data_request: Sends a transaction or a list of transactions to the immudb database.
3. get_data_request: Retrieves stored transaction data from the immudb database.
4. delete_collection: Deletes the entire collection of documents in the immudb database.
5. get_all_transaction: Retrieves all transactions from the immudb database.

Dependencies:
- requests: A module used to send HTTP requests to the immudb API.
- faker: A module to generate fake data for testing.
- immudb: The immudb API platform where the transactions are stored and managed.
"""

from faker import Faker
import requests
from faker.generator import random

fake = Faker()

APIKey = 'default.NBw3gy9WWSmIXhrrkCxnKw.vw1fnvIKEp6hBxd5JPqwYVWKgtUHzpLeTGSCbO9XkmIFNU1t'

def generate_transaction():
    """
    Generates a fake transaction.

    This function uses the `Faker` library to generate a fake transaction with the following keys:
    - account_number: A 26-digit random number.
    - account_name: A randomly generated username.
    - iban: A random IBAN number.
    - address: A fake address.
    - amount: A random amount between 1 and 10,000, rounded to two decimal places.
    - type: A random transaction type, either 'sending' or 'receiving'.

    Returns:
        dict: A dictionary representing the transaction.
    """
    data = {
        'account_number': str(fake.random_number(digits=26, fix_len=True)),
        'account_name': fake.user_name(),
        'iban': fake.iban(),
        'address': fake.address(),
        'amount': round(random.uniform(1.0, 10000.0), 2),
        'type': random.choice(('sending', 'receiving'))
    }
    return data

def put_data_request(data):
    """
    Sends transaction data to immudb.

    This function sends either a single transaction or a list of transactions to the immudb
    database using an HTTP PUT request.

    Args:
        data (dict or list): A single transaction (as a dict) or a list of transactions.

    Returns:
        bool: True if the data was successfully added, False otherwise.
    """
    if isinstance(data, list):
        data = {
            'document': data
        }
    url = 'https://vault.immudb.io/ics/api/v1/ledger/default/collection/default/document'
    response = requests.put(url, headers={'accept': 'application/json', 'X-API-Key': APIKey, 'Content-Type': 'application/json'}
                            , json=data)
    if response.status_code == 200:
        return True
    else:
        return False

def get_data_request():
    """
    Retrieves transaction data from immudb.

    This function sends a POST request to immudb to retrieve transaction data.
    It requests a maximum of 100 documents per page from the API.

    Returns:
        dict: The retrieved data in JSON format.
    """
    url = 'https://vault.immudb.io/ics/api/v1/ledger/default/collection/default/documents/search'

    headers = {
        'accept': 'application/json',
        'X-API-Key': APIKey
    }
    data = {
        "page": 1,
        "perPage": 100
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return response.json()


def delete_collection():
    """
    Deletes the entire collection in immudb.

    This function sends a DELETE request to immudb to remove all documents
    in the default collection.

    Returns:
        bool: True if the collection was successfully deleted, False otherwise.
    """
    # url = "https://vault.immudb.io/v1/ledger/default/collection/default"
    url = 'https://vault.immudb.io/ics/api/v1/ledger/default/collection/default'

    headers = {
        'Accept': 'application/json',
        "Authorization": f'Bearer {APIKey}',
        'X-API-Key': APIKey
    }

    response = requests.delete(url, headers=headers)
    print(response)
    if response.status_code == 200:
        return True
    else:
        print("Error:", response.status_code, response.text)
        return False


def get_all_transaction():
    """
    Retrieves all transactions stored in immudb.

    This function calls the `get_data_request()` to fetch all documents in the collection.
    It then processes the documents and extracts transaction details from them.

    Returns:
        list: A list of all transaction dictionaries.
    """
    current_data = get_data_request()
    revision = current_data.get('revisions')
    all_doc = []
    for document in revision:
        if 'document' in document.get('document').keys():
            for inside_doc in document.get('document').get('document'):
                all_doc.append(inside_doc)
        else:
            all_doc.append(document.get('document'))
    return all_doc