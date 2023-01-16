import DB_CONNECT



if __name__ == "__main__":
    conn, cur = DB_CONNECT.DB_connect()

    sql = "SELECT * FROM users"
    cur.execute(sql)
    conn.commit()	# 저장
    for u in cur.fetchall():
        print(u)
    conn.close()	# 종료