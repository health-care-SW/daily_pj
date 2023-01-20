from flask import Flask, render_template
import random

random_number = random.randint(0, 9)
print(random_number)

app = Flask(__name__)


@app.route('/')
def hello_world():
    # Rendering HTML Elements
    return '<h1 style="text-align: center">Hello, World!</h1>' \
           '<p>This is a paragraph.</p>' \
           '<img src="https://media.giphy.com/media/hvS1eKlR75hMr0l7VJ/giphy.gif" width=200>'

# <num>처럼 꺽쇄로 들어온 자료를 내보내기


def make_bold(function):
    def wrapper():
        return "<b>" + function() + "</b>"
    return wrapper


def make_emphasis(function):
    def wrapper():
        return "<em>" + function() + "</em>"
    return wrapper


def make_underlined(function):
    def wrapper():
        return "<u>" + function() + "</u>"
    return wrapper


@app.route('/bye')
@make_bold
@make_emphasis
@make_underlined
def bye():
    return "Bye!"


@app.route('/read/<num>/')
def read(num):
    print(num)
    return 'read ' + num


@app.route('/username/<name>/<int:number>')
def greet(name, number):
    return f"Hello {name}, you are {number} years old!"


@app.route('/guess')
def home_guess_number():
    return "<h1>Guess a number between 0 and 9</h1>" \
           "<p>URL/7 과 같이 / 와 생각한 숫자를 입력해주세요!</p> " \
           "<img src='https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif'/>"


@app.route("/guess/<int:guess>")
def guess_number(guess):
    if guess > random_number:
        return "<h1 style='color: purple'>Too high, try again!</h1>" \
               "<img src='https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif'/>"

    elif guess < random_number:
        return "<h1 style='color: red'>Too low, try again!</h1>"\
               "<img src='https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif'/>"
    else:
        return "<h1 style='color: green'>You found me!</h1>" \
               "<img src='https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif'/>"


@app.route('/hello')
def hello():
    return render_template("index1.html")


app.run(debug=True)

#index1.html


#강제 새로고침 : shift +f5
# 크롬 캐시삭제 : ctrl+shift+del