from flask import Flask

app = Flask(__name__)

@app.route('/data')
def hello_world():
    return "Hello world"

if __name__=="__main__":
    app.run()
