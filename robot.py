# -*- coding: utf-8 -*-

import logging
import os
import re
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from queue import Empty
from threading import Thread

from wcferry import Wcf, WxMsg

from configuration import Config
from func_chatgpt import ChatGPT
from func_chengyu import cy
from func_claude import Claude
from func_news import News
from func_search import SearchTask
from func_task import RunTask
from func_tigerbot import TigerBot
from job_mgmt import Job


class Robot(Job):
    """个性化自己的机器人
    """

    def __init__(self, config: Config, wcf: Wcf) -> None:
        self.wcf = wcf
        self.config = config
        self.LOG = logging.getLogger("Robot")
        self.wxid = self.wcf.get_self_wxid()
        self.allContacts = self.getAllContacts()
        self.searchTask = SearchTask()
        self.runTask = RunTask(self.config.GITHUB)
        self.claude = None
        if self.config.CLAUDE:
            self.claude = Claude(self.config.CLAUDE)
        # 选择当前默认的语言模型
        enable_bot = self.config.ENABLE_BOT
        if 'chatgpt' == enable_bot:
            self.chat = ChatGPT(self.config.CHATGPT)
        elif 'claude' == enable_bot:
            self.chat = self.claude
        elif 'tigerbot' == enable_bot:
            self.chat = TigerBot(self.config.TIGERBOT)
        else:
            self.chat = None

    def toAt(self, msg: WxMsg) -> bool:
        """处理被 @ 消息
        :param msg: 微信消息结构
        :return: 处理状态，`True` 成功，`False` 失败
        """
        return self.toChitchat(msg)

    def toChengyu(self, msg: WxMsg) -> bool:
        """
        处理成语查询/接龙消息
        :param msg: 微信消息结构
        :return: 处理状态，`True` 成功，`False` 失败
        """
        status = False
        texts = re.findall(r"^([#|?|？])(.*)$", msg.content)
        # [('#', '天天向上')]
        if texts:
            flag = texts[0][0]
            text = texts[0][1]
            if flag == "#":  # 接龙
                if cy.isChengyu(text):
                    rsp = cy.getNext(text)
                    if rsp:
                        self.sendTextMsg(rsp, msg.roomid)
                        status = True
            elif flag in ["?", "？"]:  # 查词
                if cy.isChengyu(text):
                    rsp = cy.getMeaning(text)
                    if rsp:
                        self.sendTextMsg(rsp, msg.roomid)
                        status = True

        return status

    def toChitchat(self, msg: WxMsg) -> bool:
        """闲聊，接入 ChatGPT
        """
        q = re.sub(r"@.*?[\u2005|\s]", "", msg.content).replace(" ", "")
        if q.startswith('查询'):  # 如果是特殊任务
            self.LOG.info(f"收到:{msg.sender}, 查询任务:{q}")
            rsp = self.searchTask.do_search(q)
        elif q.startswith('执行'):
            self.LOG.info(f"收到:{msg.sender}, 执行任务:{q}")
            rsp = self.runTask.do_run(q, msg.sender)
        elif q.startswith('claude') and self.claude:  # 如果是claude并且不为空
            rsp = self.claude.get_answer(q, (msg.roomid if msg.from_group() else msg.sender), msg.sender)
        elif not self.chat:  # 没接 ChatGPT，固定回复
            rsp = "你@我干嘛？"
        else:
            rsp = self.chat.get_answer(q, (msg.roomid if msg.from_group() else msg.sender), msg.sender)

        # 判断返回值
        if rsp:
            if msg.from_group():
                self.sendTextMsg(rsp, msg.roomid, msg.sender)
            else:
                self.sendTextMsg(rsp, msg.sender)
            return True
        else:
            self.LOG.error(f"无法从 ChatGPT 获得答案")
            return False

    def job_wuliu(self):
        roomId = '35053039913@chatroom'
        sender = 'wxid_xtbtinq9kbvf21'
        rsp = self.searchTask.do_search("查询大鹏物流")
        self.sendTextMsg(
            "定时查询的大鹏物流信息结果为： " + '\n \n' + rsp + '\n \n (间隔半小时自动查询，晚十至早十期间静默)', roomId,
            sender)
        return True

    def noticeMeiyuan(self):
        roomId = '35053039913@chatroom'
        sender = 'wxid_tqn5yglpe9gj21'
        rsp = self.searchTask.do_search("查询美元汇率")
        numbers = re.findall('\d+\.\d+|\d+', rsp)
        print(numbers)
        if len(numbers) > 2 and float(numbers[2]) <= 725:
            print()
            # self.sendTextMsg("提醒现在的美元汇率情况低于725：\n" + rsp, roomId, sender)
        return True

    def noticeLibraryschedule(self):
        roomId = '39094040348@chatroom'
        # roomId = '2666401439@chatroom'
        sender = ''
        rsp = self.searchTask.do_search("查询图书馆时间")
        rsp2 = self.searchTask.do_search("查询美元汇率")
        rsp3 = self.searchTask.do_search("查询gym时间")
        msg = "早上好☀️宝子们，\n\n"
        if rsp != "": msg = msg + "今日图书馆情况：\n" + rsp + "\n\n"
        if rsp3 != "": msg = msg + "今日gym情况：\n" + rsp3 + "\n\n"
        if rsp2 != "": msg = msg + "今日汇率情况：\n" + rsp2

        "\n\n今日汇率情况：\n" + rsp2
        self.sendTextMsg(msg, roomId, sender)
        return True

    def noticeAoYuanschedule(self):
        roomId = '39121926591@chatroom'
        # roomId = '2666401439@chatroom'
        sender = ''
        rsp = self.searchTask.do_search("查询澳币汇率")
        rsp2 = self.searchTask.do_search("查询美元汇率")
        msg = "早上好☀️宝宝，\n\n"
        if rsp != "": msg = msg + "今日澳币汇率情况：\n" + rsp + "\n\n"
        if rsp != "": msg = msg + "今日美元汇率情况：\n" + rsp2
        self.sendTextMsg(msg, roomId, sender)
        return True

    def noticeMoyuSchedule(self):
        roomIdDachang = '20923342619@chatroom'
        roomIdB = '34977591657@chatroom'
        roomIdLiu = '39295953189@chatroom'
        roomIdWuhan = '20624707540@chatroom'

        self.sendDailyNotice(roomIdDachang)
        self.sendDailyNotice(roomIdB)
        self.sendDailyNotice(roomIdLiu)
        self.sendDailyNotice(roomIdWuhan)
        return True

    def noticeCardSchedule(self):
        roomId = '39190072732@chatroom'
        # roomId = '2666401439@chatroom'
        card_user: dict = self.config.GITHUB['card_user']
        msg = "今日结余一览\n\n"
        result = self.runTask.queryCafeteriaCardRecordAll()
        for key, value in card_user.items():
            try:
                msg += key + '\n' + result[value] + '\n\n'
            except KeyError:
                pass
        self.sendTextMsg(msg, roomId)
        return True

    def sendDailyNotice(self, roomId):
        moyu_dir = os.path.dirname(os.path.abspath(__file__)) + '/moyu-jpg/' + datetime.now().strftime(
            '%m-%d-%Y') + '.jpg'
        zaobao_dir = os.path.dirname(os.path.abspath(__file__)) + '/zaobao-jpg/' + datetime.now().strftime(
        '%m-%d-%Y') + '.jpg'

        self.sendTextMsg('早上好☀️家人萌~', roomId, '')
        moyuRes = self.wcf.send_image(moyu_dir, roomId)
        zaobaoRes = self.wcf.send_image(zaobao_dir, roomId)
        self.LOG.info(f"send_image: {moyuRes}")
        self.LOG.info(f"send_image: {zaobaoRes}")

    def processMsg(self, msg: WxMsg) -> None:
        """当接收到消息的时候，会调用本方法。如果不实现本方法，则打印原始消息。
        此处可进行自定义发送的内容,如通过 msg.content 关键字自动获取当前天气信息，并发送到对应的群组@发送者
        群号：msg.roomid  微信ID：msg.sender  消息内容：msg.content
        content = "xx天气信息为："
        receivers = msg.roomid
        self.sendTextMsg(content, receivers, msg.sender)
        """

        # 群聊消息
        if msg.from_group():
            # 如果在群里被 @
            if msg.roomid not in self.config.GROUPS:  # 不在配置的响应的群列表里，忽略
                return

            if msg.is_at(self.wxid):  # 被@
                self.toAt(msg)

            else:  # 其他消息
                self.toChengyu(msg)

            return  # 处理完群聊信息，后面就不需要处理了

        # 非群聊信息，按消息类型进行处理
        if msg.type == 37:  # 好友请求
            self.autoAcceptFriendRequest(msg)

        elif msg.type == 10000:  # 系统信息
            self.sayHiToNewFriend(msg)

        elif msg.type == 0x01:  # 文本消息
            # 让配置加载更灵活，自己可以更新配置。也可以利用定时任务更新。
            if msg.from_self():
                if msg.content == "^更新$":
                    self.config.reload()
                    self.LOG.info("已更新")
            else:
                if msg.sender not in self.config.PRI:
                    print("收到私聊, 消息进行过滤")
                    return
                else:
                    self.toChitchat(msg)  # 闲聊

    def onMsg(self, msg: WxMsg) -> int:
        try:
            self.LOG.info(msg)  # 打印信息
            self.processMsg(msg)
        except Exception as e:
            self.LOG.error(e)

        return 0

    def enableRecvMsg(self) -> None:
        self.wcf.enable_recv_msg(self.onMsg)

    def enableReceivingMsg(self) -> None:
        def innerProcessMsg(wcf: Wcf):
            while wcf.is_receiving_msg():
                try:
                    msg = wcf.get_msg()
                    self.LOG.info(msg)
                    self.processMsg(msg)
                except Empty:
                    continue  # Empty message
                except Exception as e:
                    self.LOG.error(f"Receiving message error: {e}")

        self.wcf.enable_receiving_msg()
        Thread(target=innerProcessMsg, name="GetMessage", args=(self.wcf,), daemon=True).start()

    def sendTextMsg(self, msg: str, receiver: str, at_list: str = "") -> None:
        """ 发送消息
        :param msg: 消息字符串
        :param receiver: 接收人wxid或者群id
        :param at_list: 要@的wxid, @所有人的wxid为：nofity@all
        """
        # msg 中需要有 @ 名单中一样数量的 @
        ats = ""
        if at_list:
            wxids = at_list.split(",")
            for wxid in wxids:
                # 这里偷个懒，直接 @昵称。有必要的话可以通过 MicroMsg.db 里的 ChatRoom 表，解析群昵称
                ats += f" @{self.allContacts.get(wxid, '')}"

        # {msg}{ats} 表示要发送的消息内容后面紧跟@，例如 北京天气情况为：xxx @张三，微信规定需这样写，否则@不生效
        if ats == "":
            self.LOG.info(f"To {receiver}: {msg}")
            self.wcf.send_text(f"{msg}", receiver, at_list)
        else:
            self.LOG.info(f"To {receiver}: {ats}\r{msg}")
            self.wcf.send_text(f"{ats}\n\n{msg}", receiver, at_list)

    def getAllContacts(self) -> dict:
        """
        获取联系人（包括好友、公众号、服务号、群成员……）
        格式: {"wxid": "NickName"}
        """
        contacts = self.wcf.query_sql("MicroMsg.db", "SELECT UserName, NickName FROM Contact;")
        return {contact["UserName"]: contact["NickName"] for contact in contacts}

    def keepRunningAndBlockProcess(self) -> None:
        """
        保持机器人运行，不让进程退出
        """
        while True:
            self.runPendingJobs()
            time.sleep(1)

    def autoAcceptFriendRequest(self, msg: WxMsg) -> None:
        try:
            xml = ET.fromstring(msg.content)
            v3 = xml.attrib["encryptusername"]
            v4 = xml.attrib["ticket"]
            scene = int(xml.attrib["scene"])
            self.wcf.accept_new_friend(v3, v4, scene)

        except Exception as e:
            self.LOG.error(f"同意好友出错：{e}")

    def sayHiToNewFriend(self, msg: WxMsg) -> None:
        nickName = re.findall(r"你已添加了(.*)，现在可以开始聊天了。", msg.content)
        if nickName:
            # 添加了好友，更新好友列表
            self.allContacts[msg.sender] = nickName[0]
            self.sendTextMsg(f"Hi {nickName[0]}，我自动通过了你的好友请求。", msg.sender)

    def newsReport(self) -> None:
        receivers = self.config.NEWS
        if not receivers:
            return

        news = News().get_important_news()
        for r in receivers:
            self.sendTextMsg(news, r)
