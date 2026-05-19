import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()

# ── 處理 CTA 按鈕導航 ──────────────────────────────────────
import urllib.parse as _up

st.set_page_config(
    page_title="畢業初審系統 | 長庚大學資管系",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

COMMON_CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&family=DM+Mono:wght@400;500&display=swap');
* { box-sizing: border-box; }
html, body {
    margin: 0 !important;
    padding: 0 !important;
    background: #1a1614 !important;
}
[data-testid="stApp"],
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
[data-testid="stVerticalBlock"],
[data-testid="stVerticalBlockBorderWrapper"],
section[data-testid="stMain"],
.main, .stMain {
    padding: 0 !important;
    margin: 0 !important;
    background: #1a1614 !important;
    gap: 0 !important;
}
.block-container, .main .block-container {
    padding: 0 !important;
    margin: 0 !important;
    max-width: 100% !important;
    background: #1a1614 !important;
}
iframe {
    display: block !important;
    border: none !important;
    margin: 0 !important;
    padding: 0 !important;
    width: 100% !important;
}
:root {
    --bg:#f5f4f1; --surface:#ffffff; --surface2:#f0efe9; --border:#e2e0d9;
    --accent:#2563eb; --green:#16a34a; --red:#dc2626; --yellow:#d97706;
    --purple:#7c3aed; --orange:#ea580c;
    --text:#1c1917; --text2:#b6b6b6; --text3:#b6b6b6; --radius:10px;
}
html,body,[data-testid="stAppViewContainer"],[data-testid="stAppViewBlockContainer"]{
    background:#1a1614!important; color:#f5f4f1!important;
    font-family:'Noto Sans TC',sans-serif!important;
    padding:0!important; margin:0!important;
}
section.main, [data-testid="stAppViewContainer"] > section {
    padding:0!important; margin:0!important;
}
[data-testid="stSidebar"]{
    background:#1a1614!important;
    border-right:1px solid #2d2926!important;
    min-width:220px!important; max-width:220px!important; width:220px!important;
}
[data-testid="stSidebar"][aria-expanded="false"]{
    min-width:220px!important; max-width:220px!important;
    transform:none!important; margin-left:0!important;
}
[data-testid="stSidebar"] * { color:#f5f4f1!important; }
[data-testid="stSidebar"] [data-testid="stVerticalBlock"]{gap:2px!important;}
[data-testid="stSidebarNav"]{display:none!important;}
[data-testid="collapsedControl"]{display:none!important;}
button[kind="header"]{display:none!important;}
[data-testid="stPageLink"] p{
    font-size:13px!important; font-weight:500!important;
    color:#b6b6b6!important; padding:8px 10px!important; margin:0!important;
}
[data-testid="stPageLink"]:hover p{ color:#f5f4f1!important; }
[data-testid="stPageLink"]{ border-radius:8px!important; width:100%!important; }
.main .block-container{padding:0!important;max-width:100%!important;margin:0!important;}
[data-testid="stAppViewContainer"] > .main{padding:0!important;}
iframe{display:block!important;}
#MainMenu,footer,header{visibility:hidden!important;}
[data-testid="stDecoration"]{display:none!important;}
[data-testid="stHeader"]{display:none!important;}
.badge{display:inline-flex;align-items:center;padding:2px 8px;border-radius:999px;font-size:11px;font-weight:600;}
.badge-pass{background:#dcfce7;color:#16a34a;border:1px solid #86efac;}
.badge-fail{background:#fee2e2;color:#dc2626;border:1px solid #fca5a5;}
.badge-warn{background:#fef3c7;color:#d97706;border:1px solid #fcd34d;}
.badge-info{background:#dbeafe;color:#2563eb;border:1px solid #93c5fd;}
.badge-prog{background:#ede9fe;color:#7c3aed;border:1px solid #c4b5fd;}
.prog-wrap{background:#e2e0d9;border-radius:999px;height:6px;overflow:hidden;}
.prog-fill{height:6px;border-radius:999px;transition:width .4s ease;}
.section-heading{font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#b6b6b6;padding-bottom:8px;border-bottom:1px solid #e2e0d9;margin-bottom:14px;}
.card{background:#ffffff;border:1px solid #e2e0d9;border-radius:10px;padding:16px 18px;margin-bottom:10px;}
.card-label{font-size:10px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#b6b6b6;margin-bottom:5px;}
.card-value{font-family:'DM Mono',monospace;font-size:26px;font-weight:500;line-height:1;}
table{width:100%;border-collapse:collapse;font-size:13px;}
th{background:#f0efe9;color:#b6b6b6;font-size:10px;letter-spacing:1px;text-transform:uppercase;padding:7px 12px;text-align:left;border-bottom:1px solid #e2e0d9;font-weight:700;}
td{padding:8px 12px;border-bottom:1px solid #e2e0d9;color:#1c1917;}
tr:last-child td{border-bottom:none;}
tr:hover td{background:#f0efe9;}
[data-baseweb="input"] input,[data-baseweb="select"] div,textarea{background:#ffffff!important;border-color:#e2e0d9!important;color:#1c1917!important;border-radius:8px!important;font-family:'Noto Sans TC',sans-serif!important;}
.stButton>button{background:#2563eb!important;color:#fff!important;border:none!important;border-radius:8px!important;font-weight:600!important;font-size:13px!important;font-family:'Noto Sans TC',sans-serif!important;}
.stButton>button:hover{opacity:.85!important;}
[data-testid="stPageLink"]{border-radius:8px!important;width:100%!important;margin-bottom:2px!important;}
[data-testid="stPageLink"] p{font-size:13px!important;font-weight:500!important;color:#b6b6b6!important;padding:8px 12px!important;margin:0!important;}
[data-testid="stPageLink"]:hover p{color:#f5f4f1!important;}
[data-baseweb="tag"]{background:#dbeafe!important;border:1px solid #93c5fd!important;border-radius:6px!important;padding:2px 8px!important;margin:2px!important;}
[data-baseweb="tag"] span[title]{color:#1e40af!important;font-size:13px!important;font-weight:500!important;}
</style>"""

st.markdown(COMMON_CSS, unsafe_allow_html=True)
st.session_state["COMMON_CSS"] = COMMON_CSS

# ── Query param 導航處理 ─────────────────────────────────────
_page_map = {
    "dashboard":  "pages/1_dashboard.py",
    "courses":    "pages/2_courses.py",
    "ai_advisor": "pages/3_ai_advisor.py",
    "simulate":   "pages/4_simulate.py",
}
_nav = st.query_params.get("nav", "")
if _nav in _page_map:
    st.switch_page(_page_map[_nav])

notion_ok = bool(os.getenv("NOTION_TOKEN") and os.getenv("NOTION_DB_ID"))
notion_status = "已連接 Notion" if notion_ok else "未連接 Notion"
notion_color  = "#22c55e" if notion_ok else "#f97316"

# ── Streamlit Sidebar（原生，可正常導航）──────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:20px 12px 14px'>
      <div style='font-size:9px;letter-spacing:2px;color:#b6b6b6;
                  font-weight:700;text-transform:uppercase;margin-bottom:4px'>
        CGU · IMIS · 114
      </div>
      <div style='font-size:15px;font-weight:900;color:#f5f4f1;letter-spacing:-0.3px'>
        畢業初審系統
      </div>
    </div>
    """, unsafe_allow_html=True)

    if notion_ok:
        st.markdown("""<div style='margin:0 0 20px;background:#14532d33;border:1px solid #22c55e44;
            border-radius:8px;padding:7px 12px;display:flex;align-items:center;gap:7px'>
          <div style='width:6px;height:6px;border-radius:50%;background:#22c55e;flex-shrink:0'></div>
          <span style='font-size:11px;color:#86efac;font-weight:600;font-family:monospace'>已連接 Notion</span>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div style='margin:0 0 20px;background:#78350f33;border:1px solid #f9731644;
            border-radius:8px;padding:7px 12px;display:flex;align-items:center;gap:7px'>
          <div style='width:6px;height:6px;border-radius:50%;background:#f97316;flex-shrink:0'></div>
          <span style='font-size:11px;color:#fdba74;font-weight:600;font-family:monospace'>未連接 Notion</span>
        </div>""", unsafe_allow_html=True)


    st.page_link("app.py",                label="首頁")
    st.page_link("pages/1_dashboard.py",  label="畢業進度儀表板")
    st.page_link("pages/2_courses.py",    label="修課明細查詢")
    st.page_link("pages/3_ai_advisor.py", label="AI 選課顧問")
    st.page_link("pages/4_simulate.py",   label="模擬選課規劃")
    st.markdown("""<div style='padding:14px 12px 0;margin-top:8px;border-top:1px solid #2d2926'>
      <div style='font-size:11px;color:#b6b6b6;line-height:1.9;font-family:monospace'>
        📘 114 入學<br>🏫 長庚大學 資管系<br>🔧 Notion API
      </div></div>""", unsafe_allow_html=True)

st.components.v1.html(f"""
<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
:root{{
  --dark:#1a1614;
  --dark2:#211e1b;
  --dark3:#2a2522;
  --border:#2d2926;
  --border2:#b6b6b6;
  --text:#f5f4f1;
  --muted:#b6b6b6;
  --muted2:#b6b6b6;
  --muted3:#b6b6b6;
  --blue:#2563eb;
  --green:#22c55e;
  --yellow:#eab308;
}}
body{{
  font-family:'Noto Sans TC',sans-serif;
  background:var(--dark);
  color:var(--text);
  height:950px;
  display:flex;
  flex-direction:column;
  overflow:hidden;
  margin:0;
  padding:0;
  width:100%;
}}

/* ── Sidebar ── */
.sidebar{{
  width:220px;
  min-width:220px;
  background:var(--dark2);
  border-right:1px solid var(--border);
  display:flex;
  flex-direction:column;
  height:950px;
  overflow-y:auto;
}}
.sidebar-logo{{
  padding:24px 20px 16px;
  border-bottom:1px solid var(--border);
}}
.sidebar-logo .eyebrow{{
  font-family:'DM Mono',monospace;
  font-size:9px;
  letter-spacing:2px;
  color:#b6b6b6;
  text-transform:uppercase;
  margin-bottom:4px;
}}
.sidebar-logo .title{{
  font-size:15px;
  font-weight:900;
  color:var(--text);
  letter-spacing:-0.3px;
}}
.notion-pill{{
  margin:12px 16px;
  background:var(--dark3);
  border:1px solid var(--border2);
  border-radius:8px;
  padding:7px 12px;
  display:flex;
  align-items:center;
  gap:7px;
  font-size:11px;
  color:#b6b6b6;
  font-family:'DM Mono',monospace;
}}
.notion-dot{{
  width:6px;height:6px;border-radius:50%;flex-shrink:0;
  background:{notion_color};
  box-shadow:0 0 6px {notion_color}88;
}}
.nav-section{{
  padding:8px 12px 4px;
  font-size:9px;
  letter-spacing:2px;
  text-transform:uppercase;
  color:#b6b6b6;
  font-family:'DM Mono',monospace;
  font-weight:700;
}}
.nav-link{{
  display:flex;
  align-items:center;
  gap:10px;
  padding:9px 16px;
  margin:1px 8px;
  border-radius:8px;
  text-decoration:none;
  color:#b6b6b6;
  font-size:13px;
  font-weight:500;
  transition:all .15s;
  cursor:pointer;
}}
.nav-link:hover{{
  background:var(--dark3);
  color:var(--text);
}}
.nav-link.active{{
  background:var(--dark3);
  color:var(--text);
  border-left:2px solid var(--blue);
  padding-left:14px;
}}
.nav-icon{{font-size:15px;width:20px;text-align:center;}}
.sidebar-footer{{
  margin-top:auto;
  padding:16px 20px;
  border-top:1px solid var(--border);
  font-size:11px;
  color:#b6b6b6;
  line-height:1.9;
  font-family:'DM Mono',monospace;
}}

/* ── Main ── */
.main{{
  width:100%;
  display:flex;
  flex-direction:column;
  overflow:hidden;
}}

/* 頂部 bar */
.topbar{{
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:0 40px;
  height:56px;
  border-bottom:1px solid var(--border);
  flex-shrink:0;
}}
.topbar-left{{
  font-family:'DM Mono',monospace;
  font-size:11px;
  color:#b6b6b6;
  letter-spacing:1px;
}}
.topbar-tags{{display:flex;gap:6px;}}
.tag-pill{{
  display:inline-flex;align-items:center;gap:6px;
  background:var(--dark3);border:1px solid var(--border2);
  border-radius:999px;padding:4px 12px;
  font-size:11px;color:#b6b6b6;
  font-family:'DM Mono',monospace;
  font-weight:500;
}}
.tag-dot{{width:5px;height:5px;border-radius:50%;}}

/* Hero 主區 */
.hero{{
  flex:1;
  min-height:0;
  display:grid;
  grid-template-columns:1fr 240px;
  overflow:hidden;
  width:100%;
}}
.hero-left{{
  padding:40px 48px;
  display:flex;
  flex-direction:column;
  justify-content:space-between;
  border-right:1px solid var(--border);
}}
.big-text{{
  position:relative;
  line-height:0.87;
  letter-spacing:-4px;
}}
.big-text .l1{{
  font-size:clamp(72px,9vw,128px);
  font-weight:900;
  color:var(--text);
  display:block;
  position:relative;
  z-index:2;
}}
.big-text .l2{{
  font-size:clamp(72px,9vw,128px);
  font-weight:900;
  color:var(--blue);
  display:block;
  position:relative;
  z-index:2;
}}
.big-text .l3{{
  font-size:clamp(72px,9vw,128px);
  font-weight:900;
  font-family:'DM Mono',monospace;
  color:transparent;
  -webkit-text-stroke:1.5px #b6b6b6;
  display:block;
  letter-spacing:-4px;
  position:absolute;
  bottom:-90px;
  left:0;
  z-index:1;
  opacity:0.2;
  white-space:nowrap;
  -webkit-text-stroke:1px #b6b6b6;
}}
.hero-bottom{{}}
.hero-desc{{
  font-size:14px;color:#b6b6b6;line-height:1.8;
  max-width:440px;margin-bottom:28px;
}}
.cta-row{{display:flex;align-items:center;gap:10px;flex-wrap:wrap;}}
.cta-btn{{
  display:inline-flex;align-items:center;gap:8px;
  background:var(--blue);color:#fff;
  border:none;border-radius:999px;padding:13px 28px;
  font-size:14px;font-weight:700;
  font-family:'Noto Sans TC',sans-serif;
  text-decoration:none;cursor:pointer;
  transition:all .2s;
}}
.cta-btn:hover{{background:#1d4ed8;transform:translateY(-1px);}}
.cta-sec{{
  display:inline-flex;align-items:center;gap:8px;
  background:transparent;color:#b6b6b6;
  border:1px solid var(--border2);border-radius:999px;
  padding:12px 24px;font-size:13px;font-weight:500;
  font-family:'Noto Sans TC',sans-serif;
  text-decoration:none;cursor:pointer;transition:all .2s;
}}
.cta-sec:hover{{border-color:#b6b6b6;color:var(--text);}}

/* 右側 stats */
.hero-right{{
  padding:28px 20px;
  display:flex;flex-direction:column;gap:14px;
  overflow-y:auto;
}}
.stat-card{{
  background:var(--dark3);
  border:1px solid var(--border2);
  border-radius:12px;
  padding:16px 18px;
}}
.stat-num{{
  font-family:'DM Mono',monospace;
  font-size:38px;font-weight:500;
  color:var(--text);line-height:1;
  margin-bottom:4px;
}}
.stat-label{{
  font-size:10px;letter-spacing:1.5px;
  text-transform:uppercase;color:#b6b6b6;
  font-family:'DM Mono',monospace;
}}
.stat-card.blue .stat-num{{color:var(--blue);}}
.stat-card.green .stat-num{{color:#7c3aed;}}
.stat-card.yellow .stat-num{{color:#d97706;}}
.setup-box{{
  margin-top:auto;
  padding-top:14px;
  border-top:1px solid #2d2926;
}}
.setup-title{{
  font-size:9px;letter-spacing:2px;text-transform:uppercase;
  color:#b6b6b6;font-family:'DM Mono',monospace;
  margin-bottom:8px;
}}
.setup-code{{
  font-family:'DM Mono',monospace;
  font-size:11px;color:#b6b6b6;line-height:2;
}}

/* 底部跑馬燈 */
.ticker{{
  height:36px;
  border-top:1px solid var(--border);
  overflow:hidden;white-space:nowrap;
  display:flex;align-items:center;
  flex-shrink:0;
}}
.ticker-inner{{
  display:inline-block;
  animation:scroll 20s linear infinite;
}}
@keyframes scroll{{
  0%{{transform:translateX(0);}}
  100%{{transform:translateX(-50%);}}
}}
.ticker-item{{
  font-family:'DM Mono',monospace;
  font-size:11px;letter-spacing:2.5px;
  text-transform:uppercase;color:#b6b6b6;
  margin:0 32px;
}}
.ticker-sep{{color:var(--blue);margin:0 12px;}}
</style>
</head>
<body>



<div class="main">
  <div class="topbar">
    <div class="topbar-left">GRADUATION AUDIT SYSTEM</div>
    <div class="topbar-tags">
      <span class="tag-pill"><span class="tag-dot" style="background:#2563eb"></span>Notion API</span>
      <span class="tag-pill"><span class="tag-dot" style="background:#22c55e"></span>AI 建議</span>
      <span class="tag-pill"><span class="tag-dot" style="background:#7c3aed"></span>模擬選課</span>
    </div>
    <div style="font-family:'DM Mono',monospace;font-size:10px;color:#b6b6b6">114 入學適用</div>
  </div>

  <div class="hero">
    <div class="hero-left">
      <div class="big-text">
        <span class="l1">畢業</span>
        <span class="l2">初審</span>
        <span class="l3">SYSTEM</span>
      </div>

      <div class="hero-bottom">
        <p class="hero-desc">
          自動從 Notion 讀取修課紀錄，即時比對 114 入學畢業門檻，<br>
          AI 分析缺修狀況並給出個人化選課建議。
        </p>
      </div>
    </div>

    <div class="hero-right">
      <div class="stat-card blue">
        <div class="stat-num">48</div>
        <div class="stat-label">系訂必修學分</div>
      </div>
      <div class="stat-card">
        <div class="stat-num">12</div>
        <div class="stat-label">管院共構必修</div>
      </div>
      <div class="stat-card green">
        <div class="stat-num">42</div>
        <div class="stat-label">系選修門檻</div>
      </div>
      <div class="stat-card yellow">
        <div class="stat-num">128</div>
        <div class="stat-label">畢業總學分</div>
      </div>

      <div class="setup-box">
        <div class="setup-title">快速設定</div>
        <div class="setup-code">
          NOTION_TOKEN=secret_…<br>
          NOTION_DB_ID=32位ID
        </div>
      </div>
    </div>
  </div>

  <div class="ticker">
    <div class="ticker-inner">
      <span class="ticker-item">畢業資格審查</span><span class="ticker-sep">·</span>
      <span class="ticker-item">Notion API</span><span class="ticker-sep">·</span>
      <span class="ticker-item">AI 選課建議</span><span class="ticker-sep">·</span>
      <span class="ticker-item">114 入學適用</span><span class="ticker-sep">·</span>
      <span class="ticker-item">長庚大學 資管系</span><span class="ticker-sep">·</span>
      <span class="ticker-item">模擬選課規劃</span><span class="ticker-sep">·</span>
      <span class="ticker-item">畢業資格審查</span><span class="ticker-sep">·</span>
      <span class="ticker-item">Notion API</span><span class="ticker-sep">·</span>
      <span class="ticker-item">AI 選課建議</span><span class="ticker-sep">·</span>
      <span class="ticker-item">114 入學適用</span><span class="ticker-sep">·</span>
      <span class="ticker-item">長庚大學 資管系</span><span class="ticker-sep">·</span>
      <span class="ticker-item">模擬選課規劃</span><span class="ticker-sep">·</span>
    </div>
  </div>
</div>

<script>
function navigate(path) {{
  // Send message to Streamlit parent
  window.parent.postMessage({{
    isStreamlitMessage: true,
    type: "navigate",
    path: path
  }}, "*");
}}
document.querySelectorAll('[onclick]').forEach(el => {{
  el.style.cursor = 'pointer';
}});
</script>
</body>
</html>
""", height=820, scrolling=False)
