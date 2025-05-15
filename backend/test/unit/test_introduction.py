import pytest
import unittest.mock as mock
from src.controllers.usercontroller import UserController

def test_invalid_email_raises_value_error():
    invalid_email = 'invalidemail.com'

    mock_dao = mock.MagicMock()
    controller = UserController(dao=mock_dao)

    with pytest.raises(ValueError, match="Error: invalid email address") as e_info:
        controller.get_user_by_email(invalid_email)

    assert str(e_info.value) == 'Error: invalid email address'


def test_valid_email_returns_one_user_true():
    user1 = {'email': 'valid@email.com'}

    mock_dao = mock.MagicMock()
    mock_dao.find.return_value = [user1]

    controller = UserController(dao=mock_dao)
    result = controller.get_user_by_email('valid@email.com')

    assert result == user1


def test_valid_email_multiple_users_true():
    user1 = {'email': 'duplicate@email.com'}
    user2 = {'email': 'duplicate@email.com'}
    user3 = {'email': 'duplicate@email.com'}

    mock_dao = mock.MagicMock()
    mock_dao.find.return_value = [user1, user2, user3]

    controller = UserController(dao=mock_dao)
    result = controller.get_user_by_email('duplicate@email.com')

    assert result == user1
    

def test_valid_email_no_user_true():
    mock_dao = mock.MagicMock()
    mock_dao.find.return_value = []

    controller = UserController(dao=mock_dao)
    result = controller.get_user_by_email('usinglongemailthatdoesnotexist@mail.com')

    assert result is None


def test_valid_email_db_error_true():
    email = 'valid@email.com'

    mock_dao = mock.MagicMock()
    mock_dao.find.side_effect = Exception("Database error")

    controller = UserController(dao=mock_dao)
    with pytest.raises(Exception, match="Database error") as e_info:
        controller.get_user_by_email(email)