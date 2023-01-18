import pymysql

class Database():
    def get_pwd():
        with open("pwd.txt","r") as f:
            return f.read()

    def get_db():
        # 디비 연결(mysql)
        return pymysql.connect(
                        host='localhost',
                        port=3306,
                        user='root',
                        passwd= Database.get_pwd(),
                        db="webProject",
                        charset='utf8')