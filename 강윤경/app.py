# ctrl+ v : 컨트롤창 껐다켰다
# ctrl+ ~ : 터미널
# flask 가상환경 만드는 명령어(터미널에 입력) python -m venv flask_env
# 내가 쓰는 window powershell의 정체 확인 Get-ExecutionPolicy -List
# LocalMachine 이 Undefined로 뜸
# 터미널을 관리자 권한으로 실행하여 바꿔줘야
# 터미널을 관리자 권한으로 실행 : 윈도우 + x -> powershell(관리자) -> Set-ExecutionPolicy RemoteSigned -> Y
# flask_env\Scripts\Activate.ps1 (상대경로 복사) 입력시 가상환경 성공적으로 만들어졌다는 (flask_env) 적혀나옴
# source {가상환경 이름}/bin/activate
# pip install Flask
# pip list 설치된 목룍 ( pip : 라이브러리 설치하는데 도와주는 명령어)

# 우측 하단 개발환경을 flask로 변경 후
from flask import Flask, render_template, request
# request : 사용자가 보내는 응답 받아서 사용

# __name__ 파이썬 기본 변수
app = Flask(__name__)

# decorator 문법. 함수 앞에 붙여 추가적 기능 구현. 여기서는 route 경로 호출 시 아래 함수 수행하게 만듦
# '/' 대신 다양한 경로를 써넣을 수 있을것   ex> /sql

@app.route('/')
def hello_world():
    return 'Hello world'

@app.route('/sql')
def index():
    return render_template('index.html')

# http://127.0.0.1:5000/sql에 index.html 뜸

# 특정상황에서만 페이지 출력 methods
@app.route('/command', methods=['POST'])
def command():
    return "TEST" + request.form.get('first_test')   #render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
# 터미널에 python .\app.py 입력 시 http:// ~에 실행되고 있다고 뜸

# 리눅스, 맥, 윈도우 git은 구글 검색 후 다운받으면 됨
# path 의미 : 

# ssh : 외부 서버에 원격연결 위한 tool
# git fetch : 원본 폴더의 상태를 알 수 있게 해줌 ( n commits )

# 잘 안되면 ctrl + c를 눌러 flask 서버 닫았다가 flask run 입력, 코드 run하여 다시 해보면 될 수 있음

