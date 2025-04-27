import pytest

from pymongo.errors import WriteError
from pymongo.errors import DuplicateKeyError
from src.util.dao import DAO

from dotenv import load_dotenv
load_dotenv()

@pytest.fixture
def test_dao():    
    dao_instance = DAO('user')
    
    yield dao_instance
    dao_instance.collection.delete_many({})

def test_correct_input_true(test_dao):
    data = {'firstName': 'Test', 'lastName': 'Testsson', 'email': 'test@mail.com'}
    result = test_dao.create(data)

    assert '_id' in result
    assert result['firstName'] == 'Test'
    assert result['lastName'] == 'Testsson'
    assert result['email'] == 'test@mail.com'

def test_no_input(test_dao):
    data = {}
    with pytest.raises(WriteError) as e_info:
        test_dao.create(data)
    
    assert "Document failed validation" in str(e_info.value)

def test_integer_input(test_dao):
    data = 123

    with pytest.raises(TypeError) as e_info:
        test_dao.create(data)

    assert "not iterable" in str(e_info.value)

def test_non_unique_input(test_dao):
    data = {'firstName': 'Duplicate', 'lastName': 'Duplicatesson', 'email': 'duplicate@mail.com'}
    test_dao.create(data)

    with pytest.raises(WriteError) as e_info:
        test_dao.create(data)

    assert "more than one user found with mail" in str(e_info.value)