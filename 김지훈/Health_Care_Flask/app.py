from flask import Flask, render_template, request, redirect, url_for, g, jsonify


app = Flask(__name__)

# 실제로 이렇게 관리하면 망함
app.secret_key = 'secretkey'

import app_image
import app_register
import app_data
import app_login
import app_board

@app.route('/')
def hello():
    
    if g.user is not None:
        return render_template("index.html", userName = g.user.user_name)
    return render_template("index.html")

@app.route('/redirectTest')
def redirectTest():
    return redirect(url_for('hello'))


if __name__ == "__main__":
    app.run(debug=True)



