from flask import Flask, render_template, request

app = Flask(__name__)

#데코레이터. 루트 호출시 아래 코드를 실행시킴
@app.route('/') 
def hello_world():
    return "Hello World"

@app.route('/sql')
def index():
    return render_template('index.html')

@app.route('/command', methods=['POST'])
def command():
    return "Test" + request.form.get('first_test')


if __name__ == "__main__":
    app.run(debug=True)
