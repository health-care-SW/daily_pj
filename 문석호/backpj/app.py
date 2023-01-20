from flask import Flask, render_template, request, Blueprint
from flask_ngrok import run_with_ngrok


app = Flask(__name__)
run_with_ngrok(app)

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/")
def main():
    return render_template('main.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run()