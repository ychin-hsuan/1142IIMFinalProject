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

COMMON_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700;900&family=Space+Mono:wght@400;700&display=swap');
:root{--bg:#0d0f14;--surface:#151820;--surface2:#1c2030;--border:#2a2f42;
     --accent:#4f8ef7;--accent2:#7c5cfc;--green:#2ecc8a;--red:#ff4d6d;
     --yellow:#f5c518;--text:#e8ecf4;--muted:#7a8099;--radius:12px;}
html,body,[data-testid="stAppViewContainer"]{background:var(--bg)!important;color:var(--text)!important;font-family:'Noto Sans TC',sans-serif!important;}
[data-testid="stSidebar"]{background:var(--surface)!important;border-right:1px solid var(--border)!important;}
[data-testid="stSidebar"] *{color:var(--text)!important;}
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:20px 24px;margin-bottom:16px;transition:border-color .2s,transform .15s;}
.card:hover{border-color:#3d4560;transform:translateY(-1px);}
.card-title{font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--muted);margin-bottom:6px;}
.card-value{font-family:'Space Mono',monospace;font-size:34px;font-weight:700;line-height:1;}
.badge{display:inline-block;padding:3px 10px;border-radius:999px;font-size:11px;font-weight:700;}
.badge-pass{background:#0e3d2a;color:#2ecc8a;border:1px solid #2ecc8a;}
.badge-fail{background:#3d0e1a;color:#ff4d6d;border:1px solid #ff4d6d;}
.badge-warn{background:#3d3000;color:#f5c518;border:1px solid #f5c518;}
.badge-info{background:#0e2040;color:#4f8ef7;border:1px solid #4f8ef7;}
.badge-prog{background:#1a2040;color:#7c5cfc;border:1px solid #7c5cfc;}
.prog-wrap{background:#2a2f42;border-radius:999px;height:8px;overflow:hidden;}
.prog-fill{height:8px;border-radius:999px;}
.section-heading{font-size:11px;font-weight:800;letter-spacing:3px;text-transform:uppercase;color:#7a8099;padding:6px 0 12px;border-bottom:1px solid #2a2f42;margin-bottom:20px;}
table{width:100%;border-collapse:collapse;font-size:14px;}
th{background:#1c2030;color:#7a8099;font-size:11px;letter-spacing:1.5px;text-transform:uppercase;padding:10px 14px;text-align:left;border-bottom:1px solid #2a2f42;}
td{padding:10px 14px;border-bottom:1px solid #2a2f42;color:#e8ecf4;}
tr:hover td{background:#1c2030;}
[data-baseweb="input"] input,[data-baseweb="select"] div,textarea{background:#1c2030!important;border-color:#2a2f42!important;color:#e8ecf4!important;border-radius:8px!important;}
.stButton>button{background:linear-gradient(135deg,#4f8ef7,#7c5cfc)!important;color:#fff!important;border:none!important;border-radius:8px!important;font-weight:700!important;}
#MainMenu,footer{visibility:hidden;}
[data-testid="stDecoration"]{display:none;}
</style>
"""
st.markdown(COMMON_CSS, unsafe_allow_html=True)

# 存到 session_state 讓各頁面取用
st.session_state["COMMON_CSS"] = COMMON_CSS

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:16px 0 20px'>
      <div style='font-family:Space Mono,monospace;font-size:10px;letter-spacing:3px;
                  color:#4f8ef7;font-weight:700;text-transform:uppercase;margin-bottom:4px'>CGU · IMIS</div>
      <div style='font-size:20px;font-weight:900;color:#e8ecf4'>畢業初審系統</div>
      <div style='font-size:12px;color:#7a8099;margin-top:2px'>Graduation Audit System</div>
    </div>
    <hr style='border-color:#2a2f42;margin-bottom:16px'>
    """, unsafe_allow_html=True)

    notion_ok = bool(os.getenv("NOTION_TOKEN") and os.getenv("NOTION_DB_ID"))
    if notion_ok:
        st.markdown("""<div style='background:#0e3d2a;border:1px solid #2ecc8a;border-radius:8px;
            padding:10px 14px;margin-bottom:16px;font-size:13px;color:#2ecc8a'>
            ✓ 已連接 Notion</div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div style='background:#3d2200;border:1px solid #f5c518;border-radius:8px;
            padding:10px 14px;margin-bottom:16px;font-size:13px;color:#f5c518'>
            ⚠ 未設定 Notion（請建立 .env）</div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class='section-heading'>導覽</div>
    <div style='display:flex;flex-direction:column;gap:4px'>
      <a href='/' target='_self' style='display:block;padding:9px 14px;border-radius:8px;
         color:#e8ecf4;text-decoration:none;font-size:14px'>🏠&nbsp; 首頁</a>
      <a href='/1_dashboard' target='_self' style='display:block;padding:9px 14px;border-radius:8px;
         color:#e8ecf4;text-decoration:none;font-size:14px'>📊&nbsp; 畢業進度儀表板</a>
      <a href='/2_courses' target='_self' style='display:block;padding:9px 14px;border-radius:8px;
         color:#e8ecf4;text-decoration:none;font-size:14px'>📋&nbsp; 修課明細查詢</a>
      <a href='/3_ai_advisor' target='_self' style='display:block;padding:9px 14px;border-radius:8px;
         color:#e8ecf4;text-decoration:none;font-size:14px'>🤖&nbsp; AI 選課顧問</a>
      <a href='/4_simulate' target='_self' style='display:block;padding:9px 14px;border-radius:8px;
         color:#e8ecf4;text-decoration:none;font-size:14px'>🔮&nbsp; 模擬選課規劃</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='section-heading' style='margin-top:24px'>系統資訊</div>
    <div style='font-size:12px;color:#7a8099;line-height:2'>
      📘 課程地圖：114 入學<br>
      🏫 長庚大學 資管系<br>
      🔧 Powered by Notion API
    </div>
    """, unsafe_allow_html=True)

# ── 首頁 ─────────────────────────────────────────────────────
st.markdown("""
<div style='padding:48px 0 32px'>
  <div style='font-size:11px;letter-spacing:4px;color:#4f8ef7;font-weight:700;
              text-transform:uppercase;margin-bottom:12px'>長庚大學 資訊管理學系</div>
  <h1 style='font-size:48px;font-weight:900;letter-spacing:-1px;
             background:linear-gradient(135deg,#4f8ef7,#7c5cfc);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:0 0 12px'>
    畢業初審系統
  </h1>
  <p style='color:#7a8099;font-size:16px;max-width:520px;line-height:1.7'>
    自動從 Notion 讀取修課紀錄，比對 114 入學畢業門檻，<br>
    即時顯示學分達成狀況與 AI 選課建議。
  </p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("<div class='section-heading'>快速開始</div>", unsafe_allow_html=True)
    steps = [
        ("1", "#4f8ef7", "建立 .env 檔",
         "在專案根目錄建立 <code>.env</code>，填入 NOTION_TOKEN 與 NOTION_DB_ID"),
        ("2", "#7c5cfc", "設定 Notion 權限",
         "在你的修課紀錄 Database 頁面，連接你建立的 Integration"),
        ("3", "#2ecc8a", "點選儀表板",
         "左側點「📊 畢業進度儀表板」，系統自動讀取並分析你的修課資料"),
    ]
    for num, color, title, desc in steps:
        st.markdown(f"""
        <div class='card' style='display:flex;gap:16px;align-items:flex-start;padding:16px 20px'>
          <div style='width:32px;height:32px;border-radius:50%;background:{color};
               display:flex;align-items:center;justify-content:center;
               font-weight:900;font-size:15px;flex-shrink:0'>{num}</div>
          <div>
            <div style='font-weight:700;font-size:15px;margin-bottom:4px'>{title}</div>
            <div style='font-size:13px;color:#7a8099;line-height:1.6'>{desc}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("<div class='section-heading'>功能介紹</div>", unsafe_allow_html=True)
    features = [
        ("📊", "#4f8ef7", "畢業進度儀表板",
         "KPI 卡片 + 各類學分達成率，缺修紅字即時標示，指修規定自動警示"),
        ("📋", "#7c5cfc", "修課明細查詢",
         "完整課程列表，區分完成／修習中／未修，支援關鍵字與領域篩選"),
        ("🤖", "#2ecc8a", "AI 選課顧問",
         "根據缺修狀況與興趣方向，由 AI 給出個人化選課建議"),
        ("🔮", "#f5c518", "模擬選課規劃",
         "勾選預計修課，即時預覽加入後的畢業達成狀況"),
    ]
    for icon, color, title, desc in features:
        st.markdown(f"""
        <div class='card' style='display:flex;gap:14px;align-items:flex-start;padding:14px 18px'>
          <div style='font-size:24px;line-height:1.2'>{icon}</div>
          <div>
            <div style='font-weight:700;font-size:14px;color:{color};margin-bottom:3px'>{title}</div>
            <div style='font-size:13px;color:#7a8099;line-height:1.6'>{desc}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

# .env 範本
st.markdown("<div class='section-heading' style='margin-top:8px'>.env 設定範本</div>",
            unsafe_allow_html=True)
st.code("""# .env  （放在 graduation_system/ 資料夾內）
NOTION_TOKEN=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_DB_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx""", language="bash")

st.markdown("""
<div style='background:#0e2040;border:1px solid #2a3f6f;border-radius:12px;
            padding:16px 20px;margin-top:4px;font-size:13px;color:#a0b4d0;line-height:1.8'>
  <b style='color:#4f8ef7'>📌 Notion DB 必要欄位</b><br>
  <code>課程名稱</code>（Title）&nbsp;·&nbsp;
  <code>學分</code>（Number）&nbsp;·&nbsp;
  <code>成績</code>（Number，P/F 課程留空）&nbsp;·&nbsp;
  <code>修課狀態</code>（Status：完成 / 修習中 / 未修）
</div>
""", unsafe_allow_html=True)
