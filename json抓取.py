# @FileName:    json抓取.py
# @Time:        2024/6/24 21:51
# @Author:      清韵's
# @Project:     DyLiveGiftEffect
import requests
import json
import os

# 定义请求的 URL
url = 'https://live.douyin.com/webcast/assets/effects/?aid=6383'

# 发送 GET 请求获取数据
response = requests.get(url)

# 解析响应为 JSON 格式
data = response.json()

# 提取所需的 name、resource_uri 和 url_list 数据
extracted_data = []
for asset in data['data']['assets']:
    extracted_data.append({
        "name": asset['name'],
        "resource_uri": asset['resource_uri'],
        "url_list": asset['resource_url']['url_list']
    })

# 创建文件夹，如果不存在
folder_path = 'data_folder'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# 将提取的数据写入 JSON 文件
file_path = os.path.join(folder_path, 'output.json')
with open(file_path, 'w', encoding='utf-8') as file:
    json.dump(extracted_data, file, ensure_ascii=False, indent=4)
