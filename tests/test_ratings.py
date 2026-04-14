class TestRatings:
    """Rating endpoint tests — organized by the three-level taxonomy from L7."""

    def test_create_rating(self, authenticated_client, sample_joke):
        """
        GIVEN an authenticated user and an existing joke
        WHEN they POST a valid rating to /jokes/<id>/ratings
        THEN the response should be 201 with the rating data

        Level: HAPPY PATH
        """
        payload = {
            "funniness": 4,
            "appropriateness": 5,
            "originality": 3
        }

        response = authenticated_client.post(
            f"/jokes/{sample_joke}/ratings",
            json=payload
        )

        assert response.status_code == 201

    def test_rating_boundary_values(self, authenticated_client, sample_joke):
        """
        GIVEN boundary rating values
        WHEN scores of 1 and 5 are submitted
        THEN the API should accept them

        Level: EDGE CASE
        """
        payload = {
            "funniness": 1,
            "appropriateness": 5,
            "originality": 5
        }

        response = authenticated_client.post(
            f"/jokes/{sample_joke}/ratings",
            json=payload
        )

        assert response.status_code == 201

    def test_duplicate_rating(self, authenticated_client, sample_joke):
        """
        GIVEN a user has already rated a joke
        WHEN they POST another rating
        THEN the API should return 409 conflict

        Level: ERROR CASE
        """
        payload = {
            "funniness": 4,
            "appropriateness": 4,
            "originality": 4
        }

        first_response = authenticated_client.post(
            f"/jokes/{sample_joke}/ratings",
            json=payload
        )
        assert first_response.status_code == 201

        response = authenticated_client.post(
            f"/jokes/{sample_joke}/ratings",
            json=payload
        )

        assert response.status_code == 409

    def test_rating_out_of_range(self, authenticated_client, sample_joke):
        """
        GIVEN an invalid rating value
        WHEN a score outside the range 1–5 is submitted
        THEN the API should return 400

        Level: ERROR CASE
        """
        payload = {
            "funniness": 6,
            "appropriateness": 3,
            "originality": 2
        }

        response = authenticated_client.post(
            f"/jokes/{sample_joke}/ratings",
            json=payload
        )

        assert response.status_code == 400
