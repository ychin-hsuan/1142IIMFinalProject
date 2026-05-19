import streamlit as st
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.data import get_student_taken, fetch_inprogress_courses, compute_status

st.set_page_config(page_title="畢業進度儀表板", page_icon="📊", layout="wide")
st.markdown(st.session_state.get("COMMON_CSS", ""), unsafe_allow_html=True)

st.markdown("""
<div style='padding:24px 0 16px'>
  <div style='font-size:11px;letter-spacing:3px;color:#4f8ef7;font-weight:700;text-transform:uppercase'>
    畢業進度儀表板
  </div>
  <h2 style='font-size:28px;font-weight:900;margin:4px 0'>修課狀況總覽</h2>
</div>
""", unsafe_allow_html=True)

# ── 讀取資料 ──────────────────────────────────────────────────
import os
from dotenv import load_dotenv

# 確保從專案根目錄讀取 .env
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(_root, ".env"), override=True)

# 重新讀取環境變數（pages 執行時 data.py 可能尚未載入 .env）
import utils.data as _data
_data.NOTION_TOKEN = os.getenv("NOTION_TOKEN", "")
_data.NOTION_DB_ID = os.getenv("NOTION_DB_ID", "")

with st.spinner("從 Notion 讀取修課紀錄…"):
    taken      = get_student_taken()
    inprogress = fetch_inprogress_courses()

if not taken:
    token_ok = bool(os.getenv("NOTION_TOKEN"))
    db_ok    = bool(os.getenv("NOTION_DB_ID"))
    st.error("❌ 無法從 Notion 讀取資料")
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("NOTION_TOKEN", "✓ 已設定" if token_ok else "✗ 未設定")
    with col_b:
        st.metric("NOTION_DB_ID", "✓ 已設定" if db_ok else "✗ 未設定")
    st.info(f"📁 .env 讀取路徑：{_root}/.env")
    st.info(f"Token 前10碼：{os.getenv('NOTION_TOKEN','')[:10]}...")
    st.info(f"DB ID：{os.getenv('NOTION_DB_ID','')}")
    st.warning("請確認：\n1. Integration 已連接到「個人修課紀錄」Database\n2. 修課狀態選項名稱是「完成」")
    st.stop()

s = compute_status(taken)

# ── 先修警示 ─────────────────────────────────────────────────
if s["prereq_warnings"]:
    for w in s["prereq_warnings"]:
        st.warning(f"⚠️ {w}")

