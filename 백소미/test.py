import pymysql

#connect
db = pymysql.connect(host="localhost", user="root", password="1234", charset="utf8")
cursor = db.cursor(pymysql.cursors.DictCursor)
cursor.execute('USE flask_pj_db;')
#cursor.execute('INSERT INTO user (user_id, user_pw, user_name) VALUES ("som","1234*","소미")')
cursor.execute('SELECT * FROM user;')
value = cursor.fetchall()
print(value[0]['user_name'])

#cursor.execute('UPDATE user SET user_name="백소미" WHERE user_id="som"')
#cursor.execute('DELETE FROM user WHERE user_id="som"')

db.commit()
db.close()