from flask import Flask
import flask
from configuration import Config
from robot import Robot

app = Flask(__name__)
token = ''
robot_g: Robot
receiver_map = {}

@app.route('/')
def root():
    return "pong"

@app.route('/ping')
def ping():
    return "pong"

@app.route('/send-msg', methods=['post'])
def hello_world():
    print("请求过来", flask.request.json)
    if flask.request.json.get('token') in token:
        send_receiver = flask.request.json.get('send_receiver')
        at_receiver = flask.request.json.get('at_receiver')
        content = flask.request.json.get('content')
        #
        if (not receiver_map.get(send_receiver)) or not content:
            return {"code": 100, "message": "input error or receivers not registered", "data": None}
        # 判空
        if robot_g is None:
            return {"code": 101, "message": "server exception, unknown error occurred", "data": None}
        # 开始发送
        robot_g.sendTextMsg(content, receiver_map.get(send_receiver, ""), receiver_map.get(at_receiver, ""))
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
    global robot_g
    robot_g = robot
    # 启动服务
    app.run(port=c["port"], host=c["host"])
   


if __name__ == '__main__':
    app.run(port=5000, debug=True)
