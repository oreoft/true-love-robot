import concurrent
from concurrent import futures
import os
import urllib.request
import requests
from datetime import datetime

executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
def asyncDownloadFile():
    executor.submit(downloadZaobaoFile)
def asyncDownloadMoyuFile():
    executor.submit(downloadMoyuFile)


def downloadMoyuFile():
    # 获取当前脚本所在的目录，即项目目录
    project_directory = os.path.dirname(os.path.abspath(__file__))
    download_directory = project_directory + '/moyu-jpg/'
    # 获取当前日期并将其格式化为所需的字符串
    current_date = datetime.now().strftime('%m-%d-%Y')
    # 构建文件名，例如：10-20-2023.jpg
    local_filename = f'{current_date}.jpg'
    # 构建完整的文件路径
    full_file_path = os.path.join(download_directory, local_filename)
    # 指定要下载的文件的URL
    file_url = 'https://moyu.qqsuu.cn/'
    # 使用urllib.request库下载文件并保存到指定的位置
    urllib.request.urlretrieve(file_url, full_file_path)
    print(f'{local_filename} 已下载到 {download_directory}')

def downloadZaobaoFile():
    # 获取当前脚本所在的目录，即项目目录
    project_directory = os.path.dirname(os.path.abspath(__file__))
    download_directory = project_directory + '/zaobao-jpg/'
    # 获取当前日期并将其格式化为所需的字符串
    current_date = datetime.now().strftime('%m-%d-%Y')
    # 构建文件名，例如：10-20-2023.jpg
    local_filename = f'{current_date}.jpg'
    # 构建完整的文件路径
    full_file_path = os.path.join(download_directory, local_filename)

    # 获取文件内容
    url = "https://v2.alapi.cn/api/zaobao"
    payload = "token=ODECJI71rCNDt6DO&format=image"
    headers = {'Content-Type': "application/x-www-form-urlencoded"}
    response = requests.request("POST", url, data=payload, headers=headers)

    # 保存到指定的位置
    with open(full_file_path, 'wb') as file:
        file.write(response.content)
    print(f'{local_filename} 已下载到 {download_directory}')

if __name__ == "__main__":
    downloadZaobaoFile()
