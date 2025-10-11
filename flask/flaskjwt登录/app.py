import psutil
import time
from datetime import timedelta
from flask import Flask, render_template, jsonify, request
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from flask_cors import CORS

app = Flask(__name__, template_folder='templates', static_folder='static')

app.config['JWT_SECRET_KEY'] = 'super-secret-key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)

jwt = JWTManager(app)
CORS(app, supports_credentials=True)

# 用户列表
USERS = {
    "admin": "123456",
    "user": "123456"
}

# 缓存
prev_disk_io = psutil.disk_io_counters()
prev_net_io = psutil.net_io_counters()
prev_time = time.time()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if username not in USERS or USERS[username] != password:
        return jsonify({"msg": "用户名或密码错误"}), 401

    token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)
    return jsonify(access_token=token, refresh_token=refresh_token), 200


@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_token), 200


@app.route('/app/metrics', methods=['GET'])
@jwt_required()
def metrics():
    global prev_disk_io, prev_net_io, prev_time

    current_time = time.time()
    time_diff = current_time - prev_time or 1

    cpu_percent = psutil.cpu_percent(interval=1)
    print(cpu_percent)
    cpu_freq = psutil.cpu_freq().current if psutil.cpu_freq() else 0
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    # 计算磁盘 IO
    current_disk_io = psutil.disk_io_counters()
    disk_read_speed = (current_disk_io.read_bytes - prev_disk_io.read_bytes) / time_diff
    disk_write_speed = (current_disk_io.write_bytes - prev_disk_io.write_bytes) / time_diff
    prev_disk_io = current_disk_io

    # 计算网络 IO
    current_net_io = psutil.net_io_counters()
    bytes_sent = current_net_io.bytes_sent
    bytes_recv = current_net_io.bytes_recv
    upload_speed = (bytes_sent - prev_net_io.bytes_sent) / time_diff
    download_speed = (bytes_recv - prev_net_io.bytes_recv) / time_diff
    prev_net_io = current_net_io
    prev_time = current_time

    return jsonify({
        'cpu_percent': cpu_percent,
        'cpu_freq': cpu_freq,
        'memory_percent': memory,
        'disk_percent': disk,
        'disk_read_speed': disk_read_speed,
        'disk_write_speed': disk_write_speed,
        'bytes_sent': bytes_sent,
        'bytes_recv': bytes_recv,
        'upload_speed': upload_speed,
        'download_speed': download_speed,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6090, debug=True)