# ── 畢業判斷 Banner ──────────────────────────────────────────
if s["graduation_ok"]:
    st.markdown("""<div style='background:linear-gradient(135deg,#0e3d2a,#0b2e20);
        border:1px solid #2ecc8a;border-radius:12px;padding:18px 24px;
        display:flex;align-items:center;gap:16px;margin-bottom:20px'>
        <div style='font-size:32px'>🎉</div>
        <div><b style='color:#2ecc8a;font-size:16px'>恭喜！已符合所有畢業門檻</b>
        <div style='color:#7a8099;font-size:13px;margin-top:3px'>
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
    st.markdown(f"""<div style='background:linear-gradient(135deg,#2e1a0e,#3d0e1a);
        border:1px solid #ff4d6d;border-radius:12px;padding:18px 24px;margin-bottom:20px'>
        <b style='color:#ff4d6d;font-size:15px'>⚠️ 尚未符合畢業條件</b>
        <ul style='color:#e8ecf4;margin:8px 0 0 16px;font-size:13px;line-height:2.2'>
        {''.join(f'<li>{p}</li>' for p in problems)}</ul>
    </div>""", unsafe_allow_html=True)

# ── KPI 卡片 ─────────────────────────────────────────────────
req_pct = int(s["required"]["credits_done"] / s["required"]["credits_need"] * 100)
mgt_pct = int(s["mgt_required"]["credits_done"] / s["mgt_required"]["credits_need"] * 100)

c1, c2, c3, c4, c5 = st.columns(5)
kpis = [
    (c1, "總修習學分",   str(s["total_credits"]),    "學分",                              "#4f8ef7"),
    (c2, "系訂必修",     f"{req_pct}%",              f"{s['required']['credits_done']}/{s['required']['credits_need']} 學分",
                                                                                          "#2ecc8a" if req_pct==100 else "#f5c518"),
    (c3, "管院共構必修", f"{mgt_pct}%",              f"{s['mgt_required']['credits_done']}/{s['mgt_required']['credits_need']} 學分",
                                                                                          "#2ecc8a" if mgt_pct==100 else "#f5c518"),
    (c4, "系選修學分",   str(s["elective_done"]),    f"最低需 {s['elective_need']} 學分", "#2ecc8a" if s["elective_pass"] else "#ff4d6d"),
    (c5, "加權平均分數", str(s["avg_score"]),         "排除 P/F 課程",                    "#7c5cfc"),
]
for col, title, val, sub, color in kpis:
    with col:
        st.markdown(f"""<div class='card'>
          <div class='card-title'>{title}</div>
          <div class='card-value' style='color:{color}'>{val}</div>
          <div style='font-size:12px;color:#7a8099;margin-top:6px'>{sub}</div>
        </div>""", unsafe_allow_html=True)

# ── 修習中提示 ───────────────────────────────────────────────
if inprogress:
    names = "、".join(sorted(inprogress))
    st.markdown(f"""<div style='background:#1a1a35;border:1px solid #7c5cfc;border-radius:10px;
        padding:12px 18px;margin-bottom:20px;font-size:13px;color:#c0b0ff'>
        🔄 <b>修習中</b>（本學期）：{names}
    </div>""", unsafe_allow_html=True)

# ── 圓餅圖 + 領域進度 ────────────────────────────────────────
col_l, col_r = st.columns([1, 1.5], gap="large")

with col_l:
    st.markdown("<div class='section-heading'>學分分布</div>", unsafe_allow_html=True)
    fig = go.Figure(go.Pie(
        labels=["系訂必修", "管院共構必修", "系選修"],
        values=[s["required"]["credits_done"],
                s["mgt_required"]["credits_done"],
                s["elective_done"]],
        hole=0.62,
        marker=dict(colors=["#4f8ef7","#7c5cfc","#2ecc8a"],
                    line=dict(color="#0d0f14", width=3)),
        textfont=dict(color="#e8ecf4", size=12),
        hovertemplate="%{label}: %{value} 學分<extra></extra>",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=10,b=10,l=10,r=10),
        legend=dict(font=dict(color="#e8ecf4",size=12),bgcolor="rgba(0,0,0,0)"),
        annotations=[dict(text=f"<b>{s['total_credits']}</b><br>學分",
                          x=0.5,y=0.5,font=dict(size=18,color="#e8ecf4"),showarrow=False)]
    )
    st.plotly_chart(fig, use_container_width=True)

with col_r:
    st.markdown("<div class='section-heading'>各領域選修進度</div>", unsafe_allow_html=True)

    elec_pct = min(100, int(s["elective_done"] / s["elective_need"] * 100))
    ec = "#2ecc8a" if s["elective_pass"] else "#ff4d6d"
    st.markdown(f"""<div style='margin-bottom:22px'>
      <div style='display:flex;justify-content:space-between;margin-bottom:6px'>
        <b style='font-size:14px'>系選修總計</b>
        <span class='badge {"badge-pass" if s["elective_pass"] else "badge-fail"}'>
          {"✓ 達標" if s["elective_pass"] else f"尚缺 {s['elective_need']-s['elective_done']} 學分"}
        </span>
      </div>
      <div style='display:flex;align-items:center;gap:12px'>
        <div class='prog-wrap' style='flex:1'>
          <div class='prog-fill' style='width:{elec_pct}%;background:{ec}'></div>
        </div>
        <span style='font-family:Space Mono,monospace;font-size:12px;color:#7a8099'>
          {s["elective_done"]}/{s["elective_need"]}
        </span>
      </div>
    </div>""", unsafe_allow_html=True)

    for domain, info in s["domains"].items():
        bar = min(100, int(info["done"] / s["elective_need"] * 100))
        st.markdown(f"""<div style='margin-bottom:14px'>
          <div style='display:flex;justify-content:space-between;margin-bottom:4px'>
            <span style='font-size:13px'>{domain}</span>
            <span style='font-family:Space Mono,monospace;font-size:12px;color:{info["color"]}'>{info["done"]} 學分</span>
          </div>
          <div class='prog-wrap'>
            <div class='prog-fill' style='width:{bar}%;background:{info["color"]}'></div>
          </div>
        </div>""", unsafe_allow_html=True)

# ── 缺修必修 ─────────────────────────────────────────────────
miss_req = s["required"]["miss"] + s["mgt_required"]["miss"]
# 排除修習中的
miss_req = [c for c in miss_req if c["name"] not in inprogress]

if miss_req:
    st.markdown("<div class='section-heading' style='margin-top:8px'>❌ 缺修必修課程</div>",
                unsafe_allow_html=True)
    rows = "".join(f"""<tr>
        <td>{c['name']}</td>
        <td>{'管院共構' if c in s['mgt_required']['miss'] else '系訂必修'}</td>
        <td>{c['credits']} 學分</td>
        <td>{c.get('semester','')}</td>
        <td><span class='badge badge-fail'>未修</span></td>
    </tr>""" for c in miss_req)
    st.markdown(f"""<div style='background:#151820;border:1px solid #2a2f42;border-radius:12px;overflow:hidden'>
    <table><thead><tr><th>課程名稱</th><th>類別</th><th>學分</th><th>建議修課時間</th><th>狀態</th></tr></thead>
    <tbody>{rows}</tbody></table></div>""", unsafe_allow_html=True)
