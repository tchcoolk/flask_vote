from flask import Flask, render_template, request, session, redirect, jsonify
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
import json
import uuid

app = Flask(__name__)
app.debug = True
app.secret_key = 'tch'

PLAYERS = {
    0: {'name': 'tch', 'count': 0},
    1: {'name': 'rt', 'count': 0},
    2: {'name': 'root', 'count': 0}
}

WS_DICT = {

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
            uid = uuid.uuid4()
            session['user'] = uid
            # USER_DICT[uid] = Queue()
            return redirect('/index')
        else:
            return redirect('/login')


@app.route('/index')
def index():
    return render_template('index.html', players=PLAYERS)


@app.route('/message')
def message():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        # 刚连接成功
        uid = session.get('user')
        WS_DICT[uid] = ws

        while True:
            # 等待用户发送消息,并接受
            player_id = ws.receive()
            # 如果客户端发送了关闭或者异常，那么message=None

            if player_id == None:
                del WS_DICT[uid]
                break

            player_id = int(player_id)
            print(player_id)

            old = PLAYERS[player_id]['count']
            new = old + 1
            PLAYERS[player_id]['count'] = new

            response = {'player': player_id, 'count': new}
            print(response)

            # 向客户端推送消息
            # k -> 用户唯一标识
            # v -> 用户对应的ws
            for k, v in WS_DICT.items():
                v.send(json.dumps(response))

    return 'Connected!'


if __name__ == '__main__':
    http_server = WSGIServer(('127.0.0.1', 5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
