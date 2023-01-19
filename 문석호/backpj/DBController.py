import sqlite3
from sqlite3 import Error
import numpy as np

con = sqlite3.connect('users')

def connectDB(dbName):
    try:
        return sqlite3.connect(dbName)
    except Error:
        print(Error)

def createTable(dbCon, tbname, colName, colType):
    dbCursor = dbCon.cursor()

    # CREATE문 만들기 >> create table tablename(columnname1 columntype1, columnname2 columntype2, ...)
    sql_create = ""
    collist = np.column_stack(colName, colType)
    for j in range(len(collist)):
        for i in range(len(collist[j])):
            sql_create += str(collist[j][i])
            if i != len(collist[j])-1:
                sql_create += " "
            else:
                if j != len(collist)-1:
                    sql_create += ", "
    
    dbCursor.execute("create table "+tbname+"("+sql_create+")")
    dbCon.commit()

def insertValue(dbCon, tbname, vallist):
    dbCursor = dbCon.cursor()

    # INSERT INTO문 만들기 >> insert into tablename values (value1, value2, ...)
    sql_insert = ""
    for temp in vallist:
        sql_insert += str(temp)+" "
    sql_insert = sql_insert[:len(sql_insert)-1]

    dbCursor.execute("insert into "+tbname+" values("+sql_insert+")")
    dbCon.commit()

# def update():

# def search():

# def delete():


# def sql_command(conn, command):
#     try :
#         conn.execute(command)
#         conn.commit()
#         command = command.lower()

#         if "select" in command:
#             command_split = command.split(" ")
#             select_command = "SELECT * FROM " + command_split[command_split.index("from")+1]
#             df = pd.read_sql(select_command, conn, index_col=None)
#             html = df.to_html()
#             conn.close()
#             return html, 1

#         conn.close()

#         return True, 1

#     except Exception as exception:
#         conn.close()
#         return False, exception