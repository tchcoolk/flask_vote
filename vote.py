from flask import Flask, render_template, request, session, redirect,jsonify
from queue import Queue,Empty

app = Flask(__name__)
app.debug = True
app.secret_key = 'tch'

PLAYERS = {
    0: {'name': 'tch', 'count': 0},
    1: {'name': 'rt', 'count': 0},
    2: {'name': 'root', 'count': 0}
}

USER_DICT = {

}


@app.before_request
def before_request():
    if request.path == '/login':
        return None
    else:
        user = session.get('user')
        if user:
            return None
        else:
            return redirect('/login')


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        if username:
            session['user'] = username
            USER_DICT[username] = Queue()
            return redirect('/index')
        else:
            return redirect('/login')


@app.route('/index')
def index():
    return render_template('index.html', players=PLAYERS)


@app.route('/message')
def message():
    msg = {'status': True, 'msg': None}
    try:
        q = USER_DICT[session.get('user')].get(timeout=5)
        msg['msg'] = q
    except Empty:
        pass
    print(jsonify(msg),type(jsonify(msg)))
    return jsonify(msg)


@app.route('/vote')
def vote():
    user_id = int(request.args.get('user_id'))
    try:
        PLAYERS[user_id]['count'] += 1
        username = session.get('user')
        for key,q in USER_DICT.items():
            q.put({'user_id': user_id, 'count': PLAYERS[user_id]['count']})
        return '投票成功'
    except Exception as e:
        return '投票失败'


if __name__ == '__main__':
    app.run(threaded=True)
