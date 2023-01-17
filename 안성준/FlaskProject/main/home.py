from flask import Blueprint, render_template, request
from flask import current_app as app
from main.module import dbModule

app = Blueprint("home",__name__, url_prefix="")

@app.route("/", methods=['GET','POST'])
def home():
    if request.method == 'POST':
        id = request.form.get('uid')
        password = request.form.get('upw')
        db_class = dbModule.Database()
        sql = "SELECT user_password FROM users WHERE user_email = '%s'"%(id)
        row = db_class.executeAll(sql)
        if row[0]['user_password'] == password:
            return render_template("index.html")
    else:
        return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")