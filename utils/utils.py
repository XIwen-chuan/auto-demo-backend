import json
import os
import re


def get_graph_filename_by_protocol_fileneme(filename: str):
    match = re.match(r".*?_([^_-]+)-(\d+)\.json", filename)

    if match:
        # 提取下划线和破折号之间的内容和破折号后面的数字
        pro_type = match.group(1)
        num = int(match.group(2))
    else:
        return False

    # 构建文件名
    filename = f"{pro_type}-{num}_graphData.json"
    return filename


import hashlib


def generate_unique_attr_id(data, attr_type):
    # 计算哈希值
    hash_obj = hashlib.sha256(json.dumps(data).encode('utf-8'))
    hash_value = hash_obj.hexdigest()

    # 确保哈希值是唯一的
    existing_ids = set()
    for node in data["nodes"]:
        for attr in node[attr_type]:
            existing_ids.add(attr["id"])

    new_id = hash_value
    while new_id in existing_ids:
        hash_obj.update(b"_")
        hash_value = hash_obj.hexdigest()
        new_id = hash_value

    return new_id

def generate_unique_edge_id(data):
    # 计算哈希值
    hash_obj = hashlib.sha256(json.dumps(data).encode('utf-8'))
    hash_value = hash_obj.hexdigest()

    # 确保哈希值是唯一的
    existing_ids = set()
    for edge in data["edges"]:
        existing_ids.add(edge["id"])

    new_id = hash_value
    while new_id in existing_ids:
        hash_obj.update(b"_")
        hash_value = hash_obj.hexdigest()
        new_id = hash_value

    return new_id
