from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "<a href='/sql'>Hello World</a>"

@app.route('/sql')
def index():
    return render_template("index.html")

@app.route('/command', methods=['POST','GET'])
def command():
    if request.method == 'POST':
        string = request.form.get('first_test')
        ll = list(string)
        res = "잘못된 형식"
        try:
            if ll[1] == '+':
                res = int(ll[0]) + int(ll[2])
            elif ll[1] == '-':
                res = int(ll[0]) - int(ll[2])
            elif ll[1] == '*':
                res = int(ll[0]) * int(ll[2])
            elif ll[1] == '/':
                res = int(ll[0]) / int(ll[2])
        except:
            pass    
        return render_template("index.html", result=res)
        # return "test "+ string


if __name__ == "__main__":
    app.run(debug=True)