import os
import json
import uuid

# 输入和输出文件夹路径
input_folder = '../data/protocolGraphsCompiledRaw'
output_folder = '../data/protocolGraphsCompiled'

# 遍历文件夹 A 中的 JSON 文件
for filename in os.listdir(input_folder):
    if filename.endswith('.json'):
        input_filepath = os.path.join(input_folder, filename)
        # output_filename = filename.replace('protocol_', '').replace('.json', '_graphData.json')        # output_file = os.path.join(output_dir, filename.replace("protocol_", "").replace(".json", "_graphData.json"))
        output_filename = filename.replace(".json", "_graphData.json")
        output_filepath = os.path.join(output_folder, output_filename)

        with open(input_filepath, 'r') as json_file:
            data = json.load(json_file)

            # 创建空的结果数据结构
            result_data = {
                "name": output_filename,
                "nodes": [],
                "edges": []
            }

            node_id_counter = 0  # 用于生成节点的唯一ID

            # 遍历原始 JSON 数据的每个元素
            for body in data:
                 if "result" in body and isinstance(body["result"], list):
                     for result_item in body["result"]:
                         if result_item:  # 确保 result_item 不为空
                             node_id = str(uuid.uuid4())  # 生成唯一节点ID
                             # 创建节点
                             node = {
                                 "id": node_id,
                                 "text": body["sentence"],
                                 "instruction": list(result_item.keys())[0],
                                 "slots": [],
                                 "emits": []
                             }
                             # 添加 emit 数据到节点
                             if "emit" in result_item[list(result_item.keys())[0]]:
                                 for emit_item in result_item[list(result_item.keys())[0]]["emit"]:
                                     emit_id = str(uuid.uuid4())  # 生成唯一 emit ID
                                     emit = {
                                         "key": list(emit_item.keys())[0],
                                         "value": emit_item[list(emit_item.keys())[0]],
                                         "id": emit_id,
                                         "node_id": node_id
                                     }
                                     node["emits"].append(emit)
                             # 添加 slot 数据到节点
                             if "slot" in result_item[list(result_item.keys())[0]]:
                                 for slot_item in result_item[list(result_item.keys())[0]]["slot"]:
                                     slot_id = str(uuid.uuid4())  # 生成唯一 slot ID
                                     slot = {
                                         "key": list(slot_item.keys())[0],
                                         "value": slot_item[list(slot_item.keys())[0]],
                                         "id": slot_id,
                                         "node_id": node_id
                                     }
                                     node["slots"].append(slot)
                             result_data["nodes"].append(node)

            # # 创建边连接节点
            # for i in range(len(result_data["nodes"]) - 1):
            #     edge_id = str(uuid.uuid4())
            #     edge = {
            #         "id": edge_id,
            #         "source": {
            #             "text": result_data["nodes"][i]["text"],
            #             "node_id": result_data["nodes"][i]["id"],
            #             "attr_id": result_data["nodes"][i]["id"]
            #         },
            #         "target": {
            #             "text": result_data["nodes"][i + 1]["text"],
            #             "node_id": result_data["nodes"][i + 1]["id"],
            #             "attr_id": result_data["nodes"][i + 1]["id"]
            #         },
            #         "text": "it's an edge text"
            #     }
            #     result_data["edges"].append(edge)

            # 保存转换后的数据到文件夹 B 中
            with open(output_filepath, 'w') as output_file:
                json.dump(result_data, output_file, indent=2)

print("Conversion completed.")