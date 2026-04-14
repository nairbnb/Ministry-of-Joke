import logging


class TestLogging:
    """Verify that MoJ route handlers emit structured log events."""

    def test_login_emits_log_event(self, client, caplog):
        """
        GIVEN a registered user
        WHEN they POST valid credentials to /login
        THEN an INFO log entry with event 'login_success' should be emitted

        Level: HAPPY PATH
        """
        client.post('/register', json={
            'username': 'loguser',
            'password': 'logpass123'
        })

        with caplog.at_level(logging.INFO, logger='app'):
            client.post('/login', json={
                'username': 'loguser',
                'password': 'logpass123'
            })

        assert any(
            record.levelname == "INFO" and
            hasattr(record, "event") and
            record.event == "login_success"
            for record in caplog.records
        )

    def test_login_failure_emits_warning(self, client, caplog):
        """
        GIVEN a registered user
        WHEN they POST invalid credentials to /login
        THEN a WARNING log entry with event 'login_failure' should be emitted

        Level: ERROR CASE
        """
        with caplog.at_level(logging.WARNING, logger='app'):
            client.post('/login', json={
                'username': 'nobody',
                'password': 'wrongpass'
            })

        assert any(
            record.levelname == "WARNING" and
            hasattr(record, "event") and
            record.event == "login_failure"
            for record in caplog.records
        )

    def test_rating_created_emits_log_event(self, client, app, caplog):
        """
        GIVEN an authenticated user and an existing joke
        WHEN they POST a valid rating
        THEN an INFO log entry with event 'rating_created' and joke_id field
        should be emitted

        Level: HAPPY PATH
        """
        from app.models import db, Joke, User

        client.post('/register', json={
            'username': 'ratingloguser',
            'password': 'logpass123'
        })
        client.post('/login', json={
            'username': 'ratingloguser',
            'password': 'logpass123'
        })

        with app.app_context():
            user = User.query.filter_by(username='ratingloguser').first()
            joke = Joke(text='Why did the log fail?', submitted_by=user.id)
            db.session.add(joke)
            db.session.commit()
            joke_id = joke.id

        with caplog.at_level(logging.INFO, logger='app'):
            client.post(f'/jokes/{joke_id}/ratings', json={
                'funniness': 4,
                'appropriateness': 3,
                'originality': 5
            })

        assert any(
            record.levelname == "INFO" and
            hasattr(record, "event") and
            record.event == "rating_created" and
            hasattr(record, "joke_id")
            for record in caplog.records
        )