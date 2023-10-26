import json
import os

isa_json_path = "../data/human_modified_isa/human-modified-isa.json"

def convert_json_files(input_folder, output_folder):
    # 获取输入文件夹中的所有JSON文件
    input_files = [f for f in os.listdir(input_folder) if f.endswith('.json')]

    # 从 isa_json_path 中提取所有 keys 组成 isa_instruction_words
    with open(isa_json_path, 'r') as file:
        isa_data = json.load(file)
    isa_instruction_words = []
    for key in isa_data.keys():
        isa_instruction_words.append(key)

    print("isa_instruction_words", isa_instruction_words)

    for input_file in input_files:
        input_path = os.path.join(input_folder, input_file)
        output_file = input_file.split('.')[0] + '_graphData.json'
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
                try:
                    # 将 cell['data']['protoText'] 的首单词与 isa_instruction_words 中的单词逐个进行匹配，匹配成功则将 node_instruction 设置为该单词，否则设置为 ADD
                    node_instruction = "ADD"  # 默认值
                    first_word = cell['data']['protoText'].split()[0].lower()
                    for word in isa_instruction_words:
                        if first_word == word.lower():
                            node_instruction = word.upper()
                            break

                    print(cell['data'])
                    node = {
                        "id": cell['id'],
                        "text": cell['data']['protoText'],
                        "instruction": node_instruction,
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
                source_text = ""
                target_text = ""
                # search the text of source node
                for node in result["nodes"]:
                    if node["id"] == cell['source']['cell']:
                        source_text = node["text"]
                    elif node["id"] == cell['target']['cell']:
                        target_text = node["text"]
                source_node_id = cell['source']['cell']
                target_node_id = cell['target']['cell']

                source_attr_id = str(source_node_id)
                target_attr_id = str(target_node_id)

                edge = {
                    "id": cell['id'],
                    "source": {
                        "text": source_text,
                        "node_id": source_node_id,
                        "attr_id": source_attr_id
                    },
                    "target": {
                        "text": target_text,
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
