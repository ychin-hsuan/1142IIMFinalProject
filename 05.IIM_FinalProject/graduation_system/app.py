import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title="畢業初審系統 | 長庚大學資管系",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

COMMON_CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&family=DM+Mono:wght@400;500&display=swap');
:root {
    --bg:#f5f4f1; --surface:#ffffff; --surface2:#f0efe9; --border:#e2e0d9;
    --accent:#2563eb; --green:#16a34a; --red:#dc2626; --yellow:#d97706;
    --purple:#7c3aed; --orange:#ea580c;
    --text:#1c1917; --text2:#57534e; --text3:#a8a29e; --radius:10px;
}
html,body,[data-testid="stAppViewContainer"]{
    background:var(--bg)!important; color:var(--text)!important;
    font-family:'Noto Sans TC',sans-serif!important;
}
/* ── 強制 sidebar 永遠展開、固定寬度 ── */
[data-testid="stSidebar"]{
    background:var(--surface)!important;
    border-right:1px solid var(--border)!important;
    min-width:220px!important; max-width:220px!important;
    width:220px!important;
}
[data-testid="stSidebar"][aria-expanded="false"]{
    min-width:220px!important; max-width:220px!important;
    transform:none!important; margin-left:0!important;
}
/* 隱藏 sidebar 的收合按鈕 */
button[kind="header"], [data-testid="collapsedControl"]{display:none!important;}
[data-testid="stSidebar"] *{color:var(--text)!important;}
[data-testid="stSidebarNav"]{display:none!important;}

/* ── 主內容靠左給 sidebar 空間 ── */
[data-testid="stAppViewContainer"] > .main{padding-left:0!important;}
.main .block-container{padding:1.5rem 2rem 2rem!important; max-width:100%!important;}

