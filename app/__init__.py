from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import config

db = SQLAlchemy()  # 전역 변수로 db와 migrate를 만들어서 -> 뒤에 #ORM 에서 app객체와 이어줌 
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)   # config.py 파일에 작성한 내용을 app.config 환경 변수로 부르기 위한 코드

    # ORM
    db.init_app(app)    # SQLAlchemy의 객체 db와 migrate객체를 app 객체와 이어줌
    migrate.init_app(app, db)    # db 객체를 create_app 함수 안에서 생성하면 블루프린트와 같은 다른 모듈에서 불러올 수 없음. 따라서 db, migrate와 같은 객체를 create 함수 밖에서 생성하고, 실제 객체 초기화는 create_app 함수에서 수행함
    from . import models    # migrate객체가 models.py파일을 참조하게 함 

    # 블루프린트
    from .views import book_api, user_api
    app.register_blueprint(user_api.user)
    app.register_blueprint(book_api.book)

    app.secret_key = "elice"
    app.config['SESSION_TYPE'] = 'filesystem'

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=5000)