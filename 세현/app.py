# main file
# []
# ctrl+B
# 터미널 껐다켰다? ctrl+ `

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello world"

if __name__=="__main__":
    app.run()
