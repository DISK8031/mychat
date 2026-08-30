# ⚠️ 核心修复：这两行必须放在最最最前面，不能有任何其他 import 在它们上面！
import eventlet
eventlet.monkey_patch()

# 下面才是正常的导入
from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my-secret-key'

# 指定异步模式为 eventlet
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
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