/* ── Cards ── */
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:16px 18px;margin-bottom:10px;}
.card-label{font-size:10px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:var(--text3);margin-bottom:5px;}
.card-value{font-family:'DM Mono',monospace;font-size:26px;font-weight:500;line-height:1;}
.card-sub{font-size:11px;color:var(--text3);margin-top:5px;}
/* ── Badges ── */
.badge{display:inline-flex;align-items:center;padding:2px 8px;border-radius:999px;font-size:11px;font-weight:600;}
.badge-pass{background:#dcfce7;color:var(--green);border:1px solid #86efac;}
.badge-fail{background:#fee2e2;color:var(--red);border:1px solid #fca5a5;}
.badge-warn{background:#fef3c7;color:var(--yellow);border:1px solid #fcd34d;}
.badge-info{background:#dbeafe;color:var(--accent);border:1px solid #93c5fd;}
.badge-prog{background:#ede9fe;color:var(--purple);border:1px solid #c4b5fd;}
/* ── Progress ── */
.prog-wrap{background:var(--border);border-radius:999px;height:6px;overflow:hidden;}
.prog-fill{height:6px;border-radius:999px;transition:width .4s ease;}
/* ── Section heading ── */
.section-heading{font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--text3);padding-bottom:8px;border-bottom:1px solid var(--border);margin-bottom:14px;}
/* ── Table ── */
table{width:100%;border-collapse:collapse;font-size:13px;}
th{background:var(--surface2);color:var(--text3);font-size:10px;letter-spacing:1px;text-transform:uppercase;padding:7px 12px;text-align:left;border-bottom:1px solid var(--border);font-weight:700;}
td{padding:8px 12px;border-bottom:1px solid var(--border);color:var(--text);}
tr:last-child td{border-bottom:none;}
tr:hover td{background:var(--surface2);}
/* ── Inputs ── */
[data-baseweb="input"] input,[data-baseweb="select"] div,textarea{
    background:var(--surface)!important;border-color:var(--border)!important;
    color:var(--text)!important;border-radius:8px!important;
    font-family:'Noto Sans TC',sans-serif!important;
}
/* ── Buttons ── */
.stButton>button{
    background:var(--accent)!important;color:#fff!important;border:none!important;
    border-radius:8px!important;font-weight:600!important;font-size:13px!important;
    font-family:'Noto Sans TC',sans-serif!important;
}
.stButton>button:hover{opacity:.85!important;}
/* ── page_link styling ── */
[data-testid="stPageLink"]{border-radius:8px!important;width:100%!important;}
[data-testid="stPageLink"] p{
    font-size:13px!important;font-weight:500!important;
    color:#57534e!important;padding:7px 10px!important;margin:0!important;
}
[data-testid="stPageLink"]:hover p{color:#1c1917!important;}
/* ── Hide chrome ── */
#MainMenu,footer,header{visibility:hidden!important;}
[data-testid="stDecoration"]{display:none!important;}
/* ── 縮小頂部 padding ── */
[data-testid="stHeader"]{display:none!important;}
</style>"""

st.markdown(COMMON_CSS, unsafe_allow_html=True)
st.session_state["COMMON_CSS"] = COMMON_CSS

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
    """, unsafe_allow_html=True)

    notion_ok = bool(os.getenv("NOTION_TOKEN") and os.getenv("NOTION_DB_ID"))
    if notion_ok:
        st.markdown("""<div style='margin:0 8px 8px;background:#dcfce7;border:1px solid #86efac;
            border-radius:8px;padding:6px 10px;display:flex;align-items:center;gap:6px'>
          <div style='width:6px;height:6px;border-radius:50%;background:#16a34a;flex-shrink:0'></div>
          <span style='font-size:11px;color:#15803d;font-weight:600'>已連接 Notion</span>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div style='margin:0 8px 8px;background:#fef3c7;border:1px solid #fcd34d;
            border-radius:8px;padding:6px 10px;display:flex;align-items:center;gap:6px'>
          <div style='width:6px;height:6px;border-radius:50%;background:#d97706;flex-shrink:0'></div>
          <span style='font-size:11px;color:#92400e;font-weight:600'>未連接 Notion</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    st.markdown("<div style='padding:0 8px;font-size:9px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#a8a29e;margin-bottom:4px'>導覽</div>", unsafe_allow_html=True)

    st.page_link("app.py",                label="🏠  首頁")
    st.page_link("pages/1_dashboard.py",  label="📊  畢業進度儀表板")
    st.page_link("pages/2_courses.py",    label="📋  修課明細查詢")
    st.page_link("pages/3_ai_advisor.py", label="🤖  AI 選課顧問")
    st.page_link("pages/4_simulate.py",   label="🔮  模擬選課規劃")

    st.markdown("""
    <div style='padding:12px 12px 0;margin-top:8px;border-top:1px solid #e2e0d9'>
      <div style='font-size:11px;color:#a8a29e;line-height:1.9'>
        📘 課程地圖：114 入學<br>
        🏫 長庚大學 資管系<br>
        🔧 Powered by Notion API
      </div>
    </div>""", unsafe_allow_html=True)

# ── 首頁 ─────────────────────────────────────────────────────
st.markdown("""
<div style='padding:16px 0 24px'>
  <div style='font-size:10px;letter-spacing:2.5px;color:#2563eb;font-weight:700;
              text-transform:uppercase;margin-bottom:8px'>長庚大學 資訊管理學系</div>
  <h1 style='font-size:34px;font-weight:900;letter-spacing:-0.8px;color:#1c1917;
             margin:0 0 10px;line-height:1.15'>畢業初審系統</h1>
  <p style='color:#78716c;font-size:14px;max-width:520px;line-height:1.7;margin:0'>
    自動從 Notion 讀取修課紀錄，即時比對 114 入學畢業門檻，並提供 AI 個人化選課建議。
  </p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.1], gap="large")

with col1:
    st.markdown("<div class='section-heading'>快速開始</div>", unsafe_allow_html=True)
    for color, num, title, desc in [
        ("#2563eb","1","建立 .env 檔","在專案根目錄建立 .env，填入 NOTION_TOKEN 與 NOTION_DB_ID"),
        ("#7c3aed","2","連接 Notion","在「個人修課紀錄」Database 頁面，連接你的 Integration"),
        ("#16a34a","3","開始審核","點左側「📊 畢業進度儀表板」，系統自動讀取並分析修課資料"),
    ]:
        st.markdown(f"""
        <div style='display:flex;gap:12px;align-items:flex-start;padding:12px 14px;
             border:1px solid #e2e0d9;border-radius:10px;margin-bottom:8px;background:#fff'>
          <div style='width:24px;height:24px;border-radius:50%;background:{color};
               display:flex;align-items:center;justify-content:center;
               flex-shrink:0;font-size:11px;font-weight:700;color:#fff'>{num}</div>
          <div>
            <div style='font-weight:700;font-size:13px;color:#1c1917;margin-bottom:2px'>{title}</div>
            <div style='font-size:12px;color:#78716c;line-height:1.6'>{desc}</div>
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div class='section-heading' style='margin-top:16px'>.env 設定</div>", unsafe_allow_html=True)
    st.code("NOTION_TOKEN=secret_xxxxxxxxxxxxxxxx\nNOTION_DB_ID=xxxxxxxxxxxxxxxxxxxxxxxx", language="bash")

with col2:
    st.markdown("<div class='section-heading'>系統功能</div>", unsafe_allow_html=True)
    for icon, color, title, desc in [
        ("📊","#2563eb","畢業進度儀表板","KPI 卡片、學分圓餅圖、各領域達成率，缺修課程即時標示"),
        ("📋","#7c3aed","修課明細查詢","完整列表，依完成／修習中／未修分類，支援關鍵字篩選"),
        ("🤖","#16a34a","AI 選課顧問","根據缺修狀況與興趣方向，AI 給出個人化選課建議"),
        ("🔮","#ea580c","模擬選課規劃","勾選預計修課，即時預覽加入後的畢業達成進度"),
    ]:
        st.markdown(f"""
        <div style='display:flex;gap:10px;align-items:flex-start;padding:12px 14px;
             border:1px solid #e2e0d9;border-radius:10px;margin-bottom:8px;background:#fff'>
          <div style='font-size:18px;line-height:1;margin-top:1px'>{icon}</div>
          <div>
            <div style='font-weight:700;font-size:13px;color:{color};margin-bottom:2px'>{title}</div>
            <div style='font-size:12px;color:#78716c;line-height:1.6'>{desc}</div>
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div class='section-heading' style='margin-top:12px'>Notion DB 必要欄位</div>", unsafe_allow_html=True)
    for name, ftype, color in [
        ("課程名稱","Title","#2563eb"),
        ("學分","Number 或 Rollup","#7c3aed"),
        ("成績","Number（P/F 留空）","#16a34a"),
        ("修課狀態","Status：完成 / 修習中 / 未修","#ea580c"),
    ]:
        st.markdown(f"""
        <div style='display:flex;justify-content:space-between;align-items:center;
             padding:6px 0;border-bottom:1px solid #e2e0d9'>
          <span style='font-size:13px;color:#1c1917;font-weight:500'>{name}</span>
          <span style='font-size:10px;color:{color};background:{color}18;
                border-radius:999px;padding:2px 8px;border:1px solid {color}40'>{ftype}</span>
        </div>""", unsafe_allow_html=True)
