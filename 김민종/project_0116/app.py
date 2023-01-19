from flask import Flask, render_template, session, send_from_directory
from flask_bcrypt import Bcrypt
from api import board
from classification import classi
from community import commu
import os
from util import str2time

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.register_blueprint(board)
app.register_blueprint(classi)
app.register_blueprint(commu)

app.jinja_env.filters['datetime'] = str2time

app.secret_key = 'tjdnf'
app.config['SESSION_TYPE'] = 'filesystem'

def get_app():
    return app

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico')

@app.route("/")
def main():
    if session.get("login"):
        print("session exist")
    else:
        print("session not exist")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)