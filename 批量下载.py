# @FileName:    批量下载.py
# @Time:        2024/6/24 21:51
# @Author:      清韵's
# @Project:     DyLiveGiftEffect
import requests
import json
import os
import tqdm
import logging

# 定义日志文件路径
log_file = "download_errors.log"

# 配置日志记录器，设置编码为 utf-8
logging.basicConfig(filename=log_file, level=logging.ERROR, encoding='utf-8')

# 定义文件夹路径
folder_path = "downloaded_files"

# 检查文件夹是否存在，如果不存在则创建
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# 读取 output.json 文件
with open("data_folder/output.json", "r", encoding='utf-8') as file:
    data = json.load(file)

# 计算总资源数量
total_resources = len(data)
completed_resources = 0

# 总进度条
total_progress_bar = tqdm.tqdm(total=total_resources, desc="总资源下载进度", colour='blue')

for resource_info in data:
    name = resource_info["name"]
    resource_uri = resource_info["resource_uri"]

    is_download_successful = False  # 标记是否下载成功

    try:
        response = requests.get(resource_uri)
        if response.status_code == 200:
            # 保存文件
            with open(os.path.join(folder_path, f"{name}.zip"), "wb") as f:
                f.write(response.content)
            is_download_successful = True
            completed_resources += 1
            total_progress_bar.update(1)  # 更新总进度条
    except requests.exceptions.RequestException as e:
        # 主链接下载失败，尝试备用链接
        for url in resource_info["url_list"]:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    # 保存文件
                    with open(os.path.join(folder_path, f"{name}.zip"), "wb") as f:
                        f.write(response.content)
                    is_download_successful = True
                    completed_resources += 1
                    total_progress_bar.update(1)  # 更新总进度条
                    break
            except requests.exceptions.RequestException as e:
                # 处理备用链接请求异常，将错误写入日志
                logging.error(f"下载 {name} 的 {url} 时出错: {e}")

    if not is_download_successful:
        # 所有链接都下载失败，将错误写入日志
        logging.error(f"下载 {name} 的所有链接都失败")

total_progress_bar.close()  # 关闭总进度条
