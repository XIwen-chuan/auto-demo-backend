import os
import json
import re

from fastapi import FastAPI

app = FastAPI()

protocols_list_dir = "./data/protocols"
graphs_dir = "./data/protocolGraphs"


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/api/protocol/list/")
async def get_protocols_list(skip: int = 0, limit: int = 30):
    folder_path = protocols_list_dir  # 替换为你的 JSON 文件所在文件夹的路径
    files = os.listdir(folder_path)
    files.sort()  # 确保文件按字母顺序排序

    json_files = []

    for file_name in files[skip: skip + limit]:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path) and file_name.endswith(".json"):
            with open(file_path, "r") as file:
                json_content = json.load(file)
                json_files.append(json_content)

    return json_files


@app.get("/api/protocol/graph/")
async def get_graph(filename: str):
    # 使用正则表达式匹配下划线和破折号之间的内容和破折号后面的数字
    match = re.match(r".*?_([^_-]+)-(\d+)\.json", filename)

    if match:
        # 提取下划线和破折号之间的内容和破折号后面的数字
        pro_type = match.group(1)
        num = int(match.group(2))
    else:
        print("没有匹配到结果")

    # 构建文件名
    filename = f"{pro_type}-{num}_graphData.json"
    filepath = os.path.join(graphs_dir, filename)

    # 检查文件是否存在
    if not os.path.exists(filepath):
        return {"error": "文件不存在"}

    # 读取JSON文件内容
    with open(filepath, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
            return data
        except json.JSONDecodeError:
            return {"error": "JSON解码错误"}


@app.get("/api/protocol/")
async def get_protocol(filename: str):
    # 构建完整的文件路径
    filepath = os.path.join(protocols_list_dir, filename)

    # 检查文件是否存在
    if not os.path.exists(filepath):
        return {"error": "文件不存在"}

    # 读取JSON文件内容
    with open(filepath, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
            return data
        except json.JSONDecodeError:
            return {"error": "JSON解码错误"}