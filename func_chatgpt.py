#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime

import openai
import time


class ChatGPT():

    def __init__(self, key: str, api: str, proxy: str, prompt: str) -> None:
        openai.api_key = key
        # 自己搭建或第三方代理的接口
        openai.api_base = api
        if proxy:
            openai.proxy = {"http": proxy, "https": proxy}
        self.conversation_list = {}
        self.system_content_msg = {"role": "system", "content": prompt}
        self.count = 0

    def get_answer(self, question: str, wxid: str, sender: str, config) -> str:
        # wxid或者roomid,个人时为微信id，群消息时为群id
        self.updateMessage(wxid, question.replace("debug", "", 1), "user")
        self.count += 1
        cases = {
            0: config.get("key1"),
            1: config.get("key2"),
            2: config.get("key3"),
        }
        real_key = cases.get(self.count % 3, config.get("key1"))
        real_model = "gpt-3.5-turbo"
        # 如果是有权限访问gpt4的，直接走gpt4
        if sender in config.get("gpt4"): 
            real_key=config.get("key2")
            real_model="gpt-4"
        openai.api_key = real_key
        rsp = ''
        start_time = time.time()
        try:
            ret = openai.ChatCompletion.create(
                model=real_model,
                messages=self.conversation_list[wxid],
                temperature=0.2
            )

            rsp = ret["choices"][0]["message"]["content"]
            rsp = rsp[2:] if rsp.startswith("\n\n") else rsp
            rsp = rsp.replace("\n\n", "\n")
            self.updateMessage(wxid, rsp, "assistant")
        except openai.error.AuthenticationError as e1:
            rsp = "OpenAI API 认证失败，请联系纯路人"
        except openai.error.APIConnectionError as e2:
            rsp = "啊哦~，可能内容太长搬运超时，再试试捏"
        except openai.error.Timeout as e3:
            rsp = "啊哦~，可能内容太长搬运超时，再试试捏"
        except openai.error.RateLimitError as e4:
            rsp = "你们问的太快了，回答不过来啦，得再问一遍哦"
        except openai.error.APIError as e5:
            rsp = "OpenAI API 返回了错误：" + str(e5)
        except Exception as e0:
            rsp = "发生未知错误：" + str(e0)

        # print(self.conversation_list[wxid])
        end_time = time.time()
        cost = round(end_time - start_time, 2)
        print("chat回答时间为：", cost, "秒")
        if question.startswith('debug'):
            return rsp + '\n\n' + '(cost: ' + str(cost) + 's, use: ' + real_key[-4:] + ', model:' + real_model + ')'
        else:
            return rsp

    def updateMessage(self, wxid: str, question: str, role: str) -> None:
        now_time = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        time_mk = "当需要回答时间时请直接参考回复:"
        # 初始化聊天记录,组装系统信息
        if wxid not in self.conversation_list.keys():
            question_ = [
                self.system_content_msg,
                {"role": "system", "content": "" + time_mk + now_time}
            ]
            self.conversation_list[wxid] = question_

        # 当前问题
        content_question_ = {"role": role, "content": question}
        self.conversation_list[wxid].append(content_question_)

        for cont in self.conversation_list[wxid]:
            if cont["role"] != "system":
                continue
            if cont["content"].startswith(time_mk):
                cont["content"] = time_mk + now_time

        # 只存储10条记录，超过滚动清除
        i = len(self.conversation_list[wxid])
        if i > 5:
            print("滚动清除微信记录：" + wxid)
            # 删除多余的记录，倒着删，且跳过第一个的系统消息
            del self.conversation_list[wxid][1]


if __name__ == "__main__":
    from configuration import Config
    config = Config().CHATGPT
    if not config:
        exit(0)
    api = config.get("api")
    proxy = config.get("proxy")
    prompt = config.get("prompt")

    chat = ChatGPT(config.get("key1"), api, proxy, prompt)

    while True:
        q = input(">>> ")
        try:
            time_start = datetime.now()  # 记录开始时间
            # print(chat.get_answer(q, "wxid", "wxid"), config)
            time_end = datetime.now()  # 记录结束时间

            print(f"{round((time_end - time_start).total_seconds(), 2)}s")  # 计算的时间差为程序的执行时间，单位为秒/s
        except Exception as e:
            print(e)
