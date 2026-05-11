from flask import Flask
from flask_migrate import Migrate
from app.models import db


def create_app():

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moj.db'

    db.init_app(app)
    migrate = Migrate(app, db)

    from app.routes.jokes import jokes_bp
    app.register_blueprint(jokes_bp)

    return app