# utils/data.py  ── 114 入學課程地圖 + Notion API
import os, requests
from dotenv import load_dotenv

load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN", "")
NOTION_DB_ID = os.getenv("NOTION_DB_ID", "")   # 個人修課紀錄

# ══════════════════════════════════════════════════════════════
# 課程清單（用於判斷缺修）
# ══════════════════════════════════════════════════════════════
MGT_REQUIRED = [
    {"name": "人工智慧語言與產業應用", "credits": 3, "semester": "大一上"},
    {"name": "統計學(1)",              "credits": 3, "semester": "大一上"},
    {"name": "會計學(1)",              "credits": 3, "semester": "大一下"},
    {"name": "經濟學(1)",              "credits": 3, "semester": "大二上暑"},
]
MGT_REQUIRED_CREDITS = 12

# ── 系訂必修（依 PDF 114 入學版逐一確認）──────────────────
# 大一上：計算機概論3、程式設計(1)4、微積分3、統計學(2)3
# 大一下：程式設計(2)4、資料結構3、商業溝通2
# 大二上：電腦網路3、資料庫管理3、網頁程式設計(1)3
# 大二下：管理資訊系統3
# 大三上：系統分析與設計3、管理資訊系統（大二下）
# 大三上：資訊倫理與法律3
# 大三下：畢業專題(1)3（P/F）
# 大四上：資訊管理專題實作(1)1
# 大四下：畢業專題(2)3（P/F）、資訊管理專題實作(2)1
REQUIRED_COURSES = [
    # 大一上
    {"name": "計算機概論",          "credits": 3, "semester": "大一上"},
    {"name": "程式設計(1)",         "credits": 4, "semester": "大一上"},
    {"name": "微積分",              "credits": 3, "semester": "大一上"},
    {"name": "統計學(2)",           "credits": 3, "semester": "大一上"},
    # 大一下
    {"name": "程式設計(2)",         "credits": 4, "semester": "大一下"},
    {"name": "資料結構",            "credits": 3, "semester": "大一下"},
    {"name": "商業溝通",            "credits": 2, "semester": "大一下"},
    # 大二上
    {"name": "電腦網路",            "credits": 3, "semester": "大二上"},
    {"name": "資料庫管理",          "credits": 3, "semester": "大二上"},
    {"name": "網頁程式設計(1)",     "credits": 3, "semester": "大二上"},
    # 大二下
    {"name": "管理資訊系統",        "credits": 3, "semester": "大二下"},
    # 大三上
    {"name": "系統分析與設計",      "credits": 3, "semester": "大三上"},
    {"name": "資訊倫理與法律",      "credits": 3, "semester": "大三上"},
    # 大三下
    {"name": "畢業專題(1)",         "credits": 3, "semester": "大三下"},   # P/F
    # 大四上
    {"name": "資訊管理專題實作(1)", "credits": 1, "semester": "大四上"},
    # 大四下
    {"name": "畢業專題(2)",         "credits": 3, "semester": "大四下"},   # P/F
    {"name": "資訊管理專題實作(2)", "credits": 1, "semester": "大四下"},
]
REQUIRED_CREDITS = 48
PASS_FAIL_COURSES = {"畢業專題(1)", "畢業專題(2)"}
ELECTIVE_MIN_TOTAL     = 30   # 本系選修最低下限
ELECTIVE_MIN_SCHOOL    = 30   # 系內開設課程至少需修
ELECTIVE_EXTERNAL_MAX  = 12   # 他系選修至多承認
ELECTIVE_TOTAL_REQUIRED = 42  # 系選修畢業門檻總計
# ══════════════════════════════════════════════════════════════
# 完整系選修課程清單（依 PDF 114 入學版，供模擬選課頁使用）
# ══════════════════════════════════════════════════════════════
ALL_ELECTIVES = {
    "企業管理": [
        {"name": "資訊管理導論",            "credits": 3, "semester": "大一下"},
        {"name": "行銷管理",                "credits": 3, "semester": "大二上"},
        {"name": "生產與作業管理",          "credits": 3, "semester": "大二上"},
        {"name": "人力資源管理",            "credits": 3, "semester": "大三上"},
        {"name": "物流與供應鏈管理",        "credits": 3, "semester": "大三上"},
        {"name": "財務管理",                "credits": 3, "semester": "大三下"},
        {"name": "顧客關係管理與商業智慧",  "credits": 3, "semester": "大四上"},
        {"name": "專案管理",                "credits": 3, "semester": "大四上"},
        {"name": "管理科學",                "credits": 3, "semester": "大四上"},
        {"name": "服務科學與管理",          "credits": 3, "semester": "大四下"},
        {"name": "數位轉型全球觀點",        "credits": 2, "semester": "大四下"},
        {"name": "精實供應鏈管理",          "credits": 3, "semester": "大四下"},
        {"name": "知識管理",                "credits": 3, "semester": "大四下"},
    ],
    "企業資訊應用": [
        {"name": "網路行銷",                "credits": 3, "semester": "大三上"},
        {"name": "電子商務",                "credits": 3, "semester": "大三下"},
        {"name": "程式交易",                "credits": 3, "semester": "大四上"},
        {"name": "大數據應用電子商務",      "credits": 3, "semester": "大四上"},
        {"name": "企業資源規劃",            "credits": 3, "semester": "大四下"},
        {"name": "數位行銷",                "credits": 3, "semester": "大四下"},
    ],
    "資訊技術": [
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
    ],
    "資訊安全": [
        {"name": "資訊安全導論",            "credits": 3, "semester": "大二下"},
        {"name": "資訊系統稽核與管理",      "credits": 3, "semester": "大三上"},
        {"name": "區塊鏈實務與應用",        "credits": 3, "semester": "大三上"},
        {"name": "網路安全",                "credits": 3, "semester": "大三下"},
        {"name": "網路攻防技術與應用",      "credits": 3, "semester": "大四上"},
        {"name": "醫療系統安全",            "credits": 3, "semester": "大四上"},
    ],
    "數據創新與智能互動": [
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
        {"name": "資訊科技使用者調查法",    "credits": 2, "semester": "大四上"},
        {"name": "數據管理工具研析",        "credits": 3, "semester": "大四下"},
        {"name": "數據創新與智能互動專題",  "credits": 2, "semester": "大四下"},
        {"name": "大數據處理與分析技術",    "credits": 3, "semester": "大四下"},
    ],
    "產業實務": [
        {"name": "資訊管理專題實作(1)",     "credits": 1, "semester": "大四上",
         "note": "已列於系必修，此處亦計入產業實務"},
        {"name": "校外實習",               "credits": 3, "semester": "大三上"},
        {"name": "資訊管理專題實作(2)",     "credits": 1, "semester": "大四下",
         "note": "已列於系必修，此處亦計入產業實務"},
        {"name": "企業實習",               "credits": 6, "semester": "大四下",
         "note": "限大四，不得與台塑企業實習同學期"},
        {"name": "台塑企業實習",           "credits": 9, "semester": "大四下",
         "note": "不得與企業實習同學期"},
    ],
}


