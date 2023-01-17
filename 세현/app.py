# main file
# []
# ctrl+B
# 터미널 껐다켰다? ctrl+ `

from flask import Flask, render_template, request

app = Flask(__name__) # 전체 프로그램 관장

@app.route('/') # 문법: 데코레이터 #root 경로를 실행하면 아래 함수를 실행해라
def hello_world():
    return "Hello world"

@app.route('/sql')
def index():
    return render_template('index.html')

@app.route('/command', methods=['POST']) #web에서 API로 Data를 주고받을 때 POST, GET
def command():
    #print(request.form.get('first_test'))
    return "Test" + request.form.get('first_test') # render_template('index.)

if __name__=="__main__":
    app.run(debug=True)
