from flask import Flask
from flask_migrate import Migrate
from app.models import db
from flask_login import LoginManager
from app.models import User
from logging_config import configure_logging


login_manager = LoginManager()


def create_app(config=None):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moj.db'
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'

    configure_logging(app)

    db.init_app(app)
    login_manager.init_app(app)

    Migrate(app, db)

    from app.routes.jokes import jokes_bp
    app.register_blueprint(jokes_bp)

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.ratings import ratings_bp
    app.register_blueprint(ratings_bp)

    from routes.api_v1 import api_v1_bp
    app.register_blueprint(api_v1_bp)

    return app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))