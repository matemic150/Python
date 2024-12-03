"""
Test Suite for immudb Transactions API

This test suite is designed to validate the functionality of the immudb transactions API.
It includes tests for adding a transaction, retrieving data from the API, and ensuring that
the added transaction can be successfully retrieved.

Tests included:
1. test_put_data_request: Validates that a single transaction can be added successfully.
2. test_get_data_request: Ensures that data can be fetched from the API.
3. test_transaction_included: Checks if the added transaction is available in the retrieved data.

Dependencies:
- pytest: A framework that makes building simple and scalable test cases easy.
- immudb: Custom module containing functions for generating transactions and interacting with the API.
"""

import pytest
from immudb import generate_transaction, put_data_request, get_data_request, delete_collection, get_all_transaction


@pytest.fixture
def transaction():
    """
    Fixture to generate a transaction before each test.

    This function creates a new transaction object that can be used in multiple tests.
    It ensures that each test operates with a fresh transaction object, maintaining
    test isolation and preventing side effects.

    Returns:
        dict: A dictionary representing a transaction with keys such as account_number,
        account_name, iban, address, amount, and type.
    """
    return generate_transaction()


def test_put_data_request(transaction):
    """
    Test for adding a single transaction.

    This test verifies that the function responsible for adding a transaction
    returns a successful response. It uses the transaction fixture to get
    a transaction object and calls the put_data_request function.

    Asserts:
        True if the transaction is stored successfully, otherwise raises an AssertionError.
    """
    response = put_data_request(transaction)

    assert response is True, "Transaction not stored successfully."


def test_get_data_request():
    """
    Test for fetching data from the API.

    This test checks if the API returns data correctly. It retrieves the current
    data from the API and verifies that the 'revisions' key is present in the response.

    Asserts:
        True if the 'revisions' key exists in the fetched data, otherwise raises an AssertionError.
    """
    current_data = get_data_request()
    assert current_data.get('revisions') is not None, "Failed to fetch data from API."

def test_transaction_overwriting(transaction):
    """
    Test for overwriting a transaction's amount.

    This test verifies that an existing transaction in the vault can be updated (overwritten).
    Initially, a transaction is added to the vault with a certain 'amount'. Then, the same
    transaction's 'amount' is updated to a new value (999) using the update method.

    The test checks if the updated transaction with the modified 'amount' is present
    in the current data returned by the API.

    Asserts:
        True if the transaction with the updated 'amount' (999) exists, otherwise raises an AssertionError.
    """
    put_data_request(transaction)
    put_data_request(transaction.update({'amount': 999}))
    assert any(i.get('account_number') == transaction['account_number'] and i.get('amount') == 999 for i in get_all_transaction())\
        , "Transaction not found in current data."

def test_transaction_included_not_empty_vault(transaction):
    """
    Test for verifying transaction inclusion in a non-empty vault.

    This test ensures that when a transaction is inserted into an already populated vault,
    it is correctly included in the list of transactions.

    Steps:
        1. Insert the same transaction twice using `put_data_request`.
        2. Retrieve all transactions using `get_all_transaction`.
        3. Verify that the inserted transaction exists in the vault.

    Asserts:
        True if the transaction with the correct account number is found,
        otherwise raises an AssertionError with the message "Transaction not found in current data."
    """
    put_data_request(generate_transaction())
    put_data_request(transaction)
    assert any(i.get('account_number') == transaction['account_number'] for i in get_all_transaction())\
        , "Transaction not found in current data."

def test_transaction_included_empty_vault(transaction):
    """
    Test for verifying transaction inclusion in an empty vault.

    This test checks if a transaction is properly added and retrieved when the vault is initially empty.

    Steps:
        1. Clear the vault using `delete_collection`.
        2. Insert a new transaction using `put_data_request`.
        3. Retrieve all transactions using `get_all_transaction`.
        4. Verify that the inserted transaction exists in the vault.

    Asserts:
        True if the transaction with the correct account number is found,
        otherwise raises an AssertionError with the message "Transaction not found in current data."
    """
    delete_collection()
    put_data_request(transaction)
    assert any(i.get('account_number') == transaction['account_number'] for i in get_all_transaction())\
        , "Transaction not found in current data."


def test_110_transaction_included_not_empty_vault(transaction):
    """
    Test for verifying batch transaction inclusion in a non-empty vault.

    This test ensures that when a batch of 111 transactions is inserted into a non-empty vault,
    a specific transaction (100th in the batch) is correctly included.

    Steps:
        1. Insert a single transaction to simulate a non-empty vault using `put_data_request`.
        2. Generate a batch of 111 transactions and insert them into the vault.
        3. Retrieve all transactions using `get_all_transaction`.
        4. Verify that the 100th transaction in the batch exists in the vault.

    Asserts:
        True if the 100th transaction is found, otherwise raises an AssertionError
        with the message "Transaction not found in current data."
    """
    put_data_request(transaction)
    transaction_list = [generate_transaction() for _ in range(110)]
    put_data_request(transaction_list)
    assert any(i.get('account_number') == transaction_list[99]['account_number'] for i in get_all_transaction())\
        , "Transaction not found in current data."


def test_110_transaction_included_empty_vault():
    """
    Test for verifying batch transaction inclusion in an empty vault.

    This test ensures that when the vault is empty and a batch of 111 transactions is inserted,
    a specific transaction (100th in the batch) is correctly included.

    Steps:
        1. Clear the vault using `delete_collection`.
        2. Generate a batch of 111 transactions and insert them into the vault using `put_data_request`.
        3. Retrieve all transactions using `get_all_transaction`.
        4. Verify that the 100th transaction in the batch exists in the vault.

    Asserts:
        True if the 100th transaction is found, otherwise raises an AssertionError
        with the message "Transaction not found in current data."
    """
    delete_collection()
    transaction_list = [generate_transaction() for _ in range(110)]
    put_data_request(transaction_list)
    assert any(i.get('account_number') == transaction_list[99]['account_number'] for i in get_all_transaction())\
        , "Transaction not found in current data."