PREREQS = [
    ("程式設計(1)",     "程式設計(2)"),
    ("統計學(1)",       "統計學(2)"),
    ("網頁程式設計(1)", "網頁程式設計(2)"),
    ("資料庫管理",      "資料庫程式規劃"),
]

DOMAIN_COLORS = {
    # 系選修五大領域（計入系選修門檻）
    "企業管理":          "#4f8ef7",
    "企業資訊應用":      "#f5c518",
    "資訊技術":          "#7c5cfc",
    "資訊安全":          "#ff4d6d",
    "數據創新與智能互動":"#2ecc8a",
    "產業實務":          "#f97316",
}

# 通識/英文/體育等領域 → 不計入系選修，但計入 other_taken 顯示
OTHER_DOMAIN_NAMES = {
    "英文閱讀與寫作",
    "基礎英文（A）",
    "基礎英文（B）",
    "基礎英文(A)",
    "基礎英文(B)",
    "跨域學習與實踐",
    "運算思維",
    "自然科學",
    "社會科學",
    "人文藝術",
    "公民與社會探究",
    "藝術與人文思維",
    "多元課程",
    "英文",
    "通識",
    "體育",
}

NAME_MAP = {
    "程式設計1":          "程式設計(1)",
    "程式設計2":          "程式設計(2)",
    "會計學1":            "會計學(1)",
    "經濟學1":            "經濟學(1)",
    "統計學1":            "統計學(1)",
    "統計學2":            "統計學(2)",
    "網頁程式設計1":      "網頁程式設計(1)",
    "網頁程式設計2":      "網頁程式設計(2)",
    "管理學":             "商業溝通",
    "資料庫":             "資料庫管理",
    # 通識/體育 → 略過（不計入畢業審查）
    "英文閱讀與寫作":     None,
    "體育大一(2)":        None,
    "體育":               None,
    "體育大二(1)":        None,
    "體育大二(2)":        None,
}

