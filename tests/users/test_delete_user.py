from typing import Callable
from flask.testing import FlaskClient

from tests.users.utils import to_dict


def test_delete_user_success_plus_one_request(
    client: FlaskClient, create_users: Callable
) -> None:
    user_data = {'name': 'John', 'email': 'doegmail.com'}
    user, = create_users([user_data])
    res = client.delete('/users/1')
    assert res.status_code == 200
    assert res.get_json() == {'user_deleted': to_dict(user)}
    res = client.delete('/users/1')
    assert res.status_code == 204
    assert res.data == b''
