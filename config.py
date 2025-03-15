import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI: str


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('POSTGRES_URI')


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
