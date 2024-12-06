from flask import Flask
import os
import platform
import sys

app = Flask(__name__)

@app.route('/hello')
def hello():
    # 获取操作系统信息
    os_info = platform.platform()
    # 获取Python版本
    python_version = platform.python_version()
    # 组装返回信息
    response = {
        'Operating System': os_info,
        'Python Version': python_version
    }
    return response

if __name__ == '__main__':
    app.run(debug=True)