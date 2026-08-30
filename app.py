# 核心修复：必须在导入任何其他包之前，导入 eventlet 并进行 monkey_patch
import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my-secret-key'

# 核心修复：指定 async_mode='eventlet'，并允许跨域
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/msg.mp3')
def sound():
    return send_from_directory('static', 'msg.mp3')

@socketio.on('chat message')
def handle_message(msg):
    print('收到消息: ' + msg)
    send(msg, broadcast=True)

if __name__ == '__main__':
    # 核心修复：使用 socketio.run 启动，并加上 allow_unsafe_werkzeug=True
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
