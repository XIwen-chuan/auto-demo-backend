import os
import shutil

def filter_and_copy_files(source_folder, target_folder, filter_folder):
    # 获取A文件夹中的所有文件
    source_files = os.listdir(source_folder)

    # 筛选符合条件的文件
    for source_file in source_files:
        if source_file.startswith("protocol_") and source_file.endswith(".json"):
            prefix = source_file.replace("protocol_", "").replace(".json", "")
            target_file = f"{prefix}_graphData.json"

            # 检查B文件夹中是否存在对应项
            if target_file in os.listdir(filter_folder):
                source_path = os.path.join(source_folder, source_file)
                target_path = os.path.join(target_folder, source_file)

                # 复制文件到C文件夹
                shutil.copy(source_path, target_path)
                print(f"File {source_file} copied to {target_folder}")

if __name__ == "__main__":
    # 定义A、B、C文件夹路径
    folder_A = "../data/protocols"
    folder_B = "../data/protocolGraphs"
    folder_C = "../data/protocolsLabeled"

    # 确保目标文件夹存在，如果不存在则创建
    os.makedirs(folder_C, exist_ok=True)

    # 执行过滤和复制操作
    filter_and_copy_files(folder_A, folder_C, folder_B)