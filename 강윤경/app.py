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
from flask import Flask

# __name__ 파이썬 기본 변수
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello world'

if __name__ == '__main__':
    app.run()
# 터미널에 python .\app.py 입력 시 http:// ~에 실행되고 있다고 뜸