#!/usr/bin/env python3
# main.py — 时间锁定入口（安全合规）
from datetime import datetime, timezone
import sys
import requests   # 可选依赖，仅当启用 online_time_check=True 时需要
from PyQt6.QtWidgets import QApplication, QMessageBox
from pathlib import Path


from main_1 import MainWindow
# ---- 配置 ----
EXPIRE_DATE = datetime(2025, 12, 31, tzinfo=timezone.utc)  # 到期当日 00:00 UTC 后不可用（可按需改）
ONLINE_TIME_CHECK = True   # True 尝试使用在线时间服务（更可靠），False 则只用本地时间
ONLINE_TIME_URL = "http://worldtimeapi.org/api/timezone/Etc/UTC"  # 公开 HTTP 接口示例
ONLINE_TIMEOUT = 5  # seconds
ALLOW_CLOCK_DRIFT_SECONDS = 60  # 容忍少量网络/时钟误差

# ---- 你的程序入口（替换为你实际的 GUI 启动函数） ----
def start_application():

    window = MainWindow()
    window.show()

    return window

# ---- 时间获取与校验 ----
def get_local_utc_now():
    return datetime.now(timezone.utc)

def get_online_utc_now():
    """
    尝试从世界时间 API 获取当前 UTC 时间。
    返回 datetime（UTC）或 None（失败）。
    """
    try:
        resp = requests.get(ONLINE_TIME_URL, timeout=ONLINE_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        # worldtimeapi 返回 'unixtime' 或 'datetime'
        if "unixtime" in data:
            ts = int(data["unixtime"])
            return datetime.fromtimestamp(ts, timezone.utc)
        elif "datetime" in data:
            # 格式如 "2025-11-10T23:35:01.123456+00:00"
            return datetime.fromisoformat(data["datetime"]).astimezone(timezone.utc)
    except Exception:
        return None

def is_expired(online_check=ONLINE_TIME_CHECK):
    """
    返回 (expired: bool, used_online: bool, checked_time: datetime)
    """
    now_local = get_local_utc_now()
    checked_time = now_local
    used_online = False

    if online_check:
        online_now = get_online_utc_now()
        if online_now:
            used_online = True
            checked_time = online_now
        else:
            # 在线获取失败：继续使用本地时间（可记录日志）
            checked_time = now_local

    expired = checked_time >= EXPIRE_DATE
    return expired, used_online, checked_time

# ---- 用户提示（GUI） ----
def show_expired_message_and_exit(checked_time, used_online):
    msg = QMessageBox()
    msg.setWindowTitle("程序已过期")
    reason = "（网络时间）" if used_online else "（本机时间）"
    msg.setText(f"程序已过期，当前时间 {checked_time.isoformat()} {reason}，请联系开发者获取更新版本。")
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.exec()
    sys.exit(0)

# ---- 主流程 ----
def main():
    app = QApplication(sys.argv)

    # 校验到期
    expired, used_online, checked_time = is_expired(online_check=ONLINE_TIME_CHECK)

    if expired:
        show_expired_message_and_exit(checked_time, used_online)

    # 若未过期，启动主程序（例如你的 PyQt 窗口）
    main_window = start_application()

    # 运行事件循环
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
