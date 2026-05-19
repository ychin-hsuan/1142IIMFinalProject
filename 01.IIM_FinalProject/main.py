import requests
import os
from dotenv import load_dotenv

# 1. 載入環境變數
load_dotenv()
token = os.getenv("NOTION_TOKEN")

# 2. 定義 Headers (確保這段在最前面，才不會報 NameError)
headers = {
    "Authorization": f"Bearer {token}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def get_database_info():
    """第一步：先找出機器人有權限存取的資料庫 ID"""
    search_url = "https://api.notion.com/v1/search"
    payload = {"filter": {"value": "database", "property": "object"}}
    
    res = requests.post(search_url, headers=headers, json=payload)
    results = res.json().get("results", [])
    
    if not results:
        print("❌ 找不到資料庫！請檢查 Notion 頁面是否有 Connect to 你的機器人。")
        return None
    
    # 假設我們拿第一個找到的資料庫
    db = results[0]
    print(f"✅ 成功連線到資料庫：{db['title'][0]['plain_text']}")
    return db['id']

def calculate_credits(db_id):
    query_url = f"https://api.notion.com/v1/databases/{db_id}/query"
    res = requests.post(query_url, headers=headers)
    data = res.json()
    
    total = 0
    print("\n--- 課程清單明細 ---")
    
    for page in data.get("results", []):
        props = page.get("properties", {})
        
        # 1. 拿課程名稱
        name_list = props.get("課程名稱", {}).get("title", [])
        name = name_list[0].get("plain_text") if name_list else "未命名"
        
        # 2. 拿學分 (針對 Array 型 Rollup 的剝洋蔥寫法)
        rollup_data = props.get("學分", {}).get("rollup", {})
        rollup_array = rollup_data.get("array", [])
        
        # 判斷 array 是否有東西，有的話取第一個元素的 number
        if rollup_array:
            credit = rollup_array[0].get("number", 0)
        else:
            credit = 0
            
        print(f"- {name}: {credit} 學分")
        total += credit
        
    print("-" * 30)
    print(f"📊 目前累積總學分: {total}")


# --- 主程式執行區 ---
if __name__ == "__main__":
    target_db_id = get_database_info()
    if target_db_id:
        calculate_credits(target_db_id)