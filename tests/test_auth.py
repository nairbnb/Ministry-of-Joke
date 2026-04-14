from app.models import db, User


def test_register_new_user_valid_credentials(client, app):
    """
    GIVEN a valid username and password
    WHEN POST /register
    THEN response is 201 Created
        AND user exists in the database with role 'joke-teller'

    Level: HAPPY PATH
    """
    response = client.post("/register", json={
        "username": "newuser",
        "password": "password123"
    })

    assert response.status_code == 201

    with app.app_context():
        user = User.query.filter_by(username="newuser").first()
        assert user is not None
        assert user.role == "joke-teller"


def test_register_username_already_exist(client, app):
    """
    GIVEN a username that already exists
    WHEN POST /register with the same username
    THEN response is 409 Conflict

    Level: EDGE CASE
    """
    with app.app_context():
        user = User(username="dupuser")
        user.set_password("pass")
        db.session.add(user)
        db.session.commit()

    response = client.post("/register", json={
        "username": "dupuser",
        "password": "pass"
    })

    assert response.status_code == 409


def test_access_get_admin_users_as_joke_teller(authenticated_client):
    """
    GIVEN a logged-in user with role 'joke-teller'
    WHEN GET /admin/users
    THEN response is 403 Forbidden

    Level: ERROR CASE
    """
    response = authenticated_client.get("/admin/users")
    assert response.status_code == 403


def test_access_get_admin_users_without_logging_in(client):
    """
    GIVEN no logged-in user
    WHEN GET /admin/users
    THEN response is 401 Unauthorized (NOT 403, NOT 500)

    Level: ERROR CASE (SECURITY)
    """
    response = client.get("/admin/users")
    assert response.status_code == 401


def test_login_missing_fields(client):
    """
    GIVEN a running application
    WHEN an attacker POSTs to /login with empty JSON {}
    THEN the response is 400 Bad Request
    """
    response = client.post('/login', json={})
    assert response.status_code == 400