def _normalize(raw: str):
    # 清除 Notion bold 標記（** 或 * ）和多餘空白
    name = raw.strip().strip("*").strip()
    return NAME_MAP.get(name, name)

def _headers() -> dict:
    return {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }

def _get_credits(prop: dict) -> float:
    """支援 number 和 rollup"""
    if prop.get("type") == "number":
        return prop.get("number") or 0
    if prop.get("type") == "rollup":
        arr = prop.get("rollup", {}).get("array", [])
        if arr and arr[0].get("type") == "number":
            return arr[0].get("number") or 0
    return 0

# ══════════════════════════════════════════════════════════════
# 畢業審查總覽 page ID → 領域選修 快取
# ══════════════════════════════════════════════════════════════
_course_meta_cache: dict[str, dict] = {}   # page_id → {elective_domain, belonging}

def fetch_course_meta(page_id: str) -> dict:
    """
    查詢「畢業審查總覽」裡的單一課程 page，
    取得「所屬領域」和「領域選修」欄位。
    結果會快取，避免重複查詢。
    """
    if page_id in _course_meta_cache:
        return _course_meta_cache[page_id]

    try:
        res   = requests.get(
            f"https://api.notion.com/v1/pages/{page_id}",
            headers=_headers(), timeout=8,
        )
        props = res.json().get("properties", {})

        # 所屬領域（multiselect）
        belonging = [
            opt["name"]
            for opt in props.get("所屬領域", {}).get("multi_select", [])
        ]

        # 領域選修（select）
        sel = props.get("領域選修", {})
        if sel.get("type") == "select" and sel.get("select"):
            elective_domain = sel["select"]["name"]
        else:
            elective_domain = None

        meta = {"belonging": belonging, "elective_domain": elective_domain}
        _course_meta_cache[page_id] = meta
        return meta
    except Exception:
        return {"belonging": [], "elective_domain": None}


