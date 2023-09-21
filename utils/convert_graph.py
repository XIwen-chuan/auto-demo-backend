import json
import os


def convert_json_files(input_folder, output_folder):
    # 获取输入文件夹中的所有JSON文件
    input_files = [f for f in os.listdir(input_folder) if f.endswith('.json')]

    for input_file in input_files:
        input_path = os.path.join(input_folder, input_file)
        output_file = input_file.split('.')[0] + '.json'
        output_path = os.path.join(output_folder, output_file)

        with open(input_path, 'r') as infile:
            data = json.load(infile)

        # 初始化结果数据结构
        result = {
            "name": input_file,
            "nodes": [],
            "edges": []
        }

        # 处理节点
        for cell in data['cells']:
            if cell['shape'] == 'custom-react-shape':
                print(cell['data'])
                try:
                    node = {
                        "id": cell['id'],
                        "text": cell['data']['protoText'],
                        "instruction": "ADD",
                        "slots": [{
                            "key": "it's a slot key",
                            "value": "it's a slot value",
                            "id": str(cell['id']),
                            "node_id": cell['id'],
                        }],
                        "emits": []
                    }
                except:
                    node = {
                        "id": cell['id'],
                        "text": "node",
                        "instruction": "ADD",
                        "slots": [{
                            "key": "it's a slot key",
                            "value": "it's a slot value",
                            "id": str(cell['id']),
                            "node_id": cell['id'],
                        }],
                        "emits": []
                    }
                result["nodes"].append(node)

        # 处理边
        for cell in data['cells']:
            if cell['shape'] == 'edge':
                source_node_id = cell['source']['cell']
                target_node_id = cell['target']['cell']

                source_attr_id = str(source_node_id)
                target_attr_id = str(target_node_id)

                edge = {
                    "id": cell['id'],
                    "source": {
                        "node_id": source_node_id,
                        "attr_id": source_attr_id
                    },
                    "target": {
                        "node_id": target_node_id,
                        "attr_id": target_attr_id
                    },
                    "text": "it's a edge text"
                }
                result["edges"].append(edge)

        # 将结果保存为新的JSON文件
        with open(output_path, 'w') as outfile:
            json.dump(result, outfile, indent=2)

# 示例用法
input_folder = '../data/oldProtocolGraphs'
output_folder = '../data/protocolGraphs'
convert_json_files(input_folder, output_folder)
