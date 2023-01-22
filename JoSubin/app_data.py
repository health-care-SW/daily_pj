# from flask import Flask, render_template, request
# from flask_ngrok import run_with_ngrok
# import os
# import sqlite3
# import pandas as pd

# app = Flask(__name__)
# run_with_ngrok(app)

# '''
# DB 함수
# '''
# def get_db(db_name):
#     return sqlite3.connect(db_name)

# def sql_command(conn, command):

#     try :

#         conn.execute(command)
#         conn.commit()
#         command = command.lower()

#         if "select" in command:

#             command_split = command.split(" ")
#             select_command = "SELECT * FROM " + command_split[command_split.index("from")+1]
#             df = pd.read_sql(select_command, conn, index_col=None)
#             html = df.to_html()

#             conn.close()

#             return html, 1

#         conn.close()

#         return True, 1

#     except Exception as exception:

#         conn.close()

#         return False, exception


# '''
# File upload
# '''
# @app.route("/index")
# def index():
#     return render_template('data.html')

# @app.route('/dbsql', methods=['POST'])
# def sql_processing():
#     if request.method == 'POST':

#         con = get_db('/' + request.form.get('db_name'))
#         sql = request.form.get('sql')
#         result_sql, excep = sql_command(con, sql)

#         if result_sql == False :
#             return render_template('data.html', label="비정상" +  str(excep))

#         elif result_sql == True :
#             return render_template('data.html', label="정상 작동")

#         else :
#             result_sql = "<html><body> " + result_sql + "</body></html>"
#             return result_sql

# if __name__ == '__main__':
#     app.run()

