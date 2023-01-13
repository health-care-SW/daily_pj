from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello siyou^__^"

# # html파일로 응답하기
@app.route('/sql')  
def index():
    return render_template('index.html')

@app.route('/command', methods=['POST'])  
def command():
    
    return "TEST" + request.form.get('command')


if __name__=="__main__":
    app.run(debug=True)
    
#가상환경 활성화 : .\flask_env\Scripts\Activate.ps1   (ps1은 powershell이라서)
# python .app/py3

