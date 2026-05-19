import requests, os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("NOTION_TOKEN")

# 基礎 Headers 設定
headers = {
    "Authorization": f"Bearer {token}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"  # 傳送 JSON 資料時必須加上這行
}

# --- 第一部分：確認連線身分 (你原本成功的內容) ---
user_url = "https://api.notion.com/v1/users/me"
res = requests.get(user_url, headers=headers)
print("--- 機器人資訊 ---")
print(res.json())

# --- 第二部分：搜尋你有權限存取的資料庫 ---
search_url = "https://api.notion.com/v1/search"

# 設定過濾條件，只搜尋 object 為 database 的內容
payload = {
    "filter": {
        "value": "database",
        "property": "object"
    }
}

# 注意：搜尋 API 是使用 POST 方法
search_res = requests.post(search_url, headers=headers, json=payload)

print("\n--- 資料庫搜尋結果 ---")
print(search_res.json())