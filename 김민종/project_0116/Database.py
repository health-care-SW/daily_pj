import pymysql

class Database():
    def __init__(self):
        self.db = pymysql.connect(
                        host='localhost',
                        port=3306,
                        user='root',
                        passwd= self.get_pwd(),
                        db="webProject",
                        charset='utf8')
    def get_pwd(self):
        with open("pwd.txt","r") as f:
            return f.read()

    def get_db(self):
        return self.db

    def execute_query(self, sql, *params):
        conn = self.get_db()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
        return cursor