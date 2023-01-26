import pymysql

conn = pymysql.connect(
        host = 'localhost',
        port = 3306,
        user = 'root',
        passwd = '1234',
        db = 'flaskdb',
        charset = 'utf8',

)

def insert(a,b):

        cursor = conn.cursor() 
      
        sql = "INSERT INTO flaskdb.user VALUE('{}','{}');".format(a,b)

        # "INSERT INTO flaskdb.user VALUE ('5', 'geon', 'ddd','5555');"
              
        
        # sql 구문 실행하기
        cursor.execute(sql) 

        # 실행한 데이터 받아오기
        # print(rows)
        conn.commit() 
        conn.close() 

def print_rows():
        cursor = conn.cursor() 
        sql = "SELECT * FROM flaskdb.user;"
        cursor.execute(sql)
        rows = cursor.fetchall()
        print(rows)
        conn.commit()
        conn.close()
        
# print(1)
# print(db_conn)

