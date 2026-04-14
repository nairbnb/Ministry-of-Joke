import pytest
from app import create_app
from app.models import db as _db, User, Joke


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.logger.propagate = True
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def authenticated_client(client, app):
    """Returns a test client logged in as a joke-teller."""
    with app.app_context():
        user = User(username='testuser')
        user.set_password('testpass')
        _db.session.add(user)
        _db.session.commit()
        client.post('/login', json={
            'username': 'testuser',
            'password': 'testpass'
        })
    return client


@pytest.fixture
def sample_joke(app):
    """Creates a joke in the test database and returns its id."""
    with app.app_context():
        user = User(username='jokeauthor')
        user.set_password('testpass')
        _db.session.add(user)
        _db.session.commit()
        joke = Joke(text="Test joke", submitted_by=user.id)
        _db.session.add(joke)
        _db.session.commit()
        return joke.id