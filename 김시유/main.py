from flask import Flask, render_template
import requests

blog_posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html", posts=blog_posts)


@app.route('/post/<int:blog_id>')
def get_post(blog_id):
    for post in blog_posts:
        if post["id"] == blog_id:
            return render_template("post.html", post=post)


if __name__ == "__main__":
    app.run(debug=True)
