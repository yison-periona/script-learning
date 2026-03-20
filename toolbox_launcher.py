"""
toolbox_launcher.py
Double-click this exe to launch the File Toolbox
"""
import sys
import os
import webbrowser
import threading
import time

# 找到 toolbox_app.py 的真实路径
# PyInstaller 打包后文件在 _internal/ 里
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

app_path = os.path.join(base_path, "scripts", "toolbox_app.py")


def open_browser():
    time.sleep(4)
    webbrowser.open("http://localhost:8501")


threading.Thread(target=open_browser, daemon=True).start()

# 直接用 streamlit 的 Python 接口启动，而不是 subprocess
from streamlit.web import cli as stcli

sys.argv = [
    "streamlit", "run", app_path,
    "--server.headless", "true",
    "--global.developmentMode", "false"
]

stcli.main()
