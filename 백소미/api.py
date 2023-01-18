from flask import Flask, redirect

app = Flask(__name__)



@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return redirect(login.html)
    elif request.method == 'POST':
        #데이터 저장
        user_id = request.form['user_id']
        user_pw = request.form['user_pw']

        user = User.query.filter(User.user_id == user_id).first()


if __name__ == '__main__':
    app.debug = True
    app.run()

