class TestJokeCountEndpoint:
    """Tests for GET /api/v1/jokes/count"""

    def test_joke_count_returns_200(self, client):
        """
        GIVEN an application with the API v1 blueprint registered
        WHEN the client sends GET /api/v1/jokes/count
        THEN the response status code should be 200

        Level: HAPPY PATH
        """
        response = client.get('/api/v1/jokes/count')
        assert response.status_code == 200

    def test_joke_count_returns_envelope(self, client):
        """
        GIVEN an application with jokes in the database
        WHEN the client sends GET /api/v1/jokes/count
        THEN the response body should contain 'data' with an integer 'count' and 'status' == 'ok'

        Level: HAPPY PATH
        """
        response = client.get('/api/v1/jokes/count')
        body = response.get_json()
        assert body["status"] == "ok"
        assert isinstance(body["data"]["count"], int)

    def test_joke_count_zero_when_empty(self, client):
        """
        GIVEN an application with no jokes in the database
        WHEN the client sends GET /api/v1/jokes/count
        THEN the response should return count == 0 (not null, not an error)

        Level: EDGE CASE
        """
        response = client.get('/api/v1/jokes/count')
        body = response.get_json()

        assert response.status_code == 200
        assert body["status"] == "ok"
        assert body["data"]["count"] == 0

    def test_joke_count_wrong_method_returns_405(self, client):
        """
        GIVEN the endpoint only allows GET requests
        WHEN the client sends POST /api/v1/jokes/count
        THEN the response status code should be 405 Method Not Allowed

        Level: ERROR CASE
        """
        response = client.post('/api/v1/jokes/count')

        assert response.status_code == 405