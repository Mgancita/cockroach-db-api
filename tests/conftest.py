"""Pytest fixtures."""

import logging

from alembic import command
from alembic.config import Config
import pytest
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists
from starlette.config import environ
from starlette.testclient import TestClient

from config import apisecrets
from main import api

# This sets `os.environ`, but provides some additional protection.
# If we placed it below the application import, it would raise an error
# informing us that 'TESTING' had already been read from the environment.
environ["TESTING"] = "True"
logging.getLogger("alembic").setLevel(logging.ERROR)


@pytest.fixture(scope="module", autouse=True)
def create_test_database():
    """Create a clean database on every test case.

    For safety, we should abort if a database already exists.

    We use the `sqlalchemy_utils` package here for a few helpers in
    consistently creating and dropping the database.
    """
    # Create connection engine
    dburl = apisecrets.DATABASE_URL
    engine = create_engine(dburl)

    # Check test db
    test_dburl = apisecrets.TEST_URL
    assert not database_exists(test_dburl), "Test database already exists. Aborting tests."

    # Create test db and run migrations
    alembic_config = Config("alembic.ini")
    with engine.connect() as conn:
        conn.execute(f"CREATE DATABASE {apisecrets.TEST_DATABASE_NAME}")

        alembic_config.attributes["connection"] = conn
        command.upgrade(alembic_config, "head")
        # command.history(alembic_config, indicate_current=True)

    # Run tests
    yield

    # Drop test db
    with engine.connect() as conn:
        conn.execute(f"DROP DATABASE {apisecrets.TEST_DATABASE_NAME} CASCADE")


@pytest.fixture()
def client():
    """Create a unique client for each TestCase."""
    with TestClient(api) as client:
        yield client
