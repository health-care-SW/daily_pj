from flask import Flask
import pymysql
from flask_bcrypt import Bcrypt


from pyproject import app_main
from pyproject import app_image
from pyproject import app_data

from pyproject import api
from pyproject.db_connect import db


app = Flask( __name__ )



# app.register_blueprint( app_main.bp )

app.register_blueprint( api.board )

app.register_blueprint( app_image.bp )
app.register_blueprint( app_data.bp )

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://hchang:devpass@127.0.0.1:3306/board"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 암호화를 위해 특정 문자열을 secret_key에 저장하여야 함. 들어갈 값은 임의의 값. 일반적으로 random 함수를 사용해서 변경하여 사용 
app.secret_key = 'My_key'

db.init_app(app)
bcrypt = Bcrypt(app)

if __name__ == '__main__':
    app.run( debug=True )
