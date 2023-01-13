from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def hello():
    return 'hello world'


@app.route('/sql')
def index():
    return render_template("index.html")

@app.route('/command', methods=['POST'])
def command():
    getStr = request.form.get('first_test')

    if '+' in getStr: 
        a,b = getStr.split('+')
        res = int(a) + int(b)

        return 'command: ' + str(res)
    else:
        return 'invalid command'


if __name__ == "__main__":
    app.run(debug=True)


















