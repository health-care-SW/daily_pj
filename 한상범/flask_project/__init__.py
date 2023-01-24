from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy() # 추가
migrate = Migrate() # 추가

def create_app():
    app = Flask(__name__)

    app.config.from_object(config)


    db.init_app(app)
    migrate.init_app(app, db)
    from . import models # 작성한 모델을 migrate 기능이 인식하려면 inmport가 필요

    from .views import main_views, data_views, image_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(data_views.bp)
    app.register_blueprint(image_views.bp)

    return app