from flask import Flask, render_template, request
app = Flask(__name__) # Flask라는 클래스를 app이라는 인스턴스에 받는 것이다.

@app.route('/') # 이 경로를 호출하면 아래의 함수를 호출하여라.
def hello_world():
    return "Hello World"

@app.route('/sql')
def index():
    return render_template("index.html")

@app.route('/command', methods=['POST'])
def test():
    return "TEST"+request.form.get('first_test')
           
if __name__ == "__main__":
    app.run(debug=True)