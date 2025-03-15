import pytest
from typing import Callable
from flask.testing import FlaskClient

from tests.users.utils import to_dict


@pytest.mark.parametrize(
    'dataset', [
        [],
        [{'name': 'John', 'email': 'test@gmail.py'}],
        [
            {'name': 'John', 'email': 'test@gmail.py'},
            {'name': 'Jane', 'email': 'test2@gmail.com'}
        ],
    ]
)
def test_get_users_success(
    client: FlaskClient, create_users: Callable, dataset: list[dict]
) -> None:
    users = create_users(dataset) if dataset else []
    res = client.get('/users/')
    assert res.status_code == 200
    assert res.get_json() == {
        'users': [to_dict(user, fields=['id', 'name']) for user in users]
    }
