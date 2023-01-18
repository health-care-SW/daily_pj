from flask import Blueprint, render_template, request, redirect
from flask import current_app as app
from main.module import dbModule

app = Blueprint("home",__name__, url_prefix="")

@app.route("/", methods=['GET','POST'])
def home():
    if request.method == 'POST':
        id = request.form.get('uid')
        password = request.form.get('upw')
        db_class = dbModule.Database()
        sql = "SELECT user_password, user_name FROM users WHERE user_email = '%s'"%(id)
        row = db_class.executeAll(sql)
        if row[0]['user_password'] == password:
            return render_template("index.html", label=row[0]['user_name'])
        else: return redirect('/login')
    else:
        return render_template("index.html")

@app.route("/login",methods=['POST','GET'])
def login():
    if request.method=='POST':
        db_class = dbModule.Database()
        name = request.form.get('userName')
        password = request.form.get('userPassword')
        email = request.form.get('userEmail')
        sql = "INSERT into users( user_name, user_password, user_email ) values( '%s', '%s', '%s' )"%(name, password, email)
        row = db_class.executeAll(sql)
        db_class.commit()
        print(row)
        return render_template("login.html")
    else:
        return render_template("login.html")
    
@app.route("/register", methods=['POST'])
def sugnup():
    return render_template("register.html")