import pytest
from app import create_app

"""
pytest 에게 "이 함수는 테스트에 필요한 공통 준비물(fixture)이야" 
라고 알려주는 Decorator.
"""
@pytest.fixture
def client():
    app = create_app()
    """
    config : Flask 객체 app 이 가지고 있는 설정 관리 객체
    config['TESTING'] 설정이 True 가 되면 Flask의 내부 동작이
    테스트에 적합하게 몇 가지 바뀐다.
    1. 에러 핸들링 중단
    - 에러를 내부적으로 숨기지 않고 pytest 에 그대로 던져준다.
    2. 확장 기능의 동작 변경
    - Flask 라이브러리들이 테스트중이라고 판단해서 실제로
      메일을 보내거나 하지 않고 더미 데이터를 사용하는 등 
      테스트용 동작을 수행한다.
    """
    app.config['TESTING'] = True
    """
    with : 
    파이썬의 Context Manager,
    이 블록이 끝나면 세션이나 리소스를 
    자동으로 닫아주는 Clean-up 역할을 한다.
    app.test_client() :
    실제 서버 없이 Flask 내부 엔진에 HTTP 요청을 
    보낼 수 있는 가상 클라이언트를 생성
    _as client :
    with 문을 통해 생성된 객체에 이름을 붙여주는 과정
    yield vs return :
    return 은 값을 주고 함수를 완전히 끝낸다.
    yield 는 값을 테스트 함수로 전달한 뒤,
    테스트가 끝나면 다시 이 코드로 돌아와 
    yield 뒷부분을 실행한다.
    """
    with app.test_client() as client:
        yield client

"""
함수 이름이 test_ 로 시작하면 pytest 가 자동으로 
테스트 함수로 인식한다.
"""
def test_get_jokes_returns_empty_list(client):
    """
    BDD(Behavior Driven Development) Pattern:

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