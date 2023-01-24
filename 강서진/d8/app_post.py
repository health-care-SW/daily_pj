from flask import redirect, render_template, request, jsonify, Blueprint, session, g, url_for
from models import User, Post, db
import datetime
from datetime import timezone
from sqlalchemy import update


board = Blueprint('post', __name__)


@board.before_app_request
def load_logged_in_user():
    username = session.get('login')
    if username is None:
        g.user = None
    else:
        g.user = db.session.query(User).filter(User.username == username).first()


@board.route("/blog", methods=["GET"])
def forum():
    guest = "GUEST"
    post_list = Post.query.order_by(Post.created_at.desc())

    return render_template('blog.html', post_list=post_list, guest=guest)


@board.route("/post", methods=["GET", "POST"])
def post():
    guest="GUEST"
    # 세션 o
    if 'login' in session:
        # 로그인하지 않은 상태일 때
        if session['login'] == None:
            return render_template('login.html', message="You need to login first.", guest=guest)

        # 로그인 한 상태일 때    
        else:
            # 글 작성 후 폼 제출시 db에 커밋 ("POST")
            if request.method == "POST":

                title = request.form['title']
                author = session['login']
                content = request.form['content']
                created_at = datetime.datetime.now(timezone.utc)
                modified_at = None
                # print(title, author, content, created_at)

                new_post = Post(title, author, content, created_at, modified_at)

                db.session.add(new_post)
                db.session.commit()
                return render_template('blog.html', message="Submitted.")

            # 링크로 접근시 작성 폼 ("GET")
            else:
                return render_template('post.html')

    # 세션 x
    else:
        return render_template('login.html', message="You need to login first.", guest=guest)

@board.route("/content/<int:postid>/", methods=["GET"])
def show_post(postid):
    guest="GUEST"
    # 세션 o
    if 'login' in session:
        if session['login']:
            post = Post.query.get(postid)
            return render_template('content.html', post=post, postid=postid)
        else:
            return render_template('login.html', message="You need to login to see this post.", guest=guest)
    
    # 세션 x
    else: 
        return render_template('login.html', message="You need to login to see this post.", guest=guest)


@board.route('/edit/<int:postid>/', methods=["GET","POST"])
def edit_post(postid):
    post = Post.query.get(postid)
    print(post.id)

    # edit 버튼 눌러서 접근 ("GET")
    if request.method=="GET":
        return render_template('edit.html', post=post, postid=postid)

    # edit 완료하고 폼 제출 ("POST")
    else:
        post.title = request.form['title']
        post.content = request.form['content']
        post.modified_at = datetime.datetime.now(timezone.utc)

        db.session.commit()
        
        return render_template('base.html', message="Your post has been edited.")
            
@board.route('/delete/<int:postid>/', methods=["GET"])
def delete_post(postid):

    post = Post.query.get(postid)
    db.session.delete(post)
    db.session.commit()

    return render_template('blog.html', message="Your post has been deleted.")
