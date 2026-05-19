import streamlit as st
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# 確保 .env 從專案根目錄讀取
from dotenv import load_dotenv
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(_root, ".env"), override=True)

import utils.data as _data
_data.NOTION_TOKEN = os.getenv("NOTION_TOKEN", "")
_data.NOTION_DB_ID = os.getenv("NOTION_DB_ID", "")

from utils.data import (get_student_taken, fetch_inprogress_courses, compute_status,
                          ALL_ELECTIVES, DOMAIN_COLORS,
                          ELECTIVE_MIN_SCHOOL, ELECTIVE_EXTERNAL_MAX, ELECTIVE_TOTAL_REQUIRED,
                          OTHER_DOMAIN_NAMES)

st.set_page_config(page_title="畢業進度儀表板", page_icon="📊", layout="wide")

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


# ── 讀取資料 ──────────────────────────────────────────────────
with st.spinner("從 Notion 讀取修課紀錄…"):
    taken      = get_student_taken()
    inprogress = fetch_inprogress_courses()

if not taken:
    st.error("❌ 無法從 Notion 讀取資料")
    st.info(f"📁 .env 路徑：{_root}/.env")
    st.info(f"Token：{os.getenv('NOTION_TOKEN','(未設定)')[:15]}...")
    st.info(f"DB ID：{os.getenv('NOTION_DB_ID','(未設定)')}")
    st.warning("請確認：\n1. Integration 已連接到「個人修課紀錄」Database\n2. 修課狀態選項名稱是「完成」")
    st.stop()

s = compute_status(taken, inprogress)



# ── 先修警示 ─────────────────────────────────────────────────
for w in s.get("prereq_warnings", []):
    st.warning(f"⚠️ {w}")

# ── 畢業判斷 Banner ──────────────────────────────────────────
if s["graduation_ok"]:
    st.markdown("""<div style='background:linear-gradient(135deg,#dcfce7,#dcfce7);
        border:1px solid #86efac;border-radius:12px;padding:18px 24px;
        display:flex;align-items:center;gap:16px;margin-bottom:20px'>
        <div style='font-size:32px'>🎉</div>
        <div><b style='color:#16a34a;font-size:16px'>恭喜！已符合所有畢業門檻</b>
        <div style='color:#78716c;font-size:13px;margin-top:3px'>
          管院共構必修、系訂必修及系選修 30 學分均已達標</div></div>
    </div>""", unsafe_allow_html=True)
else:
    problems = []
    if not s["required"]["pass"]:
        problems.append(f"系訂必修仍缺 {s['required']['credits_need']-s['required']['credits_done']} 學分（{len(s['required']['miss'])} 門課）")
    if not s["mgt_required"]["pass"]:
        problems.append(f"管院共構必修缺 {s['mgt_required']['credits_need']-s['mgt_required']['credits_done']} 學分")
    if not s["elective_pass"]:
        problems.append(f"系選修僅修 {s['elective_done']} 學分，還需 {s['elective_need']-s['elective_done']} 學分")
    st.markdown(f"""<div style='background:linear-gradient(135deg,#fef3c7,#fee2e2);
        border:1px solid #fca5a5;border-radius:12px;padding:18px 24px;margin-bottom:20px'>
        <b style='color:#dc2626;font-size:15px'>⚠️ 尚未符合畢業條件</b>
        <ul style='color:#1c1917;margin:8px 0 0 16px;font-size:13px;line-height:2.2'>
        {''.join(f'<li>{p}</li>' for p in problems)}</ul>
    </div>""", unsafe_allow_html=True)

# ── KPI 卡片 ─────────────────────────────────────────────────
req_pct = int(s["required"]["credits_done"] / s["required"]["credits_need"] * 100)
mgt_pct = int(s["mgt_required"]["credits_done"] / s["mgt_required"]["credits_need"] * 100)

