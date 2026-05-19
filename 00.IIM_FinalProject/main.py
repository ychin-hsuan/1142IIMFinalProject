import requests
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()
token = os.getenv("NOTION_TOKEN")

# 定義 Headers
headers = {
    "Authorization": f"Bearer {token}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def get_database_info():
    """找出機器人有權限存取的第一個資料庫 ID"""
    search_url = "https://api.notion.com/v1/search"
    payload = {"filter": {"value": "database", "property": "object"}}
    
    try:
        res = requests.post(search_url, headers=headers, json=payload)
        results = res.json().get("results", [])
        if not results:
            return None
        return results[0]['id']
    except Exception as e:
        print(f"Error fetching database info: {e}")
        return None

def calculate_credits(db_id):
    """抓取資料並按學期分類"""
    query_url = f"https://api.notion.com/v1/databases/{db_id}/query"
    res = requests.post(query_url, headers=headers)
    data = res.json()
    
    semester_data = {}
    total_all = 0
    
    for page in data.get("results", []):
        props = page.get("properties", {})
        
        # 1. 處理課程名稱與學期標籤
        name_obj = props.get("課程名稱", {}).get("title", [])
        full_name = name_obj[0].get("plain_text") if name_obj else "未命名"
        
        if "[" in full_name and "]" in full_name:
            sem_key = full_name.split("]")[0].replace("[", "").strip()
            course_name = full_name.split("]")[1].strip()
        else:
            sem_key = "其他"
            course_name = full_name

        # 2. 處理 Rollup Array 型態的學分 (你之前的成功路徑)
        rollup_data = props.get("學分", {}).get("rollup", {})
        rollup_array = rollup_data.get("array", [])
        credit = rollup_array[0].get("number", 0) if rollup_array else 0
        
        # 3. 分類存入字典
        if sem_key not in semester_data:
            semester_data[sem_key] = []
        
        semester_data[sem_key].append({
            "name": course_name,
            "credit": credit
        })
        total_all += credit

    return semester_data, total_all

# 測試用：直接執行 main.py 時會印出結果
if __name__ == "__main__":
    db_id = get_database_info()
    if db_id:
        data, total = calculate_credits(db_id)
        print(f"✅ 成功解析！總學分：{total}")