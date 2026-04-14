from flask import Blueprint, request, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({'error': 'Username already exists'}), 409
    user = User(username=data.get('username'))
    user.set_password(data.get('password'))
    db.session.add(user)
    db.session.commit()
    return jsonify({'username': user.username}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        current_app.logger.warning(
            "Login failed",
            extra={
                "event": "login_failure",
                "attempted_username": data.get('username') if data else None,
                "endpoint": "POST /login",
                "status_code": 400
            }
        )
        return jsonify({'error': 'Bad Request: Missing credentials'}), 400
    user = User.query.filter_by(username=data.get('username')).first()
    if user is None or not user.check_password(data.get('password', '')):
        current_app.logger.warning(
            "Login failed",
            extra={
                "event": "login_failure",
                "attempted_username": data.get('username'),
                "endpoint": "POST /login",
                "status_code": 401
            }
        )
        return jsonify({'error': 'Invalid credentials'}), 401
    login_user(user)
    current_app.logger.info(
        "Login successful",
        extra={
            "event": "login_success",
            "user_id": user.id,
            "endpoint": "POST /login",
            "status_code": 200
        }
    )
    return jsonify({'message': f'Welcome, {user.username}'}), 200


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out'}), 200


@auth_bp.route('/admin/users', methods=['GET'])
@login_required
def list_users():
    """List all registered users. Admin only."""
    if current_user.role != 'admin':
        return jsonify({'error': 'Forbidden'}), 403
    users = User.query.all()
    return jsonify(
        [{'id': u.id, 'username': u.username, 'role': u.role} for u in users])