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