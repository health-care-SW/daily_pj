from flask import render_template, Blueprint, request
import sqlite3
import pandas as pd


bp = Blueprint('dtb', __name__, url_prefix='/dtb')


def get_db(db_name):
    return sqlite3.connect(db_name)


def exe_sql(conn, command: str):
    try:
        conn.execute(command)
        conn.commit()

        if command.split(" ")[0].lower() == 'select':
            df = pd.read_sql(command, conn, index_col=None)
            df_html = df.to_html()
            return df_html, 2
        else:
            return 'select 아님', 1
    except:
        return None, 0


@bp.route('/')
def dtb():
    return render_template('dtb/dtb.html')


@bp.route('/dbsql/', methods=["POST"])
def sql_test():
    if request.method == 'POST':
        db_name = request.form.get('db_name')
        sql_command = request.form.get('sql')

        conn = get_db(db_name)

        output, status = exe_sql(conn, sql_command)
        if status == 1:
            return render_template('dtb/dtb.html', label="정상 작동") + output
        elif status == 2:
            return render_template('dtb/show_table.html') + output
        else:
            return render_template('dtb/dtb.html', label="오류 발생", output=None)
    else:
        return render_template('dtb/dtb.html')


@bp.route('/show_table',methods=['POST'])
def show_table():
    return render_template('dtb/show_table.html')
