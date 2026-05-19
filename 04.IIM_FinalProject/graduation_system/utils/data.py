# utils/data.py
import os, requests
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN", "")
NOTION_DB_ID = os.getenv("NOTION_DB_ID", "")   # 個人修課紀錄 DB

# ══════════════════════════════════════════════════════════════
# 管院共構必修（12 學分）
# ══════════════════════════════════════════════════════════════
MGT_REQUIRED = [
    {"name": "人工智慧語言與產業應用", "credits": 3, "semester": "大一上"},
    {"name": "統計學(1)",              "credits": 3, "semester": "大一上"},
    {"name": "會計學(1)",              "credits": 3, "semester": "大一下"},
    {"name": "經濟學(1)",              "credits": 3, "semester": "大二上暑"},
]
MGT_REQUIRED_CREDITS = 12

# ══════════════════════════════════════════════════════════════
# 系訂必修（49 學分）
# ══════════════════════════════════════════════════════════════
REQUIRED_COURSES = [
    {"name": "計算機概論",              "credits": 3, "semester": "大一上"},
    {"name": "程式設計(1)",             "credits": 4, "semester": "大一上"},
    {"name": "微積分",                  "credits": 3, "semester": "大一上"},
    {"name": "統計學(2)",               "credits": 3, "semester": "大一上", "note": "先修：統計學(1)"},
    {"name": "程式設計(2)",             "credits": 4, "semester": "大一下", "note": "先修：程式設計(1)"},
    {"name": "資料結構",                "credits": 3, "semester": "大一下"},
    {"name": "商業溝通",                "credits": 2, "semester": "大一下"},
    {"name": "電腦網路",                "credits": 3, "semester": "大二上"},
    {"name": "資料庫管理",              "credits": 3, "semester": "大二上"},
    {"name": "網頁程式設計(1)",         "credits": 3, "semester": "大二上"},
    {"name": "管理資訊系統",            "credits": 3, "semester": "大二下"},
    {"name": "系統分析與設計",          "credits": 3, "semester": "大三上"},
    {"name": "資訊倫理與法律",          "credits": 3, "semester": "大三上"},
    {"name": "畢業專題(1)",             "credits": 3, "semester": "大三下", "note": "P/F"},
    {"name": "資訊管理專題實作(1)",     "credits": 1, "semester": "大四上"},
    {"name": "畢業專題(2)",             "credits": 3, "semester": "大四下", "note": "P/F"},
    {"name": "資訊管理專題實作(2)",     "credits": 1, "semester": "大四下"},
]
REQUIRED_CREDITS = 49
PASS_FAIL_COURSES = {"畢業專題(1)", "畢業專題(2)"}

