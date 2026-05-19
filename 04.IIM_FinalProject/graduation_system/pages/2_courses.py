import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.data import get_student_taken, compute_status, REQUIRED_COURSES, MGT_REQUIRED, ELECTIVE_DOMAINS

st.set_page_config(page_title="修課明細查詢", page_icon="📋", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700;900&family=Space+Mono:wght@400;700&display=swap');
:root{--bg:#0d0f14;--surface:#151820;--surface2:#1c2030;--border:#2a2f42;
     --accent:#4f8ef7;--accent2:#7c5cfc;--green:#2ecc8a;--red:#ff4d6d;
     --yellow:#f5c518;--text:#e8ecf4;--muted:#7a8099;--radius:12px;}
html,body,[data-testid="stAppViewContainer"]{background:var(--bg)!important;color:var(--text)!important;font-family:'Noto Sans TC',sans-serif!important;}
[data-testid="stSidebar"]{background:var(--surface)!important;border-right:1px solid var(--border)!important;}
[data-testid="stSidebar"] *{color:var(--text)!important;}
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:18px 22px;margin-bottom:14px;}
.badge{display:inline-block;padding:3px 10px;border-radius:999px;font-size:11px;font-weight:700;}
.badge-pass{background:#0e3d2a;color:#2ecc8a;border:1px solid #2ecc8a;}
.badge-fail{background:#3d0e1a;color:#ff4d6d;border:1px solid #ff4d6d;}
.badge-warn{background:#3d3000;color:#f5c518;border:1px solid #f5c518;}
.badge-info{background:#0e2040;color:#4f8ef7;border:1px solid #4f8ef7;}
.section-heading{font-size:11px;font-weight:800;letter-spacing:3px;text-transform:uppercase;color:#7a8099;padding:6px 0 12px;border-bottom:1px solid var(--border);margin-bottom:20px;}
table{width:100%;border-collapse:collapse;font-size:14px;}
th{background:#1c2030;color:#7a8099;font-size:11px;letter-spacing:1.5px;text-transform:uppercase;padding:10px 14px;text-align:left;border-bottom:1px solid var(--border);}
td{padding:10px 14px;border-bottom:1px solid var(--border);color:var(--text);}
tr:hover td{background:#1c2030;}
[data-baseweb="input"] input{background:#1c2030!important;border-color:#2a2f42!important;color:var(--text)!important;}
[data-baseweb="select"] div{background:#1c2030!important;color:var(--text)!important;}
.stButton>button{background:linear-gradient(135deg,#4f8ef7,#7c5cfc)!important;color:#fff!important;border:none!important;border-radius:8px!important;font-weight:700!important;}
#MainMenu,footer,header{visibility:hidden;}[data-testid="stDecoration"]{display:none;}
</style>
""", unsafe_allow_html=True)

student = st.session_state.get("student", {"id":"B1344062","name":"示範學生","grade":"大三"})
taken   = get_student_taken(student)
s       = compute_status(taken)

st.markdown(f"""
<div style='padding:24px 0 16px'>
  <div style='font-size:11px;letter-spacing:3px;color:#4f8ef7;font-weight:700;text-transform:uppercase'>修課明細查詢</div>
  <h2 style='font-size:26px;font-weight:900;margin:4px 0'>
    {student['name']} <span style='color:#7a8099;font-weight:400;font-size:17px'>｜ {student['id']}</span>
  </h2>
</div>
""", unsafe_allow_html=True)

# ── 篩選器 ──────────────────────────────────────────────
f1, f2, f3 = st.columns([2, 1, 1])
with f1:
    keyword = st.text_input("🔍  搜尋課程名稱", placeholder="輸入關鍵字…")
with f2:
    cat_filter = st.selectbox("課程類別", ["全部", "系必修", "管院共必修"] + list(ELECTIVE_DOMAINS.keys()))
with f3:
    status_filter = st.selectbox("修課狀態", ["全部", "已修", "未修"])

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ── 整理所有課程清單 ─────────────────────────────────────
all_courses = []

for c in REQUIRED_COURSES:
    taken_info = taken.get(c["name"], {})
    all_courses.append({
        "name":     c["name"],
        "credits":  c["credits"],
        "category": "系必修",
        "semester": c.get("semester",""),
        "taken":    c["name"] in taken,
        "grade":    taken_info.get("grade",""),
        "score":    taken_info.get("score",""),
    })

for c in MGT_REQUIRED:
    taken_info = taken.get(c["name"], {})
    all_courses.append({
        "name":     c["name"],
        "credits":  c["credits"],
        "category": "管院共必修",
        "semester": c.get("semester",""),
        "taken":    c["name"] in taken,
        "grade":    taken_info.get("grade",""),
        "score":    taken_info.get("score",""),
    })

for domain, info in ELECTIVE_DOMAINS.items():
    for c in info["courses"]:
        taken_info = taken.get(c["name"], {})
        all_courses.append({
            "name":     c["name"],
            "credits":  c["credits"],
            "category": domain,
            "semester": "",
            "taken":    c["name"] in taken,
            "grade":    taken_info.get("grade",""),
            "score":    taken_info.get("score",""),
        })

# ── 套用篩選 ─────────────────────────────────────────────
filtered = all_courses
if keyword:
    filtered = [c for c in filtered if keyword in c["name"]]
if cat_filter != "全部":
    filtered = [c for c in filtered if c["category"] == cat_filter]
if status_filter == "已修":
    filtered = [c for c in filtered if c["taken"]]
elif status_filter == "未修":
    filtered = [c for c in filtered if not c["taken"]]

# ── 統計小卡 ───────────────────────────────────────────
taken_count  = sum(1 for c in filtered if c["taken"])
miss_count   = sum(1 for c in filtered if not c["taken"])
total_cr     = sum(c["credits"] for c in filtered if c["taken"])

m1, m2, m3 = st.columns(3)
for col, label, val, color in [
    (m1, "篩選結果已修", f"{taken_count} 門", "#2ecc8a"),
    (m2, "篩選結果未修", f"{miss_count} 門",  "#ff4d6d"),
    (m3, "篩選結果學分", f"{total_cr} 學分",   "#4f8ef7"),
]:
    with col:
        st.markdown(f"""<div class='card' style='padding:14px 20px'>
          <div style='font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#7a8099;margin-bottom:4px'>{label}</div>
          <div style='font-family:Space Mono,monospace;font-size:28px;font-weight:700;color:{color}'>{val}</div>
        </div>""", unsafe_allow_html=True)

# ── 課程表格 ─────────────────────────────────────────────
st.markdown("<div class='section-heading' style='margin-top:8px'>課程列表</div>", unsafe_allow_html=True)

def grade_color(g):
    if not g: return "#7a8099"
    if g.startswith("A"): return "#2ecc8a"
    if g.startswith("B"): return "#4f8ef7"
    if g.startswith("C"): return "#f5c518"
    return "#ff4d6d"

rows_html = ""
for c in filtered:
    status_badge = "<span class='badge badge-pass'>✓ 已修</span>" if c["taken"] \
               else "<span class='badge badge-fail'>✗ 未修</span>"
    cat_badge = f"<span class='badge badge-info' style='font-size:10px'>{c['category']}</span>"
    g = c.get("grade", "")
    grade_html = f"<b style='color:{grade_color(g)}'>{g}</b>" if g else "—"
    score_html = str(c["score"]) if c["score"] else "—"
    rows_html += f"""<tr>
        <td>{c['name']}</td>
        <td>{cat_badge}</td>
        <td style='font-family:Space Mono,monospace'>{c['credits']}</td>
        <td>{c.get('semester','') or '—'}</td>
        <td>{grade_html}</td>
        <td>{score_html}</td>
        <td>{status_badge}</td>
    </tr>"""

st.markdown(f"""
<div style='background:#151820;border:1px solid #2a2f42;border-radius:12px;overflow:hidden'>
<table>
  <thead><tr>
    <th>課程名稱</th><th>類別</th><th>學分</th>
    <th>建議修課時間</th><th>成績</th><th>分數</th><th>狀態</th>
  </tr></thead>
  <tbody>{rows_html}</tbody>
</table>
</div>
""", unsafe_allow_html=True)

if not filtered:
    st.markdown("""<div style='text-align:center;padding:48px;color:#7a8099'>
        <div style='font-size:32px;margin-bottom:8px'>🔍</div>
        <div>找不到符合條件的課程</div></div>""", unsafe_allow_html=True)
