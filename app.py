from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my-secret-key'

# 核心修改1：加上 cors_allowed_origins="*" 允许跨域
# 核心修改2：加上 async_mode='threading' 兼容 Render 免费版环境
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/msg.mp3')
def sound():
    return send_from_directory('static', 'msg.mp3')

@socketio.on('chat message')
def handle_message(msg):
    print('收到消息: ' + msg)
    # broadcast=True 表示把消息广播给所有在线的人
    send(msg, broadcast=True)

# 核心修改3：必须用 socketio.run，并加上 allow_unsafe_werkzeug=True
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
