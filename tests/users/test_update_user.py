from typing import Callable
import pytest
from flask.testing import FlaskClient

from tests.users.utils import to_dict


@pytest.mark.parametrize(
    'user_data', [
        {'name': 'John', 'email': 'test123@gmail.com'},
        {'name': 'Jane', 'email': 'doe@gmail.com'},
    ]
)
def test_update_user_success(
    client: FlaskClient, create_users: Callable, user_data: dict
) -> None:
    user, = create_users([{'name': 'John', 'email': 'doe@gmail.com'}])
    res = client.put('/users/1', json=user_data)
    assert res.status_code == 200
    assert res.get_json() == {
        'user_updated': to_dict(user) | user_data
    }


@pytest.mark.parametrize(
    'user_data', [
        {'name': 'John', 'email': 'doegmail.com'},
        {'name': 'John', 'email': 'doe@gmailcom'},
        {'name': 'John', 'email': ' doe@gmail.com '},
    ]
)
def test_update_user_error_email_invalid(
    client: FlaskClient, create_users: Callable, user_data: dict
) -> None:
    create_users([{'name': 'John', 'email': 'doe@gmail.com'}])
    res = client.put('/users/1', json=user_data)
    assert res.status_code == 422
    assert res.get_json() == {
        'error': {'email': ['Not a valid email address.']}
    }


def test_update_user_error_email_exists(
    client: FlaskClient, create_users: Callable
) -> None:
    first_user_data = {'name': 'John', 'email': 'doe@gmail.com'}
    second_user_data = {'name': 'Jane', 'email': 'test123@gmail.com'}
    create_users([first_user_data, second_user_data])
    res = client.put(
        '/users/2', json=second_user_data | {'email': first_user_data['email']}
    )
    assert res.status_code == 422
    assert res.get_json() == {'error': 'Email already exists'}
