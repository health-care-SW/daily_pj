from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy() # 추가
migrate = Migrate() # 추가

def create_app():
    app = Flask(__name__)

    # 추가
    # config.py 파일에 작성한 항목을 읽기 위함
    app.config.from_object(config)

    #ORM 추가
    # db와 migrate 객체를 app에 등록
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models # 작성한 모델을 migrate 기능이 인식하려면 inmport가 필요

    from .views import main_views, question_views, answer_views, auth_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)

    return app