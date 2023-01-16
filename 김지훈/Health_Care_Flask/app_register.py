from flask import Flask, render_template, request
import User

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("register.html")


@app.route('/register', methods=["POST"])
def register():
    userName = request.form.get('user_name')
    userPw = request.form.get('user_password')
    userEmail = request.form.get('user_email')
    user = User.User(userName, userPw, userEmail)
    User.insert_user(user)
    return render_template("register.html")

if __name__ == "__main__":
    print(123)
    app.run(debug=True)