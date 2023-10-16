from flask import Flask
import flask
from configuration import Config
from robot import Robot

app = Flask(__name__)
token = ''
robot_g: Robot
receiver_map = {}
group_map = {}

@app.route('/send-msg', methods=['post'])
def hello_world():
    if flask.request.json.get('token') in token:
        send_group = flask.request.json.get('send_group')
        send_receiver = flask.request.json.get('send_receiver')
        content = flask.request.json.get('content')
        # 为了保证安全这里还有一层转换
        if (not group_map.get(send_group) and not receiver_map.get(send_receiver)) or not content:
            return {"code": 100, "message": "input error or receivers not registered", "data": None}
        # 判空
        if robot_g is None:
            return {"code": 101, "message": "server exception, unknown error occurred", "data": None}
        # 开始发送
        robot_g.sendTextMsg(content, send_group, send_receiver)
        return {"code": 0, "message": "success", "data": None}
    return {"code": 103, "message": "failed token check", "data": None}


def enableHTTP(config: Config, robot: Robot):
    """暴露 HTTP 发送消息接口供外部调用，不配置则忽略"""
    c = config.HTTP
    if not c:
        return

    # 配置赋值
    global token
    token = c["token"]
    global receiver_map
    receiver_map = c["receiver_map"]
    global group_map
    group_map = c["group_map"]

    # 启动服务
    app.run(c["port"], c["host"])
    global robot_g
    robot_g = robot


if __name__ == '__main__':
    app.run(port=5000, debug=True)
