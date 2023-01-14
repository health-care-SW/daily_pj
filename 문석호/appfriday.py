from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello, World!"

@app.route('/sql')
def index():
    return render_template('index.html')

@app.route('/command', methods=['POST'])
def command():
    exp = request.form.get('first_test').split()

    if len(exp)!=3:
        return "연산 1번만 가능"
    elif exp[1] == '+':
        return exp[0] + exp[2]
    elif exp[1] == '-':
        return int(exp[0]) - int(exp[2])
    elif exp[1] == '*':
        return int(exp[0]) * int(exp[2])
    elif exp[1] == '/':
        if int(exp[2]) == 0:
            return "DIV 0 ERROR"
        else:
            return int(exp[0]) / int(exp[2])
    else:
        return "TEXT"
    # return "TEST"+request.form.get('first_test') # render_template('index.html')

if __name__=="__main__":
    app.run()

