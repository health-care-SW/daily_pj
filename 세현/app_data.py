# '''
# File upload
# '''
# @app.route("/index")
# def index():
#     return render_template('data.html')

# @app.route('/dbsql', methods=['POST'])
# def sql_processing():
#     if request.method == 'POST':

#         con = get_db(request.form.get('db_name'))

#         sql = request.form.get('sql')
#         result_sql = sql_command(con, sql)

#         if result_sql == False :
#             return render_template('data.html', label="비정상")

#         elif result_sql == True :
#             return render_template('data.html', label="정상 작동")

#         else :
#             result_sql = "<html><body> " + result_sql + "</body></html>"
#             return result_sql
