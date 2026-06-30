import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_jokes_returns_empty_list(client):
    """
    GIVEN a fresh MoJ application with no jokes submitted
    WHEN a GET request is made to /jokes
    THEN the response is 200 OK and the jokes list is empty

    Level: HAPPY PATH
    """
    response = client.get('/jokes')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'
    assert data['data']['jokes'] == []


def test_submit_joke_valid(client):
    """
    GIVEN a running MoJ application
    WHEN a POST request is made to /jokes with valid non-empty text
    THEN the response should be 201 Created

    Level: HAPPY PATH
    """
    
    pass


def test_submit_joke_max_length(client):
    """
    GIVEN a running MoJ application
    WHEN a POST request is made to /jokes with text exactly 500 characters long
    THEN the response should be 201 Created

    Level: EDGE CASE
    """
    pass


def test_submit_joke_empty_text(client):
    """
    GIVEN a running MoJ application
    WHEN a POST request is made to /jokes with an empty string as the text field
    THEN the response should be 400 Bad Request

    Level: ERROR CASE
    """
    pass


def test_submit_joke_over_max_length(client):
    """
    GIVEN a running MoJ application
    WHEN a POST request is made to /jokes with text of 501 characters
    THEN the response should be 400 Bad Request

    Level: EDGE CASE
    """
    pass


def test_submit_joke_whitespace_only(client):
    """
    GIVEN a running MoJ application
    WHEN a POST request is made to /jokes with text consisting entirely of whitespace
    THEN the response should be 400 Bad Request

    Level: EDGE CASE
    """
    pass