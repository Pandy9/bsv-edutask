import pytest
from unittest.mock import MagicMock, patch
from src.controllers.usercontroller import UserController

@pytest.fixture
def controller():
    mock_dao = MagicMock()
    return UserController(dao=mock_dao)

def test_get_user_by_email_single_user(controller):
    mock_user = {'email': 'user@example.com'}
    controller.dao.find.return_value = [mock_user]

    result = controller.get_user_by_email('user@example.com')
    assert result == mock_user

def test_get_user_by_email_multiple_users(controller):
    mock_user1 = {'email': 'user@example.com'}
    mock_user2 = {'email': 'user@example.com'}
    controller.dao.find.return_value = [mock_user1, mock_user2]

    with patch("builtins.print") as mock_print:
        result = controller.get_user_by_email('user@example.com')
        assert result == mock_user1
        mock_print.assert_called_with("Error: more than one user found with mail user@example.com")

def test_get_user_by_email_no_users(controller):
    controller.dao.find.return_value = []

    result = controller.get_user_by_email('user@example.com')
    assert result is None

def test_get_user_by_email_invalid_email(controller):
    with pytest.raises(ValueError, match="invalid email address"):
        controller.get_user_by_email("invalid-email")

def test_get_user_by_email_dao_exception(controller):
    controller.dao.find.side_effect = Exception("DB failure")

    with pytest.raises(Exception, match="DB failure"):
        controller.get_user_by_email("user@example.com")
