#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime

import openai
import time
import requests
from bs4 import BeautifulSoup
import json


class ChatGPT():

    def __init__(self, config) -> None:
        self.config = config
        # 自己搭建或第三方代理的接口
        openai.api_base = config.get("api")
        # 代理
        proxy = config.get("proxy")
        if proxy:
            openai.proxy = {"http": proxy, "https": proxy}
        self.conversation_list = {}
        self.system_content_msg = {"role": "system", "content": config.get("prompt")}
        self.system_content_msg2 = {"role": "system", "content": config.get("prompt2")}
        # 轮训负载key的计数器
        self.count = 0

    def get_answer(self, question: str, wxid: str, sender: str) -> str:
        # 特殊逻辑
        if question.startswith('查询'):
            if '大鹏签证' in question:
                return self.reqQianzheng()
            if '美元汇率' in question:
                return self.searchMeiyuan()
            if '图书馆时间' in question:
                return self.librarySchedule()
            if '大鹏物流' in question:
                return self.reqWuliu('https://trace.fkdex.com/sf/SF1388111071920:0069')
            if '测试物流' in question:
                return self.reqWuliu('https://trace.fkdex.com/sf/SF1420456743485:8020')
            return '该查询任务无法找到'
            
        # 走chatgpt wxid或者roomid,个人时为微信id，群消息时为群id
        self.updateMessage(wxid, question.replace("debug", "", 1), "user")
        self.count += 1
        cases = {
            0: self.config.get("key1"),
            1: self.config.get("key2"),
            2: self.config.get("key3"),
        }
        real_key = cases.get(self.count % 3, self.config.get("key1"))
        real_model = "gpt-3.5-turbo"
        # 如果是有权限访问gpt4的，直接走gpt4
        if sender in self.config.get("gpt4") and ('gpt4' in question or 'GPT4' in question):
            real_key = self.config.get("key2")
            real_model="gpt-4"
        openai.api_key = real_key
        rsp = ''
        start_time = time.time()
        print("开始发送给chatgpt， 其中real_key: ", real_key[-4:], " real_model: ", real_model)
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
            return rsp + '\n\n' + '(cost: ' + str(cost) + 's, use: ' + real_key[-4:] + ', model: ' + real_model + ')'
        else:
            return rsp
        
    def reqQianzheng(self) -> str:
        url = "https://www.visa.go.kr/openPage.do?MENU_ID=10301"
        payload = 'CMM_TEST_VAL=test&sBUSI_GB=PASS_NO&sBUSI_GBNO=EK1772377&ssBUSI_GBNO=EK1772377&pRADIOSEARCH=gb03&sEK_NM=HUANG%20PENG&sFROMDATE=1997-02-08&sMainPopUpGB=main&TRAN_TYPE=ComSubmit&SE_FLAG_YN=&LANG_TYPE=CH'
        headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'WMONID=gAoIK87q47a; JSESSIONID_evisa=0mWRZ9reCxvtPoMunNqR0GIdERVSDyMyL3U6aZV1zzd8fiaVx7JzOCXyHkotCmvP.evisawas2_servlet_EVISA; JSESSIONID_evisa=CpdiyMfA7J47vNdcGvYd9wkcWq4j4TMTLCeXVkqVz3P4l0YVxvvdxybUPSCWizmP.evisawas2_servlet_EVISA',
        'Origin': 'https://www.visa.go.kr',
        'Pragma': 'no-cache',
        'Referer': 'https://www.visa.go.kr/openPage.do?MENU_ID=10301',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        soup = BeautifulSoup(response.text, features="html.parser")
        return soup.find(id="PROC_STS_CDNM_1").text.strip()
    
    def librarySchedule(self) -> str:
        url = "https://library.iit.edu/"
        payload = {}
        headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'apt.uid=AP-PQQY5YJEHTTA-2-1658549780581-31137818.0.2.ed40e09e-bd68-416d-828a-5465e6efefca',
        'Pragma': 'no-cache',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        soup = BeautifulSoup(response.text.replace('View the full library schedule', ''), 'html.parser')
        result = soup.find('div', {'class': 'views-row'}).text
        return result.strip()

    
    def reqWuliu(self, url) -> str:
        payload = {}
        headers = {
        'authority': 'trace.fkdex.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'origin': 'https://www.ickd.cn',
        'pragma': 'no-cache',
        'referer': 'https://www.ickd.cn/',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        res = json.loads(response.text)
        data = res['data']
        if len(data) <= 0:
            return '运单未揽收或寄件时间超过3个月，请稍后再试试捏'
        else:
            return json.dumps(data, indent=4, ensure_ascii=False)
        
    def searchMeiyuan(self) -> str:
        url = "https://srh.bankofchina.com/search/whpj/search_cn.jsp"
        payload = 'erectDate=&nothing=&pjname=%E7%BE%8E%E5%85%83&head=head_620.js&bottom=bottom_591.js'
        headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'JSESSIONID=00001CdOkfmL1j6G9cXi9ak2N4F:-1',
        'Origin': 'https://srh.bankofchina.com',
        'Pragma': 'no-cache',
        'Referer': 'https://srh.bankofchina.com/search/whpj/search_cn.jsp',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        s = BeautifulSoup(response.text, features="html.parser").text
        s1 = s.strip().split('美元')[2].strip().replace(' ', '')
        # print(s1)
        arr = s1.split('\n')
        str = '现汇买入价:' + arr[0].strip() + ',\n现钞买入价:' + arr[2].strip() + ',\n现汇卖出价:' + arr[4].strip() + ',\n现钞卖出价:' + arr[6].strip() + ',\n中行折算价:' + arr[8].strip() + ',\n发布时间:' + arr[10].strip()
        return str


    def updateMessage(self, wxid: str, question: str, role: str) -> None:
        now_time = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        time_mk = "当需要回答时间时请直接参考回复:"
        # 初始化聊天记录,组装系统信息
        if wxid not in self.conversation_list.keys():
            question_ = [
                self.system_content_msg if wxid not in self.config.get("gpt4") else self.system_content_msg2,
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
    chat = ChatGPT(config)
    # 测试程序
    while True:
        q = input(">>> ")
        try:
            time_start = datetime.now()  # 记录开始时间
            print(chat.get_answer(q, "wxid_tqn5yglpe9gj21", "wxid_tqn5yglpe9gj21"))
            time_end = datetime.now()  # 记录结束时间
            print(f"{round((time_end - time_start).total_seconds(), 2)}s")  # 计算的时间差为程序的执行时间，单位为秒/s
        except Exception as e:
            print(e)