c1, c2, c3, c4, c5 = st.columns(5)
for col, title, val, sub, color in [
    (c1, "總修習學分",   str(s["total_credits"]),  "學分",                              "#4f8ef7"),
    (c2, "系訂必修",     f"{req_pct}%",            f"{s['required']['credits_done']}/{s['required']['credits_need']} 學分",
                                                                                         "#2ecc8a" if req_pct==100 else "#f5c518"),
    (c3, "管院共構必修", f"{mgt_pct}%",            f"{s['mgt_required']['credits_done']}/{s['mgt_required']['credits_need']} 學分",
                                                                                         "#2ecc8a" if mgt_pct==100 else "#f5c518"),
    (c4, "系選修學分",   str(s["elective_done"]),  f"需 {ELECTIVE_TOTAL_REQUIRED} 學分（本系≥{ELECTIVE_MIN_SCHOOL}）", "#2ecc8a" if s["elective_pass"] else "#ff4d6d"),
    (c5, "加權平均分數", str(s["avg_score"]),       "排除 P/F 課程",                    "#7c5cfc"),
]:
    with col:
        st.markdown(f"""<div class='card'>
          <div class='card-title'>{title}</div>
          <div class='card-value' style='color:{color}'>{val}</div>
          <div style='font-size:12px;color:#78716c;margin-top:6px'>{sub}</div>
        </div>""", unsafe_allow_html=True)

# ── 修習中提示 ───────────────────────────────────────────────
if inprogress:
    names = "、".join(sorted(inprogress.keys()))
    st.markdown(f"""<div style='background:#eff6ff;border:1px solid #7c5cfc;border-radius:10px;
        padding:12px 18px;margin-bottom:20px;font-size:13px;color:#7c3aed'>
        🔄 <b>修習中</b>（本學期）：{names}
    </div>""", unsafe_allow_html=True)

# ── 圓餅圖 + 領域進度 ────────────────────────────────────────
col_l, col_r = st.columns([1, 1.5], gap="large")

with col_l:
    st.markdown("<div class='section-heading'>學分分布</div>", unsafe_allow_html=True)
    other_cr = sum(v["credits"] for v in s.get("other_taken", {}).values())
    pie_labels = ["系訂必修", "管院共構必修", "系選修"]
    pie_values = [s["required"]["credits_done"], s["mgt_required"]["credits_done"], s["elective_done"]]
    pie_colors = ["#4f8ef7","#7c5cfc","#2ecc8a"]
    if other_cr > 0:
        pie_labels.append("通識/其他")
        pie_values.append(other_cr)
        pie_colors.append("#64748b")

    fig = go.Figure(go.Pie(
        labels=pie_labels,
        values=pie_values,
        hole=0.62,
        marker=dict(colors=pie_colors, line=dict(color="#ffffff", width=3)),
        textfont=dict(color="#1c1917", size=12),
        hovertemplate="%{label}: %{value} 學分<extra></extra>",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=10,b=10,l=10,r=10),
        legend=dict(font=dict(color="#1c1917",size=12),bgcolor="rgba(0,0,0,0)"),
        annotations=[dict(text=f"<b>{s['total_credits']}</b><br>學分",
                          x=0.5,y=0.5,font=dict(size=18,color="#1c1917"),showarrow=False)]
    )
    st.plotly_chart(fig, width='stretch')

