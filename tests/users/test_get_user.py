import pytest
from typing import Callable
from flask.testing import FlaskClient

from tests.users.utils import to_dict


@pytest.mark.parametrize(
    'dataset', [
        [],
        [{'name': 'John', 'email': 'test@gmail.py'}],
    ]
)
def test_get_user_not_found(
    client: FlaskClient, create_users: Callable, dataset: list[dict]
) -> None:
    if dataset:
        create_users(dataset)
    res = client.get('/users/2')
    assert res.status_code == 404
    assert res.get_json() == {'error': 'User not found'}


@pytest.mark.parametrize(
    'dataset', [
        [{'name': 'John', 'email': 'test@gmail.py'}],
        [
            {'name': 'John', 'email': 'test@gmail.py'},
            {'name': 'Jane', 'email': 'test2@gmail.com'}
        ],
    ]
)
def test_get_user_found(
    client: FlaskClient, create_users: Callable, dataset: list[dict]
) -> None:
    user = create_users(dataset)[0]
    res = client.get(f'/users/{user.id}')
    assert res.status_code == 200
    assert res.get_json() == {'user': to_dict(user)}
