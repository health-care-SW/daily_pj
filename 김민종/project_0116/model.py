import pymysql

class User():
    __tablename__ ='user'

    def __init__(self, user_id, user_pw):
        self.user_id = user_id
        self.user_pw = user_pw

    def get_db():
        # 디비 연결(mysql)
        return pymysql.connect(
                        host='localhost',
                        port=3306,
                        user='root',
                        passwd='327954',
                        db="webProject",
                        charset='utf8')

    def find(id):
        conn = User.get_db()
        cursor = conn.cursor()
        sql = "select * from user where id=%s;"
        cursor.execute(sql,(id))
        rows = cursor.fetchall()
        for row in rows:
            if row[0] == id:
                db_id = row[0]
                db_pw = row[1]
                break
        user = User(db_id, db_pw)
        return user