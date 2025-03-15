import pytest
from typing import Generator
from flask import Flask
from flask.testing import FlaskClient

from app.models import db
from create_app import create_app
from config import TestConfig


@pytest.fixture
def app() -> Generator[Flask, None, None]:
    app = create_app(config=TestConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()
