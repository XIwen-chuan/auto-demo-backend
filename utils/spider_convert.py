import os
import json

# 指定数据目录
data_dir = '../data/protocolsFromH5'
output_dir = '../data/oldProtocolGraphs'

# 确保输出目录存在
os.makedirs(output_dir, exist_ok=True)

# 遍历数据目录中的JSON文件
for filename in os.listdir(data_dir):
    if filename.endswith(".json"):
        # 读取原始JSON文件
        with open(os.path.join(data_dir, filename), 'r') as file:
            data = json.load(file)

        try:
            # 获取data.graphData字段的字符串内容
            graph_data_str = data['graphData']

            # 检查graph_data_str是否为空
            if graph_data_str is not None:
                # 解码被转义的JSON字符串
                graph_data = json.loads(graph_data_str)

                # 构建输出文件名
                output_filename = f"{os.path.splitext(filename)[0]}.json"

                # 保存新的JSON对象到输出文件
                with open(os.path.join(output_dir, output_filename), 'w') as output_file:
                    json.dump(graph_data, output_file, indent=2)

                print(f"处理文件 {filename} 完成，已保存为 {output_filename}")
            else:
                print(f"警告：文件 {filename} 的data.graphData字段为空，跳过处理")
        except KeyError:
            print(f"警告：文件 {filename} 的data字段缺少graphData字段，跳过处理")