# ══════════════════════════════════════════════════════════════
# 本系選修五大領域（系選修整體至少 30 學分）
# ══════════════════════════════════════════════════════════════
ELECTIVE_DOMAINS = {
    "企業管理領域": {
        "color": "#4f8ef7",
        "courses": [
            {"name": "資訊管理導論",            "credits": 3, "semester": "大一下"},
            {"name": "管理學",                  "credits": 3, "semester": "大一下"},
            {"name": "行銷管理",                "credits": 3, "semester": "大二上"},
            {"name": "生產與作業管理",          "credits": 3, "semester": "大二上"},
            {"name": "人力資源管理",            "credits": 3, "semester": "大三上"},
            {"name": "物流與供應鏈管理",        "credits": 3, "semester": "大三上"},
            {"name": "財務管理",                "credits": 3, "semester": "大三下"},
            {"name": "專案管理",                "credits": 3, "semester": "大四上"},
            {"name": "管理科學",                "credits": 3, "semester": "大四上"},
            {"name": "服務科學與管理",          "credits": 3, "semester": "大四下"},
            {"name": "數位轉型全球觀點",        "credits": 2, "semester": "大四下"},
            {"name": "精實供應鏈管理",          "credits": 3, "semester": "大四下"},
            {"name": "知識管理",                "credits": 3, "semester": "大四下"},
        ]
    },
    "企業資訊應用領域": {
        "color": "#f5c518",
        "courses": [
            {"name": "網路行銷",                "credits": 3, "semester": "大三上"},
            {"name": "電子商務",                "credits": 3, "semester": "大三下"},
            {"name": "顧客關係管理與商業智慧",  "credits": 3, "semester": "大四上"},
            {"name": "大數據應用電子商務",      "credits": 3, "semester": "大四上"},
            {"name": "企業資源規劃",            "credits": 3, "semester": "大四下"},
            {"name": "數位行銷",                "credits": 3, "semester": "大四下"},
            {"name": "程式交易",                "credits": 3, "semester": "大四下"},
        ]
    },
    "資訊技術領域": {
        "color": "#7c5cfc",
        "courses": [
            {"name": "資訊技術實務",            "credits": 3, "semester": "大一上"},
            {"name": "資訊科技專業詞彙",        "credits": 3, "semester": "大一上"},
            {"name": "C語言程式設計",           "credits": 3, "semester": "大二上"},
            {"name": "行動裝置應用程式設計",    "credits": 3, "semester": "大二下"},
            {"name": "網路系統管理實務",        "credits": 3, "semester": "大二下"},
            {"name": "物聯網概論",              "credits": 3, "semester": "大二下"},
            {"name": "網頁程式設計(2)",         "credits": 3, "semester": "大三上"},
            {"name": "作業系統",                "credits": 3, "semester": "大三上"},
            {"name": "視窗程式設計",            "credits": 3, "semester": "大三上"},
            {"name": "企業網站開發",            "credits": 3, "semester": "大三下"},
            {"name": "醫療資訊交換實務",        "credits": 0.5, "semester": "大四上"},
            {"name": "醫療資訊系統分析",        "credits": 0.5, "semester": "大四上"},
            {"name": "銀行金融資訊系統實務",    "credits": 0.5, "semester": "大四上"},
            {"name": "銀行金融資訊系統分析",    "credits": 0.5, "semester": "大四上"},
            {"name": "數位鑑識",                "credits": 3, "semester": "大四下"},
        ]
    },
    "資訊安全領域": {
        "color": "#ff4d6d",
        "courses": [
            {"name": "資訊安全導論",            "credits": 3, "semester": "大二下"},
            {"name": "資訊系統稽核與管理",      "credits": 3, "semester": "大三上"},
            {"name": "區塊鏈實務與應用",        "credits": 3, "semester": "大三上"},
            {"name": "網路安全",                "credits": 3, "semester": "大三下"},
            {"name": "網路攻防技術與應用",      "credits": 3, "semester": "大四上"},
            {"name": "醫療系統安全",            "credits": 3, "semester": "大四上"},
        ]
    },
    "數據創新與智能互動領域": {
        "color": "#2ecc8a",
        "courses": [
            {"name": "應用統計學",              "credits": 3, "semester": "大二上"},
            {"name": "資料視覺化",              "credits": 3, "semester": "大二下"},
            {"name": "雲端機器學習",            "credits": 3, "semester": "大二下"},
            {"name": "數據擷取與應用",          "credits": 2, "semester": "大二下"},
            {"name": "智能機器互動設計",        "credits": 3, "semester": "大二下"},
            {"name": "數據程式案例研析",        "credits": 3, "semester": "大三上"},
            {"name": "數據處理基礎",            "credits": 2, "semester": "大三上"},
            {"name": "大數據分析方法",          "credits": 3, "semester": "大三下"},
            {"name": "資料庫程式規劃",          "credits": 3, "semester": "大三下"},
            {"name": "非關聯式資料庫",          "credits": 3, "semester": "大三下"},
            {"name": "網頁與文字探勘",          "credits": 3, "semester": "大四上"},
            {"name": "數據管理工具研析",        "credits": 3, "semester": "大四下"},
            {"name": "數據創新與智能互動專題",  "credits": 2, "semester": "大四下"},
            {"name": "大數據處理與分析技術",    "credits": 3, "semester": "大四下"},
            {"name": "資訊科技使用者調查法",    "credits": 2, "semester": "大四上"},
        ]
    },
}

ELECTIVE_MIN_TOTAL = 30

PREREQS = [
    ("程式設計(1)",     "程式設計(2)"),
    ("統計學(1)",       "統計學(2)"),
    ("網頁程式設計(1)", "網頁程式設計(2)"),
    ("資料庫管理",      "資料庫程式規劃"),
]

# ══════════════════════════════════════════════════════════════
# Notion API
# ══════════════════════════════════════════════════════════════
# ══════════════════════════════════════════════════════════════
# Notion 課程名稱 → data.py 標準名稱 對照表
# ══════════════════════════════════════════════════════════════
NAME_MAP = {
    "程式設計1":     "程式設計(1)",
    "程式設計2":     "程式設計(2)",
    "會計學1":       "會計學(1)",
    "會計學(1).":    "會計學(1)",
    "經濟學1":       "經濟學(1)",
    "統計學1":       "統計學(1)",
    "統計學2":       "統計學(2)",
    "網頁程式設計1": "網頁程式設計(1)",
    "網頁程式設計2": "網頁程式設計(2)",
    "管理學":        "管理學",    # 企業管理領域選修
    "英文閱讀與寫作": None,       # 通識課程，不計入審查
}

def _normalize(raw: str):
    name = raw.strip()
    if name in NAME_MAP:
        return NAME_MAP[name]
    return name

def _get_credits(prop: dict) -> float:
    """學分欄位可能是 number 或 rollup，統一處理"""
    if prop.get("type") == "number":
        return prop.get("number") or 0
    if prop.get("type") == "rollup":
        arr = prop.get("rollup", {}).get("array", [])
        if arr and arr[0].get("type") == "number":
            return arr[0].get("number") or 0
    return 0


