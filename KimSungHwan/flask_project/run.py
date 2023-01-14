from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/') #함수나 클래스 앞에 붙혀서 추가적인 기능을 구현(루트경로를 호출하면 아래것을 실행시켜라)
def home():
    return 'hello world'

@app.route('/sql')
def index():
    return render_template('index.html')

@app.route('/command',methods = ['POST'])
def command():
    return "Test" + request.form.get('first_test')

if __name__ == '__main__':
    app.run(debug=True)