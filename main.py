import os
import json
import re

from starlette.responses import FileResponse

from utils.utils import get_graph_filename_by_protocol_fileneme, generate_unique_attr_id, generate_unique_edge_id

from fastapi import FastAPI, HTTPException, UploadFile, Header
from typing_extensions import Annotated
from typing import Union

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
        raise HTTPException(status_code=404, detail="文件不存在")

    # 构建文件名
    filename = f"{pro_type}-{num}_graphData.json"
    filepath = os.path.join(graphs_dir, filename)

    # 检查文件是否存在
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="文件不存在")

    # 读取JSON文件内容
    with open(filepath, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
            return data
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="JSON解码错误")


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


@app.post("/api/upload_json/")
async def upload_and_convert_json(
    file: UploadFile,
    protocol_filename: Annotated[Union[str, None], Header()] = None
):
    try:
        # 解析上传的JSON文件内容
        uploaded_data = json.loads(file.file.read().decode("utf-8"))

        # 初始化结果数据结构
        result = {
            "name": protocol_filename,
            "nodes": [],
            "edges": []
        }

        # 处理节点
        for cell in uploaded_data['cells']:
            if cell['shape'] == 'custom-react-shape':
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
        for cell in uploaded_data['cells']:
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
                    "text": "it's an edge text"
                }
                result["edges"].append(edge)


        print("protocol_filename", protocol_filename)
        graph_filename = get_graph_filename_by_protocol_fileneme(protocol_filename)

        # 将处理后的JSON数据保存为新的JSON文件
        output_path = os.path.join("./data/protocolGraphs", graph_filename)
        with open(output_path, 'w') as outfile:
            json.dump(result, outfile, indent=2)

        return {"message": "文件上传和处理成功"}
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/download_json/")
async def download_graph_json(
        filename: str,
):
    # 使用正则表达式匹配下划线和破折号之间的内容和破折号后面的数字
    match = re.match(r".*?_([^_-]+)-(\d+)\.json", filename)

    if match:
        # 提取下划线和破折号之间的内容和破折号后面的数字
        pro_type = match.group(1)
        num = int(match.group(2))
    else:
        raise HTTPException(status_code=404, detail="文件不存在")

    # 构建文件名
    filename = f"{pro_type}-{num}_graphData.json"
    filepath = os.path.join(graphs_dir, filename)
    try:
        # 确保指定的文件存在
        if os.path.exists(filepath):
            # 使用 FileResponse 返回文件
            return FileResponse(filepath, media_type="application/json")
        else:
            return {"error": "文件不存在"}
    except Exception as e:
        return {"error": f"发生错误: {str(e)}"}

@app.delete("/api/attr/")
async def delete_attr(
        filename: str,
        attr_id: str
):
    graph_filename = get_graph_filename_by_protocol_fileneme(filename)
    filepath = os.path.join(graphs_dir, graph_filename)
    try:
        # 读取 JSON 文件
        with open(filepath, 'r') as file:
            data = json.load(file)

        # 删除指定的 slot 和 emit
        for node in data["nodes"]:
            for slot in node["slots"][:]:
                if slot["id"] == attr_id:
                    print("slot", slot)
                    node["slots"].remove(slot)
            for emit in node["emits"][:]:
                if emit["id"] == attr_id:
                    print("emit", emit)
                    node["emits"].remove(emit)

        # 删除与指定 attr_id 相关的 edges
        data["edges"] = [edge for edge in data["edges"] if
                         edge["source"]["attr_id"] != attr_id and edge["target"]["attr_id"] != attr_id]

        print("after data", data)
        # 保存更新后的 JSON 内容回到文件
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=2)

        print(f"成功删除 attr_id 为 {attr_id} 的 slot, emit 和相关的 edges")
    except FileNotFoundError:
        print(f"文件 '{filename}' 未找到")
    except Exception as e:
        print(f"发生错误: {e}")
    return {"msg": "finished"}

