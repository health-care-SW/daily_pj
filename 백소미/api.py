from flask import Flask, request, redirect

app = Flask(__name__)

nextId = 4
topics = [
    {'i': 1,'user_id': 'one','user_pw': '1111'},
    {'i': 2,'user_id': 'two','user_pw': '2222'},
    {'i': 3,'user_id': 'three','user_pw': '3333'}
]

def template(contents, content, i=None): #id 기본값 None
    contextUI = ''
    if i != None:
        contextUI = f'''
            <li><a href="/update/{i}/">회원정보수정</a></li>
            <li><form action="/delete/{i}/" method="POST"><input type="submit" value="회원탈퇴"></form></li>
        '''
    return f'''
    <!doctype html> 
    <html>
        <body>
            <h1><a href="/">HOME</a></h1>
            <p>userlist</p>
            <ol>
                {contents}
            </ol>
            {content}
            <ul>
                <li><a href="/create/">회원등록</a></li>
                {contextUI}
            </ul>
        </body>
    </html>
    '''

def getContents():
    liTags = ''
    for topic in topics:
        liTags = liTags + f'<li><a href="/read/{topic["i"]}">{topic["user_id"]}</a></li>'
    return liTags

@app.route('/')
def index():
    return template(getContents(), '<h2>Welcome</h2>')

@app.route('/read/<int:i>/')
def read(i):
    title = ''
    body = ''
    for topic in topics:
        if i == topic['i']:
            user_id = topic['user_id']
            user_pw = topic['user_pw']
            break
    print(user_id, user_pw)
    return template(getContents(), f'<h2>id : {user_id}</h2>password : {user_pw}', i) # 선택한 id 전달

@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == "GET":
        content = '''
            <form action="/create/" method="POST">
                <p><input type="text" name="user_id" placeholder="id"></p>
                <p><input type="password" name="user_pw" placeholder="password"></textarea></p>
                <p><input type="submit" value="create"></p>
            </form>
        '''
        return template(getContents(), content)

    elif request.method == "POST":
        global nextId
        user_id = request.form['user_id']
        user_pw = request.form['user_pw']
        newTopic = {'i': nextId, 'user_id': user_id, 'user_pw': user_pw} # 새 dic 생성
        topics.append(newTopic) # topics에 추가
        url = '/read/'+str(nextId)+'/'
        nextId = nextId + 1
        return redirect(url) # url로 이동

@app.route('/update/<int:i>/', methods=['GET', 'POST'])
def update(i):
    if request.method == "GET":
        user_id = ''
        user_pw = ''
        for topic in topics:
            if i == topic['i']:
                user_id = topic['user_id']
                user_pw = topic['user_pw']
                break
        content = f'''
            <form action="/update/{i}/" method="POST">
                <p>id : <input type="text" name="user_id" placeholder="id" value="{user_id}"></p>
                <p>password : <input type="text" name="user_pw" value="{user_pw}"></p>
                <p><input type="submit" value="update"></p>
            </form>
        '''
        return template(getContents(), content)

    elif request.method == "POST":
        global nextId
        user_id = request.form['user_id'] #title 받아옴
        user_pw = request.form['user_pw'] #body 받아옴
        for topic in topics:
            if i==topic['i']:
                topic['user_id'] = user_id
                topic['user_pw'] = user_pw
                break
        url = '/read/'+str(i)+'/'
        return redirect(url) # url로 이동
    
@app.route('/delete/<int:i>/', methods=['POST'])
def delete(i):
    for topic in topics:
        if i == topic['i']:
            topics.remove(topic)
            break
    return redirect('/')

app.run(debug=True)