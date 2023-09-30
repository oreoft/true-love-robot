#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json


class SearchTask():
    def __init__(self) -> None:
        print("SearchTask start...")

    def do_search(self, question: str) -> str:
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

if __name__ == "__main__":
    from configuration import Config
    c = Config()
    searchTask = SearchTask()
    rsp = searchTask.do_search("查询美元汇率")
    print(rsp)