@app.post("/api/attr/")
async def add_attr(
        filename: str,
        node_id: str,
        key: str,
        value: str,
        attr_type: str
):
    graph_filename = get_graph_filename_by_protocol_fileneme(filename)
    filepath = os.path.join(graphs_dir, graph_filename)
    try:
        # 读取 JSON 文件
        with open(filepath, 'r') as file:
            data = json.load(file)

        # 找到指定的节点
        target_node = None
        for node in data["nodes"]:
            if node["id"] == node_id:
                target_node = node
                break

        if target_node is None:
            print(f"未找到 ID 为 {node_id} 的节点")
            return
        new_id = generate_unique_attr_id(data, attr_type+'s')
        # 创建新的属性
        new_attr = {
            "key": key,
            "value": value,
            "id": new_id,
        }

        # 添加属性到节点
        target_node[attr_type+'s'].append(new_attr)

        # 保存更新后的 JSON 内容回到文件
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=2)

        print(f"成功添加 {attr_type} 到节点 {node_id}")
    except FileNotFoundError:
        print(f"文件 '{filename}' 未找到")
    # except Exception as e:
    #     print(f"发生错误: {e}")
    return {"msg": "finished"}

@app.post("/api/edge/")
async def add_edge(
        filename: str,
        source_node_id: str,
        source_attr_id: str,
        target_node_id: str,
        target_attr_id: str,
        text: str
):
    graph_filename = get_graph_filename_by_protocol_fileneme(filename)
    filepath = os.path.join(graphs_dir, graph_filename)
    try:
        # 读取 JSON 文件
        with open(filepath, 'r') as file:
            data = json.load(file)

        new_id = generate_unique_edge_id(data)
        # 创建新的边缘
        new_edge = {
            "id": new_id,  # 自动生成新边缘的唯一 ID
            "source": {
                "node_id": source_node_id,
                "attr_id": source_attr_id
            },
            "target": {
                "node_id": target_node_id,
                "attr_id": target_attr_id
            },
            "text": text
        }

        # 添加新边缘到边缘列表
        data["edges"].append(new_edge)

        # 保存更新后的 JSON 内容回到文件
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=2)

        print(f"成功添加边缘")
    except FileNotFoundError:
        print(f"文件 '{filename}' 未找到")
    except Exception as e:
        print(f"发生错误: {e}")

    return {"msg": "finished"}

@app.delete("/api/edge/")
async def delete_edge(
        filename: str,
        edge_id: str
):
    graph_filename = get_graph_filename_by_protocol_fileneme(filename)
    filepath = os.path.join(graphs_dir, graph_filename)
    try:
        # 读取 JSON 文件
        with open(filepath, 'r') as file:
            data = json.load(file)

        # 查找要删除的边缘
        deleted_edge = None
        for edge in data["edges"]:
            if edge["id"] == edge_id:
                deleted_edge = edge
                break

        if deleted_edge is None:
            print(f"未找到 ID 为 {edge_id} 的边缘")
            return

        # 从边缘列表中删除边缘
        data["edges"].remove(deleted_edge)

        # 保存更新后的 JSON 内容回到文件
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=2)

        print(f"成功删除边缘 {edge_id}")
    except FileNotFoundError:
        print(f"文件 '{filename}' 未找到")
    except Exception as e:
        print(f"发生错误: {e}")
    return {"msg": "finished"}

@app.put("/api/instruction/")
async def modify_intruction(
        filename: str,
        node_id: str,
        new_instruction: str
):
    graph_filename = get_graph_filename_by_protocol_fileneme(filename)
    filepath = os.path.join(graphs_dir, graph_filename)
    try:
        # 读取 JSON 文件
        with open(filepath, 'r') as file:
            data = json.load(file)

        # 查找要修改指令的节点
        target_node = None
        for node in data["nodes"]:
            if node["id"] == node_id:
                target_node = node
                break

        if target_node is None:
            print(f"未找到 ID 为 {node_id} 的节点")
            return

        # 修改节点的指令
        target_node["instruction"] = new_instruction

        # 保存更新后的 JSON 内容回到文件
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=2)

        print(f"成功修改节点 {node_id} 的指令为 '{new_instruction}'")
    except FileNotFoundError:
        print(f"文件 '{filename}' 未找到")
    except Exception as e:
        print(f"发生错误: {e}")

    return {"msg": "finished"}