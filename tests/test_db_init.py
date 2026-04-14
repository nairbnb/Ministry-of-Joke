import pytest
from app import create_app
from app.models import db as _db


@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


def test_db_initializes(app):
    """
    GIVEN a configured Flask application
    WHEN the app context is active
    THEN the database should be accessible without error

    Level: HAPPY PATH
    """
    with app.app_context():
        from app.models import User, Joke
        assert User.__tablename__ == 'user'
        assert Joke.__tablename__ == 'joke'