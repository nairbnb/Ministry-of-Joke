import pytest
from app import create_app
from app.models import db as _db


@pytest.fixture(scope='function')
def app():
    application = create_app()

    with application.app_context():
        _db.create_all()
        yield application
        _db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    return app.test_client()
