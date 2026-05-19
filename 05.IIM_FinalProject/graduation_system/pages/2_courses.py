import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from dotenv import load_dotenv
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(_root, ".env"), override=True)
import utils.data as _data
_data.NOTION_TOKEN = os.getenv("NOTION_TOKEN", "")
_data.NOTION_DB_ID = os.getenv("NOTION_DB_ID", "")

from utils.data import get_student_taken, fetch_inprogress_courses, compute_status, REQUIRED_COURSES, MGT_REQUIRED

st.set_page_config(page_title="修課明細查詢", page_icon="📋", layout="wide")

st.markdown(st.session_state.get("COMMON_CSS", ""), unsafe_allow_html=True)
# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:16px 12px 12px'>
      <div style='font-size:9px;letter-spacing:2px;color:#a8a29e;
                  font-weight:700;text-transform:uppercase;margin-bottom:3px'>
        CGU · IMIS · 114
      </div>
      <div style='font-size:15px;font-weight:900;color:#1c1917'>畢業初審系統</div>
    </div>
    <div style='padding:0 8px;font-size:9px;font-weight:700;letter-spacing:1.5px;
                text-transform:uppercase;color:#a8a29e;margin-bottom:4px'>導覽</div>
    """, unsafe_allow_html=True)
    st.page_link("app.py",                label="🏠  首頁")
    st.page_link("pages/1_dashboard.py",  label="📊  畢業進度儀表板")
    st.page_link("pages/2_courses.py",    label="📋  修課明細查詢")
    st.page_link("pages/3_ai_advisor.py", label="🤖  AI 選課顧問")
    st.page_link("pages/4_simulate.py",   label="🔮  模擬選課規劃")
    st.markdown("""<div style='padding:12px 12px 0;margin-top:8px;border-top:1px solid #e2e0d9'>
      <div style='font-size:11px;color:#a8a29e;line-height:1.9'>
        📘 課程地圖：114 入學<br>🏫 長庚大學 資管系
      </div></div>""", unsafe_allow_html=True)


with st.spinner("從 Notion 讀取資料…"):
    taken      = get_student_taken()
    inprogress = fetch_inprogress_courses()

if not taken and not inprogress:
    st.warning("⚠️ 無法讀取 Notion 資料，請確認 .env 設定。")
    st.stop()

s = compute_status(taken, inprogress)

# ── 篩選器 ──────────────────────────────────────────────
f1, f2, f3 = st.columns([2, 1, 1])
with f1:
    keyword = st.text_input("🔍  搜尋課程名稱", placeholder="輸入關鍵字…")
with f2:
    cat_filter = st.selectbox("課程類別", ["全部", "系必修", "管院共構", "系選修", "其他"])
with f3:
    status_filter = st.selectbox("修課狀態", ["全部", "完成", "修習中", "未修"])

# ── 整理課程清單 ─────────────────────────────────────────
all_courses = []

# 已完成的課程
for name, info in taken.items():
    belonging = info.get("belonging", [])
    cat = belonging[0] if belonging else "其他"
    all_courses.append({
        "name":    name,
        "credits": info["credits"],
        "score":   info["score"],
        "domain":  info.get("elective_domain") or "",
        "cat":     cat,
        "status":  "完成",
    })

# 修習中的課程
for name, info in inprogress.items():
    belonging = info.get("belonging", [])
    cat = belonging[0] if belonging else "其他"
    all_courses.append({
        "name":    name,
        "credits": info["credits"],
        "score":   None,
        "domain":  info.get("elective_domain") or "",
        "cat":     cat,
        "status":  "修習中",
    })

# 缺修必修
done_and_prog = {c["name"] for c in all_courses}
for c in REQUIRED_COURSES:
    if c["name"] not in done_and_prog:
        all_courses.append({
            "name": c["name"], "credits": c["credits"], "score": None,
            "domain": "", "cat": "系必修", "status": "未修",
        })
for c in MGT_REQUIRED:
    if c["name"] not in done_and_prog:
        all_courses.append({
            "name": c["name"], "credits": c["credits"], "score": None,
            "domain": "", "cat": "管院共構", "status": "未修",
        })

# ── 篩選 ─────────────────────────────────────────────────
filtered = all_courses
if keyword:
    filtered = [c for c in filtered if keyword in c["name"]]
if cat_filter != "全部":
    filtered = [c for c in filtered if cat_filter in c["cat"]]
if status_filter != "全部":
    filtered = [c for c in filtered if c["status"] == status_filter]

# ── 統計卡片 ─────────────────────────────────────────────
done_c  = sum(1 for c in filtered if c["status"] == "完成")
prog_c  = sum(1 for c in filtered if c["status"] == "修習中")
miss_c  = sum(1 for c in filtered if c["status"] == "未修")
total_cr= sum(c["credits"] for c in filtered if c["status"] == "完成")

m1, m2, m3, m4 = st.columns(4)
for col, label, val, color in [
    (m1, "篩選結果已完成", f"{done_c} 門",  "#2ecc8a"),
    (m2, "篩選結果修習中", f"{prog_c} 門",  "#7c5cfc"),
    (m3, "篩選結果未修",   f"{miss_c} 門",  "#ff4d6d"),
    (m4, "已完成學分",     f"{total_cr} 學分","#4f8ef7"),
]:
    with col:
        st.markdown(f"""<div class='card' style='padding:14px 20px'>
          <div style='font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#78716c;margin-bottom:4px'>{label}</div>
          <div style='font-family:'DM Mono',monospace;font-size:28px;font-weight:700;color:{color}'>{val}</div>
        </div>""", unsafe_allow_html=True)

# ── 課程表格 ─────────────────────────────────────────────
st.markdown("<div class='section-heading' style='margin-top:8px'>課程列表</div>", unsafe_allow_html=True)

STATUS_BADGE = {
    "完成":  "<span class='badge badge-pass'>✓ 完成</span>",
    "修習中":"<span class='badge badge-prog'>◎ 修習中</span>",
    "未修":  "<span class='badge badge-fail'>✗ 未修</span>",
}

rows_html = ""
for c in filtered:
    score_html = str(int(c["score"])) if c["score"] else "—"
    domain_html = f"<span style='font-size:12px;color:#78716c'>{c['domain']}</span>" if c["domain"] else "—"
    rows_html += f"""<tr>
        <td>{c['name']}</td>
        <td><span style='font-size:12px;color:#78716c'>{c['cat']}</span></td>
        <td>{domain_html}</td>
        <td style='font-family:'DM Mono',monospace'>{c['credits']}</td>
        <td>{score_html}</td>
        <td>{STATUS_BADGE[c['status']]}</td>
    </tr>"""

if filtered:
    st.markdown(f"""<div style='background:#ffffff;border:1px solid #e2e0d9;border-radius:12px;overflow:hidden'>
    <table><thead><tr>
      <th>課程名稱</th><th>類別</th><th>領域</th><th>學分</th><th>成績</th><th>狀態</th>
    </tr></thead><tbody>{rows_html}</tbody></table></div>""", unsafe_allow_html=True)
else:
    st.markdown("""<div style='text-align:center;padding:48px;color:#78716c'>
        <div style='font-size:32px;margin-bottom:8px'>🔍</div>
        <div>找不到符合條件的課程</div></div>""", unsafe_allow_html=True)
