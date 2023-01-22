import pymysql
from flask import Flask
from db_connect import db
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:1234@127.0.0.1:3306/notice_board"
app.config['SQLARCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'ekdwls'

db.init_app(app)
Bcrypt = Bcrypt(app)

from models import *

# 블루프린트
from views import main_views, question_views, answer_views, auth_views, comment_views
app.register_blueprint(main_views.bp)
app.register_blueprint(question_views.bp)
app.register_blueprint(answer_views.bp)
app.register_blueprint(auth_views.bp)
app.register_blueprint(comment_views.bp)

# 필터
from filter import format_datetime
app.jinja_env.filters['datetime'] = format_datetime

if __name__ == '__main__':
    app.run(debug=True)