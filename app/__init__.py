from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.routes.jokes import jokes_bp
    app.register_blueprint(jokes_bp)

    return app
