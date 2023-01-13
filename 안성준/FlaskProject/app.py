from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'hello'

@app.route('/sql')
def index():
    return render_template('index.html')

@app.route('/command',methods=['POST'])
def sql():
    return "TEST" + request.form.get('first_test')

if __name__=="__main__":
    app.run()