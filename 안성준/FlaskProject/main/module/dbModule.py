import pymysql

class Database():
    def __init__(self) -> None:
        self.db = pymysql.connect(host='localhost', user='root', password='Aasdf1234!', db='shopping_mall', charset='utf8')
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

    def commit(self):
        self.db.commit()

    def execute(self, query, args={} ):
        self.cursor.execute(query, args)

    def executeOne(self, query, args={} ):
        self.cursor.execute(query, args)
        row = self.cursor.fetchone()
        return row

    def executeAll(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        return row
    