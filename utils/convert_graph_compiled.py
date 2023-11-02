import json
import os
import uuid

def process_result(result, node):
    for key, value in result.items():
        node["instruction"] = key
        emits = value.get("emit", [])
        for emit in emits:
            emit_node = {
                "key": emit,
                "value": emits[emit],
                "id": str(uuid.uuid4()),
                "node_id": node["id"]
            }
            node["emits"].append(emit_node)
        slots = value.get("slot", [])
        for slot in slots:
            slot_node = {
                "key": slot,
                "value": slots[slot],
                "id": str(uuid.uuid4()),
                "node_id": node["id"]
            }
            node["slots"].append(slot_node)

def process_body(body, nodes):
    for item in body:
        node = {
            "id": str(uuid.uuid4()),
            "text": item["sentence"],
            "instruction": "",
            "slots": [],
            "emits": []
        }
        result = item.get("result", {})
        if result:
            process_result(result, node)
        nodes.append(node)

def process_json_file(input_file, output_file):
    with open(input_file, "r") as f:
        data = json.load(f)

    nodes = []
    process_body(data, nodes)

    graph_data = {
        "name": output_file,
        "nodes": nodes,
        "edges": []
    }

    with open(output_file, "w") as f:
        json.dump(graph_data, f, indent=2)

def main():
    input_dir = "../data/protocolGraphsCompiledRaw"
    output_dir = "../data/protocolGraphsCompiled"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(".json"):
            input_file = os.path.join(input_dir, filename)
            output_file = os.path.join(output_dir, filename.replace("protocol_", "").replace(".json", "_graphData.json"))
            process_json_file(input_file, output_file)

if __name__ == "__main__":
    main()