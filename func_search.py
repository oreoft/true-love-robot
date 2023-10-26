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
        if '澳币汇率' in question:
            return self.searchAoyuan()
        if '图书馆时间' in question:
            return self.librarySchedule()
        if '大鹏物流' in question:
            return self.reqWuliu('https://trace.fkdex.com/sf/SF1388111071920:0069')
        if '测试物流' in question:
            return self.reqWuliu('https://trace.fkdex.com/sf/SF1420456743485:8020')
        if 'gym时间' in question:
            return self.gymSchedule()
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

    def searchAoyuan(self) -> str:
        url = "https://srh.bankofchina.com/search/whpj/search_cn.jsp"
        payload = 'erectDate=&nothing=&pjname=%E6%BE%B3%E5%A4%A7%E5%88%A9%E4%BA%9A%E5%85%83&head=head_620.js&bottom=bottom_591.js'
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
        s1 = s.strip().split('澳大利亚元')[2].strip().replace(' ', '')
        # print(s1)
        arr = s1.split('\n')
        str = '现汇买入价:' + arr[0].strip() + ',\n现钞买入价:' + arr[2].strip() + ',\n现汇卖出价:' + arr[4].strip() + ',\n现钞卖出价:' + arr[6].strip() + ',\n中行折算价:' + arr[8].strip() + ',\n发布时间:' + arr[10].strip()
        return str

    def gymSchedule(self):
        url = "https://www.google.com/search?gl=us&tbm=map&q=Keating+Sports+Center%2C+Keating+Sports+Center%2C+South+Wabash+Avenue%2C+Chicago%2C+IL&nfpr=1&pb=!4m8!1m3!1d2771.238802426475!2d-87.6255606!3d41.8390215!3m2!1i375!2i358!4f13.1!7i20!10b1!12m14!1m1!18b1!17m4!1e1!1e0!3e1!3e0!20m5!1e0!2e3!3b0!5e2!6b1!26b1!19m4!2m3!1i335!2i120!4i8!20m35!3m1!2i9!6m6!1m2!1i375!2i124!1m2!1i622!2i75!7m24!1m3!1e1!2b0!3e3!1m3!1e2!2b1!3e2!1m3!1e2!2b0!3e3!1m3!1e8!2b0!3e3!1m3!1e10!2b0!3e3!1m3!1e10!2b1!3e2!9b0!22m7!4m1!2i22236!7e140!9sqKEsZfqKF4Ls9AOftpCACA%3A972177539594!17sqKEsZfqKF4Ls9AOftpCACA%3A972177539595!24m1!2e1!24m29!1m2!18m1!17b1!4b1!11m2!3e1!3e0!17b1!20m2!1e3!1e1!24b1!29b1!71b1!72m13!1m5!1b1!2b1!3b1!5b1!7b1!4b0!8m4!1m2!4m1!1e1!3sother_user_reviews!9b1!89b1!26m7!1e12!1e15!1e13!1e3!2m2!1i80!2i80!28sBChIJV9cIunMsDogRqx7m556ious%3D!34m5!9b1!12b1!14b1!25b1!26b1!37m1!1e140!49m3!6m2!1b1!2b1!69i666"
        headers = {
            'authority': 'www.google.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'cookie': '__Secure-ENID=14.SE=FC2qRULD__5u7__26INUS64KUKuHoseORxcwiGLXr4hsXlEDPRaZsbeOyaeeuyC3QA17vab89_k3CRmKavFEypyF0Gnz-kOePuG-1obBLnpPBLYmVc-k6tM_9a0dsAZlndMlQ1y3V3OR15emwmO_36NsiM8Y9X19YulV1RbRB9oF3GTo8AG5q_T67oozEwytvzAwwctDHL_Oh85vBa57LXNvuZfZPim3MAYZX5mPlA; SEARCH_SAMESITE=CgQInZkB; OTZ=7241613_76_80_104160_76_446820; SID=bwhFnPKpdTfZlOIaMyheOMgvmXsvVZjxmE4U9T6ovj3QZE5S5hlVbKgbijLO-T_DBfTcuA.; __Secure-1PSID=bwhFnPKpdTfZlOIaMyheOMgvmXsvVZjxmE4U9T6ovj3QZE5SPOdjIRmHj3m9syyi5Qbg3A.; __Secure-3PSID=bwhFnPKpdTfZlOIaMyheOMgvmXsvVZjxmE4U9T6ovj3QZE5Si4lEMv4Pureup3aR6tUMBw.; HSID=ASlHas32EfTOY8X5d; SSID=ApGeObnA1twoY0v_4; APISID=3Bmo_ywS8iRd1l5C/A9bxlaH-ndg5dl16R; SAPISID=H1a6cKaMiLIUIyFw/AbmSPm3XchL2ap9yi; __Secure-1PAPISID=H1a6cKaMiLIUIyFw/AbmSPm3XchL2ap9yi; __Secure-3PAPISID=H1a6cKaMiLIUIyFw/AbmSPm3XchL2ap9yi; AEC=Ackid1QpfdClOxA5yIoYsqcIyYUCh4FOHo478sZ_-aSevD5wCf3PRcCCaQ; __Secure-1PSIDTS=sidts-CjEB3e41hfVK1HzRxsNOm1Og6AY5CdiCJj1yi0nU4cBtKJ9qNdLbr4pB2yMuNl2wOmGlEAA; __Secure-3PSIDTS=sidts-CjEB3e41hfVK1HzRxsNOm1Og6AY5CdiCJj1yi0nU4cBtKJ9qNdLbr4pB2yMuNl2wOmGlEAA; 1P_JAR=2023-10-16-02; NID=511=QbuyF_QzXwr3qn5YRP8IgB97kTXfsOSJ7JcRc0IvivdweRsTpZ166AG8r4L4RS_MT2QbCBc99ZHSG-hU4BhbuahlnhVkykrsykdbz3H52pVGG8Y8DVZIEW9oYbgGBbduJFS6DeYbgI3APKtyyq0DpiZxw4YDwApFR8gzCDUZ5dUfzgC8c3GOJK6Jq88xxqr1pIIxfCg96UjNy_gkywrnMZxURhpXWFawXTGAhIB4b4VgAZRIpDuP9uBeC-h_IKA4LXFjm2I1MA0yVFIvS7QwvP82KeFD93io2sLHZwvRA1CryA3rAWHiyfADHdpfL9Osr_06eNet_kOae-3wvLX2RXauixfBvLlu16L0nS9ohnhTYEFdhFXT5gaDJdkUeUGS4ZtTTDw1e4RUdOB3RSHJ-MObxXEUAKEOTgwOemy5_bZHfclj4cGueX1dm9EYwXOj_m-xx7uHCqiHYlAWmTyeqsksqo20bg; UULE=a+cm9sZTogMQpwcm9kdWNlcjogMTIKdGltZXN0YW1wOiAxNjk3NDIzNjA2NDA3MDAwCmxhdGxuZyB7CiAgbGF0aXR1ZGVfZTc6IDQxODM5Mjk1MwogIGxvbmdpdHVkZV9lNzogLTg3NjMyMjI4Ngp9CnJhZGl1czogNzkyOS43OTk5OTk5OTk5OTkKcHJvdmVuYW5jZTogNgo=; DV=w0yvKC1WL7JScFlM3f0m-VxWuFxlsxhEH2Srbk0ZhAIAACBNtrgAGKFRogAAADCMjMj12f1CMgAAAJM3qZ5ZrMvnHAAAAA; SIDCC=ACA-OxO54e-CU497X8SNiSpFymhdiWfA392kattkDPKAWtxPTqrkc4lcxfFrM4dAXhtJj23ceg; __Secure-1PSIDCC=ACA-OxNNowVLHJzdPwrP_bTugJg6dkoWhBRFNZJqYcixeYJhXjhvagVXD4FzeNrKiBG2waZIJg; __Secure-3PSIDCC=ACA-OxNgJIG31RNaItQnPfcMTXbnfO7ehnD9B2D14hUw7eh-7xmbr5UpAtbf23AjRZf9BghJi3zf; NID=511=fzxKPVchSxziwf1_TJiEKWVYOpJRRpVMn4D3LTrxeczHV14x2mKQOv9AWJZ9ZAOz166fljOmQnYdqwYlDOg5Qx5OlVJ4Bnki5uFFCq1JELoIO8UIrC_KydWAbjdl8UnqS6PXuV9y4pqlNpr-5UYptVxoS7olwHibx4QwgN2rZgoo7IwB3FaGrnWTuopqnFGqUf8Fqvv29EKy4W7VzjsY; SIDCC=ACA-OxNRrzgOmsFeEqEnBhSb0E4mlq1-WSu_8rf33dRYuN1BD8B6c5GnxnKTIc98nF-wkAcTfg; __Secure-1PSIDCC=ACA-OxMqXs-u9Ueh3YD5XcbJaOqgURU1V8iaNL79b3mFswshu-DmNTN35WEw4AIACYdYEwenYg; __Secure-3PSIDCC=ACA-OxMaOSEBF4r8sbJ88ehs4bqd2RoGz-9fuaJ-2AT-py6UVco14uG9yIWn-HUvGg6P5yDXxhBH',
            'device-memory': '8',
            'referer': 'https://www.google.com/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'x-client-data': 'CIu2yQEIpbbJAQipncoBCKHiygEIk6HLAQiGoM0BCNSxzQEI3L3NAQi5yM0BCJHKzQEIucrNAQiJ080BCM3WzQEI9dbNAQio2M0BCJfZzQEI+cDUFRjAy8wBGNLVzQEYz9jNAQ==',
            'x-maps-diversion-context-bin': 'CAI='
        }
        try:
            response = requests.request("GET", url, headers=headers, data={})
            json_str = response.text
            data = json.loads(json_str[4:])
            hours = data[0][1][0][14][203][1]
            return "The gym is {} \n Today's Hours: {}".format(hours[-1][0].upper(), hours[0][3][0][0])
        except Exception as e:
            # 发生异常 这里通知我
            return ""

if __name__ == "__main__":
    from configuration import Config
    c = Config()
    searchTask = SearchTask()
    rsp = searchTask.do_search("查询gym时间")
    print(rsp)
