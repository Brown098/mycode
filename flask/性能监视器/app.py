import psutil
import time
import os
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# 用于存储上一次的磁盘和网络IO数据
prev_disk_io = psutil.disk_io_counters()
prev_net_io = psutil.net_io_counters()
prev_time = time.time()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/app/metrics')
def metrics():
    global prev_disk_io, prev_net_io, prev_time

    # 获取当前时间和时间间隔
    current_time = time.time()
    time_diff = current_time - prev_time

    # 获取CPU使用率（百分比）
    cpu_percent = psutil.cpu_percent(interval=1)

    # 获取CPU频率
    cpu_freq = psutil.cpu_freq().current if hasattr(psutil, 'cpu_freq') and psutil.cpu_freq() else 0

    # 获取内存使用率
    memory = psutil.virtual_memory()
    memory_percent = memory.percent

    # 获取磁盘使用率（根分区）
    disk = psutil.disk_usage('/')
    disk_percent = disk.percent

    # 获取磁盘IO
    current_disk_io = psutil.disk_io_counters()
    disk_read_speed = (current_disk_io.read_bytes - prev_disk_io.read_bytes) / time_diff
    disk_write_speed = (current_disk_io.write_bytes - prev_disk_io.write_bytes) / time_diff
    prev_disk_io = current_disk_io

    # 获取网络IO
    current_net_io = psutil.net_io_counters()
    bytes_sent = current_net_io.bytes_sent
    bytes_recv = current_net_io.bytes_recv
    upload_speed = (bytes_sent - prev_net_io.bytes_sent) / time_diff
    download_speed = (bytes_recv - prev_net_io.bytes_recv) / time_diff
    prev_net_io = current_net_io

    # 更新上一次的时间
    prev_time = current_time

    # 获取当前时间戳
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    return jsonify({
        'cpu_percent': cpu_percent,
        'cpu_freq': cpu_freq,
        'memory_percent': memory_percent,
        'disk_percent': disk_percent,
        'disk_read_speed': disk_read_speed,
        'disk_write_speed': disk_write_speed,
        'bytes_sent': bytes_sent,
        'bytes_recv': bytes_recv,
        'upload_speed': upload_speed,
        'download_speed': download_speed,
        'timestamp': timestamp
    })


if __name__ == '__main__':
    # 创建静态文件目录
    os.makedirs('static', exist_ok=True)

    # 创建favicon.ico文件（可选）
    with open('static/favicon.ico', 'wb') as f:
        pass

    app.run(host="127.0.0.1", port=6090, debug=True)