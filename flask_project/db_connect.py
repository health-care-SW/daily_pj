import pymysql

db_conn = pymysql.connect(
        host = 'localhost',
        port = 3306,
        user = 'root',
        passwd = '1234',
        db = 'flaskdb',
        charset = 'utf8',

)
print(1)
print(db_conn)