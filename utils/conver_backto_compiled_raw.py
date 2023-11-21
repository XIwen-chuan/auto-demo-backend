import os
import json

# 定义A文件夹和B文件夹的路径
A_folder_path = '../data/protocolGraphs'
B_folder_path = '../data/protocolGraphsBackCompiled'

# 创建B文件夹（如果不存在）
if not os.path.exists(B_folder_path):
    os.makedirs(B_folder_path)

# 遍历A文件夹中的JSON文件
for filename in os.listdir(A_folder_path):
    if filename.endswith('.json'):
        with open(os.path.join(A_folder_path, filename), 'r') as file:
            data = json.load(file)

        # 格式转换
        converted_data = []
        for node in data['nodes']:
            converted_node = {
                'title': '',
                'body': [
                    {
                        'sentence': node['text'],
                        'result': {
                            node['instruction']: {
                                'emit': [{emit['key']: emit['value']} for emit in node['emits']],
                                'slot': [{slot['key']: slot['value']} for slot in node['slots']]
                            }
                        }
                    }
                ]
            }
            converted_data.append(converted_node)

        # 写入B文件夹
        output_filename = os.path.splitext(filename)[0] + '_converted.json'
        with open(os.path.join(B_folder_path, output_filename), 'w') as output_file:
            json.dump(converted_data, output_file, indent=2)

print("转换完成，文件已保存到B文件夹中。")