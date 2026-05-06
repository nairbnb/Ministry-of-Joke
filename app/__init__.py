from flask import Flask

def create_app():
    """
    웹 서버 애플리케이션 객체
    app 객체가 실행되면서 포트를 점유하고,
    브라우저의 요청을 기다리는 역할을 수행한다.
    """
    app = Flask(__name__)

    from app.routes.jokes import jokes_bp
    """
    하위 객체에서 열심히 만든 
    blueprint 객체 여기서 등록!
    """
    app.register_blueprint(jokes_bp)

    return app
