from typing import Callable
import pytest
from flask.testing import FlaskClient

from app.models import db, User


@pytest.mark.parametrize(
    'user_data', [
        {'name': 'John', 'email': 'doe@gmail.com'},
        {'name': 'john', 'email': 'doe@gmail.com'},
        {'name': 'JOHN', 'email': 'doe@gmail.com'},
    ]
)
def test_create_user_success(client: FlaskClient, user_data: dict) -> None:
    res = client.post('/users/', json=user_data)
    assert res.status_code == 201
    assert res.get_json() == {
        'user_created': {
            'id': 1,
            'created_at': db.session.get(User, 1).created_at.isoformat(),
            'name': user_data['name'].title(),
            'email': user_data['email']
        }
    }


@pytest.mark.parametrize(
    'user_data', [
        {'name': 'John', 'email': 'doegmail.com'},
        {'name': 'John', 'email': 'doe@gmailcom'},
        {'name': 'John', 'email': ' doe@gmail.com '},
    ]
)
def test_create_user_error_email_invalid(
    client: FlaskClient, user_data: dict
) -> None:
    res = client.post('/users/', json=user_data)
    assert res.status_code == 422
    assert res.get_json() == {
        'error': {'email': ['Not a valid email address.']}
    }


def test_create_user_error_email_exists(
    client: FlaskClient, create_users: Callable
) -> None:
    user_data = {'name': 'John', 'email': 'doe@gmail.com'}
    create_users([user_data])
    res = client.post('/users/', json=user_data)
    assert res.status_code == 422
    assert res.get_json() == {'error': 'Email already exists'}
