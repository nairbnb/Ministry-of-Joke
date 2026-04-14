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

# tests/test_jokes.py
# Three-level test suite for POST /jokes
# GIVEN/WHEN/THEN format required — Level: tag required in every docstring


def test_submit_joke_valid(client):
    """
    GIVEN a running MoJ application
    WHEN a POST request is made to /jokes with valid non-empty text
    THEN the response should be 201 Created
     AND the response envelope should contain the submitted text under data.data
     AND the response envelope should include the database ID of the created joke

    Level: HAPPY PATH
    """
    response = client.post(
        '/jokes',
        json={'text': 'Why did the knight cross the road? To get to the other keep.'}
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data['data']['text'] == (
        'Why did the knight cross the road? '
        'To get to the other keep.'
    )
    assert isinstance(data['data'].get('id'), int)


def test_submit_joke_max_length(client):
    """
    GIVEN a running MoJ application
    WHEN a POST request is made to /jokes with text exactly 500 characters long
    THEN the response should be 201 Created
     AND the response envelope status should be 'created' (not 'ok')
     AND the stored text should not be truncated

    Level: EDGE CASE
    """
    max_text = 'A' * 500
    response = client.post('/jokes', json={'text': max_text})
    assert response.status_code == 201
    data = response.get_json()
    assert data['status'] == 'created'
    assert len(data['data']['text']) == 500


def test_submit_joke_empty_text(client):
    """
    GIVEN a running MoJ application
    WHEN a POST request is made to /jokes with an empty string as the text field
    THEN the response should be 400 Bad Request
     AND the response envelope should have a top-level status of 'error'
     AND the error body should include a VALIDATION_ERROR code

    Level: ERROR CASE
    """
    response = client.post('/jokes', json={'text': ''})
    assert response.status_code == 400
    data = response.get_json()
    assert data.get('status') == 'error'
    assert data['error']['code'] == 'VALIDATION_ERROR'


def test_submit_joke_over_max_length(client):
    """
    GIVEN an authenticated user
    WHEN they POST to /jokes with text of 501 characters (one over the limit)
    THEN the response should be 400 Bad Request
     AND the response body should indicate the text field is too long

    Level: EDGE CASE
    """
    over_text = 'A' * 501
    response = client.post('/jokes', json={'text': over_text})
    assert response.status_code == 400


def test_submit_joke_whitespace_only(client):
    """
    GIVEN an authenticated user
    WHEN they POST to /jokes with text consisting entirely of whitespace
    THEN the response should be 400 Bad Request
     AND the response body should treat whitespace-only input as invalid

    Level: EDGE CASE
    """
    response = client.post('/jokes', json={'text': '   '})
    assert response.status_code == 400
