from typing import Callable
import pytest

from app.models import User, db


@pytest.fixture
def create_users() -> Callable:
    def inner(dataset: list[dict]) -> list[User]:
        users = []
        for user_data in dataset:
            user = User(**user_data)
            db.session.add(user)
            users.append(user)
        db.session.commit()
        return users
    return inner
