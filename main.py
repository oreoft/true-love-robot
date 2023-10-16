#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import signal

from wcferry import Wcf

import server
from configuration import Config
from robot import Robot


def weather_report(robot: Robot) -> None:
    """模拟发送天气预报
    """

    # 获取接收人
    receivers = ["filehelper"]

    # 获取天气，需要自己实现，可以参考 https://gitee.com/lch0821/WeatherScrapy 获取天气。
    report = "这就是获取到的天气情况了"

    for r in receivers:
        robot.sendTextMsg(report, r)
        # robot.sendTextMsg(report, r, "nofity@all")   # 发送消息并@所有人


def main():
    config = Config()
    wcf = Wcf(debug=True)

    def handler(sig, frame):
        wcf.cleanup()  # 退出前清理环境
        exit(0)

    signal.signal(signal.SIGINT, handler)

    robot = Robot(config, wcf)
    robot.LOG.info("正在启动机器人···")

    # 机器人启动发送测试消息
    robot.sendTextMsg("真爱粉启动成功！", "wxid_tqn5yglpe9gj21")

    # 接收消息
    # robot.enableRecvMsg()     # 可能会丢消息？
    robot.enableReceivingMsg()  # 加队列

    # 启用http监听
    server.enableHTTP(config, robot)

    # 每天 7 点发送天气预报
    # robot.onEveryTime("07:00", weather_report, robot=robot)

    # 每天 7:30 发送新闻
    # robot.onEveryTime("07:30", robot.newsReport)

    # 每班小时查询汇率
    robot.onEveryTime(["10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30", "20:00", "20:30", "21:00", "21:30", "22:00"], robot.noticeMeiyuan)
    # robot.onEverySeconds(30, robot.noticeMeiyuan)
    # robot.onEverySeconds(30, robot.noticeLibraryschedule)
    robot.onEveryTime("07:00", robot.noticeLibraryschedule)

    # 让机器人一直跑
    robot.keepRunningAndBlockProcess()


if __name__ == "__main__":
    main()
