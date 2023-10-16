import requests
import json
import time

# 存储所有 protocolId 的列表
protocol_ids = []

headers = {
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMGNjZTAzZGJjODgwNTdhMGJmZWViM2NmZmEwOGI2ZWIiLCJleHAiOjE2OTcwMjMwNDB9.zQ1upA3Cyz5uo9bLLyVsnPUJ4sMp8T-vfgux324fAn4",
}

# 获取所有 protocolId
for page in range(1, 163):
    params = {
        "source": "all",
        "status": "all",
        "currentPage": page,
        "pageSize": 10
    }
    response = requests.post("https://helixon.yzhu.io/api/protocols/query", json=params, headers=headers)
    data = response.json()
    protocol_ids.extend([item["protocolId"] for item in data["data"]])

    print(f"page {page} done")

    time.sleep(0.1)  # 间隔0.1秒

# 遍历 protocolIds 并保存数据
for protocol_id in protocol_ids:
    params = {
        "protocolId": protocol_id
    }
    response = requests.post("https://helixon.yzhu.io/api/protocol-item/query", json=params, headers=headers)
    data = response.json()

    # 保存数据到JSON文件，文件名为 protocolId
    with open(f"./data/{protocol_id}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"{protocol_id} done")

    # 控制请求间隔
    time.sleep(0.1)  # 间隔0.1秒