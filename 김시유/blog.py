from flask import Flask, render_template
import random
import datetime
import requests


app = Flask(__name__)


@app.route('/')
def hello_world():
    random_num = random.randint(1, 10)
    current_year = datetime.datetime.now().year
    return render_template('blog.html', num=random_num, year=current_year)


@app.route('/guess/<name>')
def guess(name):
    gender_url = f"https://api.genderize.io?name={name}"
    gender_response = requests.get(gender_url)
    gender_data = gender_response.json()
    gender = gender_data['gender']
    age_url = f"https://api.agify.io?name={name}"
    age_response = requests.get(age_url)
    age_data = age_response.json()
    age = age_data['age']
    current_year = datetime.datetime.now().year

    return render_template('blog2.html', person_name=name, gender=gender, age=age, year=current_year)


@app.route('/blog')
def blog():
    blog_url = "https://www.npoint.io/docs/c790b4d5cab58020d391"
    response = requests.get(blog_url)
    all_posts = response.json()
    return render_template('blog3.html', posts=all_posts)


if __name__ == "__main__":
    app.run(debug=True)
