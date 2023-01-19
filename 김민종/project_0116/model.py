from Database import Database 
class User():
    __tablename__ ='user'

    def __init__(self, user_id, user_pw):
        self.user_id = user_id
        self.user_pw = user_pw

    def find(id):
        conn = Database().get_db()
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