def _query_notion(status: str) -> list:
    """共用的 Notion API 查詢，支援分頁"""
    token = NOTION_TOKEN
    db_id = NOTION_DB_ID
    if not token or not db_id:
        return []
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }
    payload = {
        "filter": {"property": "修課狀態", "status": {"equals": status}},
        "page_size": 100,
    }
    all_pages = []
    try:
        while True:
            res  = requests.post(
                f"https://api.notion.com/v1/databases/{db_id}/query",
                headers=headers, json=payload, timeout=10,
            )
            data = res.json()
            all_pages.extend(data.get("results", []))
            if data.get("has_more") and data.get("next_cursor"):
                payload["start_cursor"] = data["next_cursor"]
            else:
                break
    except Exception:
        pass
    return all_pages


def fetch_notion_courses() -> dict:
    """
    從 Notion 讀取「完成」的課程。
    學分欄位支援 rollup 和 number 兩種類型。
    """
    pages = _query_notion("完成")
    if not pages and not (NOTION_TOKEN and NOTION_DB_ID):
        return {}

    taken = {}
    for page in pages:
        props = page.get("properties", {})
        try:
            raw_name = props["課程名稱"]["title"][0]["plain_text"].strip()
            name     = _normalize(raw_name)
            if name is None:
                continue
            credits = _get_credits(props.get("學分", {}))
            score   = props.get("成績", {}).get("number")  # None → P/F
            is_pf   = (name in PASS_FAIL_COURSES) or (score is None)
            taken[name] = {
                "credits":    credits,
                "score":      score if score is not None else 0,
                "pass_fail":  is_pf,
                "notion_raw": raw_name,
            }
        except (KeyError, IndexError, TypeError):
            continue
    return taken


def fetch_inprogress_courses() -> set:
    """回傳「修習中」課程名稱集合"""
    pages  = _query_notion("修習中")
    result = set()
    for p in pages:
        try:
            raw  = p["properties"]["課程名稱"]["title"][0]["plain_text"].strip()
            norm = _normalize(raw)
            if norm:
                result.add(norm)
        except (KeyError, IndexError, TypeError):
            pass
    return result


def get_student_taken(student) -> dict:
    """主要入口：優先用 Notion，失敗時回傳空字典"""
    result = fetch_notion_courses()
    if "_error" in result:
        return {}
    return result


# ══════════════════════════════════════════════════════════════
# 核心計算
# ══════════════════════════════════════════════════════════════
def compute_status(taken: dict) -> dict:
    taken_names = set(taken.keys())

    mgt_done    = [c for c in MGT_REQUIRED if c["name"] in taken_names]
    mgt_miss    = [c for c in MGT_REQUIRED if c["name"] not in taken_names]
    mgt_cr_done = sum(c["credits"] for c in mgt_done)

    req_done    = [c for c in REQUIRED_COURSES if c["name"] in taken_names]
    req_miss    = [c for c in REQUIRED_COURSES if c["name"] not in taken_names]
    req_cr_done = sum(c["credits"] for c in req_done)

    domain_status = {}
    for domain, info in ELECTIVE_DOMAINS.items():
        done_list = [c for c in info["courses"] if c["name"] in taken_names]
        cr_done   = sum(c["credits"] for c in done_list)
        domain_status[domain] = {
            "done":    cr_done,
            "courses": done_list,
            "missing": [c for c in info["courses"] if c["name"] not in taken_names],
            "color":   info["color"],
        }

    total_elective = sum(v["done"] for v in domain_status.values())
    elective_pass  = total_elective >= ELECTIVE_MIN_TOTAL
    total_cr       = sum(v["credits"] for v in taken.values())

    scored = [(v["score"], v["credits"])
              for v in taken.values()
              if not v.get("pass_fail") and v.get("score", 0) > 0]
    avg_score = round(
        sum(s * c for s, c in scored) / sum(c for _, c in scored), 1
    ) if scored else 0

    prereq_warnings = [
        f"已修「{post}」但尚未修先修課「{pre}」"
        for pre, post in PREREQS
        if post in taken_names and pre not in taken_names
    ]

    return {
        "mgt_required": {
            "done": mgt_done, "miss": mgt_miss,
            "credits_done": mgt_cr_done,
            "credits_need": MGT_REQUIRED_CREDITS,
            "pass": mgt_cr_done >= MGT_REQUIRED_CREDITS,
        },
        "required": {
            "done": req_done, "miss": req_miss,
            "credits_done": req_cr_done,
            "credits_need": REQUIRED_CREDITS,
            "pass": req_cr_done >= REQUIRED_CREDITS,
        },
        "domains":         domain_status,
        "total_credits":   total_cr,
        "elective_done":   total_elective,
        "elective_pass":   elective_pass,
        "elective_need":   ELECTIVE_MIN_TOTAL,
        "avg_score":       avg_score,
        "taken_names":     taken_names,
        "prereq_warnings": prereq_warnings,
        "graduation_ok": (
            mgt_cr_done >= MGT_REQUIRED_CREDITS and
            req_cr_done >= REQUIRED_CREDITS and
            elective_pass
        ),
    }
