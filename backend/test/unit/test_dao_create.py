import pytest
from pymongo import MongoClient
from pymongo.errors import WriteError
from src.util.dao import DAO

@pytest.fixture
def test_dao():
    """Fixture to create a test DAO with a test collection."""
    client = MongoClient('mongodb://localhost:27017/')
    test_db = client['test_database']
    test_collection = test_db['test_collection']

    dao = DAO()
    dao.collection = test_collection

    yield dao

    test_db.drop_collection('test_collection')
    client.close()

def test_create_success(test_dao):
    valid_data = {"name": "John Doe", "is_active": True}
    result = test_dao.create(valid_data)
    assert result["name"] == "John Doe"
    assert result["is_active"] is True
    assert "_id" in result

def test_create_missing_required_field(test_dao):
    invalid_data = {"is_active": True}
    with pytest.raises(WriteError):
        test_dao.create(invalid_data)

def test_create_wrong_data_type(test_dao):
    invalid_data = {"name": "John Doe", "is_active": "yes"}
    with pytest.raises(WriteError):
        test_dao.create(invalid_data)

def test_create_unique_constraint_violation(test_dao):
    valid_data = {"name": "UniqueName", "is_active": True}
    test_dao.create(valid_data)
    
    duplicate_data = {"name": "UniqueName", "is_active": False}
    with pytest.raises(WriteError):
        test_dao.create(duplicate_data)