def _query_notion(status: str) -> list:
    """查詢個人修課紀錄，支援分頁"""
    if not NOTION_TOKEN or not NOTION_DB_ID:
        return []
    payload = {
        "filter": {"property": "修課狀態", "status": {"equals": status}},
        "page_size": 100,
    }
    all_pages = []
    try:
        while True:
            res  = requests.post(
                f"https://api.notion.com/v1/databases/{NOTION_DB_ID}/query",
                headers=_headers(), json=payload, timeout=10,
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


def _parse_page(page: dict) -> tuple:
    """
    解析個人修課紀錄一筆資料。
    透過 Relation 欄位「畢業審查總覽」取得 page_id，
    再查詢該課程的「所屬領域」和「領域選修」。
    """
    props = page.get("properties", {})
    try:
        raw_name = props["課程名稱"]["title"][0]["plain_text"].strip().strip("*").strip()
        name     = _normalize(raw_name)
        if name is None:
            return None, None

        credits = _get_credits(props.get("學分", {}))
        score   = props.get("成績", {}).get("number")

        # 透過 Relation 拿到畢業審查總覽的 page_id
        relation = props.get("畢業審查總覽", {}).get("relation", [])
        # 注意：欄位名稱後面可能有空格「畢業審查總覽 」
        if not relation:
            relation = props.get("畢業審查總覽 ", {}).get("relation", [])

        meta = {"belonging": [], "elective_domain": None}
        if relation:
            ref_page_id = relation[0]["id"]
            meta = fetch_course_meta(ref_page_id)

        is_pf = (name in PASS_FAIL_COURSES)

        return name, {
            "credits":         credits,
            "score":           score if score is not None else 0,
            "pass_fail":       is_pf,
            "belonging":       meta["belonging"],
            "elective_domain": meta["elective_domain"],
            "raw":             raw_name,
        }
    except (KeyError, IndexError, TypeError):
        return None, None


def fetch_notion_courses() -> dict:
    """回傳「完成」的課程字典"""
    pages = _query_notion("完成")
    taken = {}
    for page in pages:
        name, data = _parse_page(page)
        if name and data:
            taken[name] = data
    return taken


def fetch_inprogress_courses() -> dict:
    """回傳「修習中」的課程字典"""
    pages = _query_notion("修習中")
    result = {}
    for page in pages:
        name, data = _parse_page(page)
        if name and data:
            result[name] = data
    return result


def get_student_taken() -> dict:
    return fetch_notion_courses()


# ══════════════════════════════════════════════════════════════
# 核心計算
# ══════════════════════════════════════════════════════════════
def compute_status(taken: dict, inprogress: dict = None) -> dict:
    if inprogress is None:
        inprogress = {}

    taken_names      = set(taken.keys())
    inprogress_names = set(inprogress.keys())

    # 管院共構必修
    mgt_taken   = {n: v for n, v in taken.items() if "管院共構" in v.get("belonging", [])}
    mgt_cr_done = sum(v["credits"] for v in mgt_taken.values())
    mgt_miss    = [c for c in MGT_REQUIRED
                   if c["name"] not in mgt_taken and c["name"] not in inprogress_names]

    # 系訂必修
    req_taken   = {n: v for n, v in taken.items() if "系必修" in v.get("belonging", [])}
    req_cr_done = sum(v["credits"] for v in req_taken.values())
    req_miss    = [c for c in REQUIRED_COURSES
                   if c["name"] not in req_taken and c["name"] not in inprogress_names]

    # 系選修 → 依「領域選修」分組（只計 DOMAIN_COLORS 內的領域）
    elective_taken = {n: v for n, v in taken.items()
                      if "系選修" in v.get("belonging", [])
                      and v.get("elective_domain") in DOMAIN_COLORS}

    # 通識 / 其他：
    # 條件1：belonging 不包含系必修/管院共構/系選修
    # 條件2：elective_domain 屬於 OTHER_DOMAIN_NAMES
    other_taken = {n: v for n, v in taken.items()
                   if (not any(b in ["系必修", "管院共構", "系選修"]
                               for b in v.get("belonging", [])))
                   or v.get("elective_domain") in OTHER_DOMAIN_NAMES}

    domain_status = {}
    for name, info in elective_taken.items():
        domain = info.get("elective_domain") or "未分類"
        color  = DOMAIN_COLORS.get(domain, "#7a8099")
        if domain not in domain_status:
            domain_status[domain] = {"done": 0, "courses": [], "color": color}
        domain_status[domain]["done"]    += info["credits"]
        domain_status[domain]["courses"].append({"name": name, "credits": info["credits"]})

    total_elective = sum(v["done"] for v in domain_status.values())
    elective_pass  = total_elective >= ELECTIVE_TOTAL_REQUIRED
    total_cr       = sum(v["credits"] for v in taken.values())

    scored = [(v["score"], v["credits"]) for v in taken.values()
              if not v.get("pass_fail") and v.get("score", 0) > 0]
    avg_score = round(
        sum(s * c for s, c in scored) / sum(c for _, c in scored), 1
    ) if scored else 0

    prereq_warnings = [
        f"已修「{post}」但尚未修先修課「{pre}」"
        for pre, post in PREREQS
        if post in (taken_names | inprogress_names)
        and pre not in (taken_names | inprogress_names)
    ]

    return {
        "mgt_required": {
            "done_names":   set(mgt_taken.keys()),
            "miss":         mgt_miss,
            "credits_done": mgt_cr_done,
            "credits_need": MGT_REQUIRED_CREDITS,
            "pass":         mgt_cr_done >= MGT_REQUIRED_CREDITS,
        },
        "required": {
            "done_names":   set(req_taken.keys()),
            "miss":         req_miss,
            "credits_done": req_cr_done,
            "credits_need": REQUIRED_CREDITS,
            "pass":         req_cr_done >= REQUIRED_CREDITS,
        },
        "domains":          domain_status,
        "total_credits":    total_cr,
        "elective_done":    total_elective,
        "elective_pass":    elective_pass,
        "elective_need":    ELECTIVE_TOTAL_REQUIRED,
        "elective_school_min": ELECTIVE_MIN_SCHOOL,
        "elective_external_max": ELECTIVE_EXTERNAL_MAX,
        "avg_score":        avg_score,
        "taken_names":      taken_names,
        "inprogress_names": inprogress_names,
        "prereq_warnings":  prereq_warnings,
        "other_taken":      other_taken,   # 通識/英文/其他（不計入系選修）
        "graduation_ok": (
            mgt_cr_done >= MGT_REQUIRED_CREDITS and
            req_cr_done >= REQUIRED_CREDITS and
            elective_pass
        ),
    }