with col_r:
    st.markdown("<div class='section-heading'>各領域選修進度</div>", unsafe_allow_html=True)

    elec_pct = min(100, int(s["elective_done"] / ELECTIVE_TOTAL_REQUIRED * 100))
    ec = "#2ecc8a" if s["elective_pass"] else "#ff4d6d"
    st.markdown(f"""<div style='margin-bottom:22px'>
      <div style='display:flex;justify-content:space-between;margin-bottom:6px'>
        <b style='font-size:14px'>系選修總計</b>
        <span class='badge {"badge-pass" if s["elective_pass"] else "badge-fail"}'>
          {"✓ 達標" if s["elective_pass"] else f"尚缺 {ELECTIVE_TOTAL_REQUIRED - s['elective_done']} 學分"}
        </span>
      </div>
      <div style='display:flex;align-items:center;gap:12px'>
        <div class='prog-wrap' style='flex:1'>
          <div class='prog-fill' style='width:{elec_pct}%;background:{ec}'></div>
        </div>
        <span style='font-family:'DM Mono',monospace;font-size:12px;color:#78716c'>
          {s["elective_done"]}/{ELECTIVE_TOTAL_REQUIRED}
        </span>
      </div>
      <div style='font-size:11px;color:#78716c;margin-top:5px'>
        本系課程至少 {ELECTIVE_MIN_SCHOOL} 學分，他系至多承認 {ELECTIVE_EXTERNAL_MAX} 學分（通識、體育除外）
      </div>
    </div>""", unsafe_allow_html=True)

    # 以 ALL_ELECTIVES 為基準，列出全部五大領域（含未修的領域）
    for domain in ALL_ELECTIVES.keys():
        color   = DOMAIN_COLORS.get(domain, "#78716c")
        info    = s["domains"].get(domain, {"done": 0})
        done_cr = info["done"]
        bar     = min(100, int(done_cr / s["elective_need"] * 100))
        st.markdown(f"""<div style='margin-bottom:14px'>
          <div style='display:flex;justify-content:space-between;margin-bottom:4px'>
            <span style='font-size:13px'>{domain}</span>
            <span style='font-family:'DM Mono',monospace;font-size:12px;color:{color}'>{done_cr} 學分</span>
          </div>
          <div class='prog-wrap'>
            <div class='prog-fill' style='width:{bar}%;background:{color}'></div>
          </div>
        </div>""", unsafe_allow_html=True)

# ── 通識 / 其他已修課程 ──────────────────────────────────────
other_taken = s.get("other_taken", {})
if other_taken:
    other_cr = sum(v["credits"] for v in other_taken.values())
    st.markdown(f"""
    <div style='margin-top:24px'>
      <div class='section-heading'>通識 / 其他已修課程</div>
      <div style='font-size:12px;color:#78716c;margin-bottom:12px'>
        不計入系選修門檻，但計入總修習學分（共 {other_cr} 學分）
      </div>
    </div>""", unsafe_allow_html=True)

    rows = "".join(f"""<tr>
        <td style='color:#1c1917'>{name}</td>
        <td style='color:#78716c'>{', '.join(info.get('belonging', ['其他'])) or '其他'}</td>
        <td style='font-family:'DM Mono',monospace;color:#78716c'>{info['credits']}</td>
        <td style='font-family:'DM Mono',monospace;color:#64748b'>{int(info['score']) if info.get('score') else '—'}</td>
        <td><span class='badge badge-pass'>✓ 完成</span></td>
    </tr>""" for name, info in other_taken.items())

    st.markdown(f"""<div style='background:#ffffff;border:1px solid #e2e0d9;border-radius:12px;overflow:hidden'>
    <table><thead><tr>
      <th>課程名稱</th><th>類別</th><th>學分</th><th>成績</th><th>狀態</th>
    </tr></thead><tbody>{rows}</tbody></table></div>""", unsafe_allow_html=True)

# ── 缺修必修 ─────────────────────────────────────────────────
miss_all = [
    {**c, "category": "管院共構"} for c in s["mgt_required"]["miss"]
] + [
    {**c, "category": "系訂必修"} for c in s["required"]["miss"]
]

if miss_all:
    st.markdown("<div class='section-heading' style='margin-top:8px'>❌ 缺修必修課程</div>",
                unsafe_allow_html=True)
    rows = "".join(f"""<tr>
        <td>{c['name']}</td>
        <td>{c['category']}</td>
        <td>{c['credits']} 學分</td>
        <td>{c.get('semester','')}</td>
        <td><span class='badge badge-fail'>未修</span></td>
    </tr>""" for c in miss_all)
    st.markdown(f"""<div style='background:#ffffff;border:1px solid #e2e0d9;border-radius:12px;overflow:hidden'>
    <table><thead><tr><th>課程名稱</th><th>類別</th><th>學分</th><th>建議修課時間</th><th>狀態</th></tr></thead>
    <tbody>{rows}</tbody></table></div>""", unsafe_allow_html=True)
