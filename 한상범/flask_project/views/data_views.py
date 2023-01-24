from flask import Blueprint, render_template, request
import pandas as pd
from .. import db
from flask_project.models import User

# def get_db(db_name):
#     return sqlite3.connect(db_name)

def exe_sql(command):
    com = command.split()
    print(com)
    try:
        if com[0].lower() == 'add': # 명령어 : add id pw
            user = User(id = int(com[1]), password = com[2])
            db.session.add(user)
            db.session.commit()
            return None, 2

        elif com[0].lower() == 'query': # 명령어 : 쿼리 id
            user = User.query.filter_by(id = int(com[1])).first()
            # df = pd.read_sql(user.statement, user.session.bind)
            # df_html = df.to_html()
            
            return user, 1

    except:
        return None, 0


bp = Blueprint('data', __name__, url_prefix='/data')

@bp.route('/page/')
def page():
    return render_template('data.html')


@bp.route('/dbsql/', methods = ["POST"])
def dbsql():
    if request.method=='POST':
        db_name = request.form.get('db_name') # 강의에서는 SQL을 썼지만 현재는 ORM을 쓰니 필요없음
        sql_command = request.form.get('sql')

        # conn = get_db(db_name) 커넥트는 필요없음 원래 연결되어 있음

        output, status = exe_sql(sql_command)
        if status==1:
            # 잘 처리됨
            return render_template('data.html', label = "정상작동", id = output.id, password = output.password)
        elif(status == 2):
            return render_template('data.html', label = "저장완료")
        else:
            return render_template('data.html', label = "오류 발생")