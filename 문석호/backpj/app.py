from flask import Flask, render_template, request
from flask_ngrok import run_with_ngrok
import os
import sqlite3
import pandas as pd

app = Flask(__name__)
run_with_ngrok(app)

def get_db(db_name):
    return sqlite3.connect(db_name)

def sql_command(conn, command):
    try :
        conn.execute(command)
        conn.commit()
        command = command.lower()

        if "select" in command:
            command_split = command.split(" ")
            select_command = "SELECT * FROM " + command_split[command_split.index("from")+1]
            df = pd.read_sql(select_command, conn, index_col=None)
            html = df.to_html()
            conn.close()
            return html, 1

        conn.close()

        return True, 1

    except Exception as exception:
        conn.close()
        return False, exception

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/main")
def main():
    return render_template('main.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')