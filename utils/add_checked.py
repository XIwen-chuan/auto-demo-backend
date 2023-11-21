import os
import json

def add_checked_field(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    # 添加 checked 字段
    data['checked'] = False

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def process_json_files(folder_path):
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            add_checked_field(file_path)

if __name__ == "__main__":
    folder_path = "../data/protocols"  # 替换成你的实际文件夹路径
    process_json_files(folder_path)