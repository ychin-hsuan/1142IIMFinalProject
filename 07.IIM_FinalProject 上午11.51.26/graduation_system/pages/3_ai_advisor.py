import streamlit as st
import sys, os, requests as req_lib
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from dotenv import load_dotenv
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(_root, ".env"), override=True)
import utils.data as _data
_data.NOTION_TOKEN = os.getenv("NOTION_TOKEN", "")
_data.NOTION_DB_ID = os.getenv("NOTION_DB_ID", "")

from utils.data import get_student_taken, fetch_inprogress_courses, compute_status

st.set_page_config(page_title="AI 選課顧問", page_icon="🤖", layout="wide")

st.markdown("""<style>
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
[data-testid="stSidebar"]{
    background:var(--surface)!important;
    border-right:1px solid var(--border)!important;
    min-width:220px!important; max-width:220px!important; width:220px!important;
}
[data-testid="stSidebar"][aria-expanded="false"]{
    min-width:220px!important; max-width:220px!important;
    transform:none!important; margin-left:0!important;
}
button[kind="header"],[data-testid="collapsedControl"]{display:none!important;}
[data-testid="stSidebar"] *{color:var(--text)!important;}
[data-testid="stSidebarNav"]{display:none!important;}
[data-testid="stAppViewContainer"] > .main{padding-left:0!important;}
.main .block-container{padding:1.5rem 2rem 2rem!important; max-width:100%!important;}
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:16px 18px;margin-bottom:10px;}
.card-label{font-size:10px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:var(--text3);margin-bottom:5px;}
.card-value{font-family:'DM Mono',monospace;font-size:26px;font-weight:500;line-height:1;}
.card-sub{font-size:11px;color:var(--text3);margin-top:5px;}
.badge{display:inline-flex;align-items:center;padding:2px 8px;border-radius:999px;font-size:11px;font-weight:600;}
.badge-pass{background:#dcfce7;color:var(--green);border:1px solid #86efac;}
.badge-fail{background:#fee2e2;color:var(--red);border:1px solid #fca5a5;}
.badge-warn{background:#fef3c7;color:var(--yellow);border:1px solid #fcd34d;}
.badge-info{background:#dbeafe;color:var(--accent);border:1px solid #93c5fd;}
.badge-prog{background:#ede9fe;color:var(--purple);border:1px solid #c4b5fd;}
.prog-wrap{background:var(--border);border-radius:999px;height:6px;overflow:hidden;}
.prog-fill{height:6px;border-radius:999px;transition:width .4s ease;}
.section-heading{font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--text3);padding-bottom:8px;border-bottom:1px solid var(--border);margin-bottom:14px;}
table{width:100%;border-collapse:collapse;font-size:13px;}
th{background:var(--surface2);color:var(--text3);font-size:10px;letter-spacing:1px;text-transform:uppercase;padding:7px 12px;text-align:left;border-bottom:1px solid var(--border);font-weight:700;}
td{padding:8px 12px;border-bottom:1px solid var(--border);color:var(--text);}
tr:last-child td{border-bottom:none;}
tr:hover td{background:var(--surface2);}
[data-baseweb="input"] input,[data-baseweb="select"] div,textarea{
    background:var(--surface)!important;border-color:var(--border)!important;
    color:var(--text)!important;border-radius:8px!important;
    font-family:'Noto Sans TC',sans-serif!important;
}
.stButton>button{
    background:var(--accent)!important;color:#fff!important;border:none!important;
    border-radius:8px!important;font-weight:600!important;font-size:13px!important;
    font-family:'Noto Sans TC',sans-serif!important;
}
.stButton>button:hover{opacity:.85!important;}
[data-testid="stPageLink"]{border-radius:8px!important;width:100%!important;}
[data-testid="stPageLink"] p{font-size:13px!important;font-weight:500!important;color:#57534e!important;padding:7px 10px!important;margin:0!important;}
[data-testid="stPageLink"]:hover p{color:#1c1917!important;}
#MainMenu,footer,header{visibility:hidden!important;}
[data-testid="stDecoration"]{display:none!important;}
[data-testid="stHeader"]{display:none!important;}
/* multiselect tag */
[data-baseweb="tag"]{background:#dbeafe!important;border:1px solid #93c5fd!important;border-radius:6px!important;padding:2px 8px!important;margin:2px!important;}
[data-baseweb="tag"] span[title]{color:#1e40af!important;font-size:13px!important;font-weight:500!important;}
[data-baseweb="tag"] svg{color:#3b82f6!important;}
</style>""", unsafe_allow_html=True)

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
    st.page_link("app.py",                label="首頁")
    st.page_link("pages/1_dashboard.py",  label="畢業進度儀表板")
    st.page_link("pages/2_courses.py",    label="修課明細查詢")
    st.page_link("pages/3_ai_advisor.py", label="AI 選課顧問")
    st.page_link("pages/4_simulate.py",   label="模擬選課規劃")
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

col_left, col_right = st.columns([1, 1.6], gap='large')

# ── 左欄：缺修摘要 + 設定 ────────────────────────────────
with col_left:
    st.markdown("<div class='section-heading'>⚠️ 目前缺修狀況</div>", unsafe_allow_html=True)

    if not s["required"]["pass"]:
        lack = s["required"]["credits_need"] - s["required"]["credits_done"]
        st.markdown(f"""<div style='background:#fee2e2;border:1px solid #fca5a5;
            border-left:4px solid #dc2626;border-radius:10px;
            padding:12px 16px;margin-bottom:10px'>
          <div style='font-weight:700;font-size:14px;color:#1c1917'>系訂必修</div>
          <div style='font-size:12px;color:#78716c;margin-top:3px'>
            缺 <b style='color:#dc2626'>{lack} 學分</b>（{len(s["required"]["miss"])} 門課）
          </div></div>""", unsafe_allow_html=True)

    if not s["mgt_required"]["pass"]:
        lack = s["mgt_required"]["credits_need"] - s["mgt_required"]["credits_done"]
        st.markdown(f"""<div style='background:#fef3c7;border:1px solid #fcd34d;
            border-left:4px solid #d97706;border-radius:10px;
            padding:12px 16px;margin-bottom:10px'>
          <div style='font-weight:700;font-size:14px;color:#1c1917'>管院共構必修</div>
          <div style='font-size:12px;color:#78716c;margin-top:3px'>
            缺 <b style='color:#d97706'>{lack} 學分</b>
          </div></div>""", unsafe_allow_html=True)

    if not s["elective_pass"]:
        lack = s["elective_need"] - s["elective_done"]
        st.markdown(f"""<div style='background:#ede9fe;border:1px solid #c4b5fd;
            border-left:4px solid #7c3aed;border-radius:10px;
            padding:12px 16px;margin-bottom:10px'>
          <div style='font-weight:700;font-size:14px;color:#1c1917'>系選修</div>
          <div style='font-size:12px;color:#78716c;margin-top:3px'>
            缺 <b style='color:#7c3aed'>{lack} 學分</b>（最低需 {s["elective_need"]} 學分）
          </div></div>""", unsafe_allow_html=True)

    if s["graduation_ok"]:
        st.markdown("""<div style='background:#dcfce7;border:1px solid #86efac;
            border-left:4px solid #16a34a;border-radius:10px;
            padding:12px 16px;margin-bottom:10px;text-align:center'>
            <div style='font-size:20px'>🎉</div>
            <div style='font-weight:700;color:#16a34a;margin-top:3px'>已達所有門檻</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div class='section-heading' style='margin-top:16px'>設定偏好</div>", unsafe_allow_html=True)
    interest = st.multiselect("興趣方向", [
        "AI / 機器學習", "資安", "前後端開發", "數據分析",
        "企業管理", "金融科技", "醫療資訊"
    ], default=["AI / 機器學習"])
    extra = st.text_area("補充說明（選填）", placeholder="例：想往數據科學發展…", height=80)
    api_key = st.text_input("OpenAI API Key（選填）", type="password", placeholder="sk-…（留空使用內建回應）")

# ── 右欄：對話介面 ────────────────────────────────────────
with col_right:
    st.markdown("<div class='section-heading'>💬 AI 選課顧問對話</div>", unsafe_allow_html=True)

    if "ai_chat" not in st.session_state:
        st.session_state.ai_chat = []

    for msg in st.session_state.ai_chat:
        if msg["role"] == "user":
            st.markdown(f"""<div style='background:#dbeafe;border:1px solid #93c5fd;border-radius:12px 12px 4px 12px;
                padding:14px 18px;margin:10px 0;margin-left:20%'>{msg['content']}</div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div style='background:#f5f4f1;border:1px solid #e2e0d9;border-radius:12px 12px 12px 4px;
                padding:14px 18px;margin:10px 0;margin-right:20%;line-height:1.7'>🤖 {msg['content']}</div>""", unsafe_allow_html=True)

    # 快捷問題
    if not st.session_state.ai_chat:
        st.markdown("""<style>
        div[data-testid="stHorizontalBlock"] .stButton>button {
            background: #f5f4f1 !important;
            color: #374151 !important;
            border: 1px solid #e2e0d9 !important;
            font-size: 12px !important;
            font-weight: 500 !important;
            padding: 8px 12px !important;
            text-align: left !important;
            width: 100% !important;
        }
        div[data-testid="stHorizontalBlock"] .stButton>button:hover {
            background: #e2e0d9 !important;
            color: #1c1917 !important;
        }
        </style>""", unsafe_allow_html=True)
        st.markdown("<div style='color:#78716c;font-size:12px;font-weight:600;margin-bottom:8px;letter-spacing:0.5px'>💡 快速提問</div>", unsafe_allow_html=True)
        qcols = st.columns(2)
        quick_qs = ["幫我分析缺修哪些課", "推薦最適合我的三門課", "大三下學期應該選什麼", "如何最快達成畢業門檻"]
        for i, q in enumerate(quick_qs):
            with qcols[i % 2]:
                if st.button(q, key=f"qq_{i}"):
                    st.session_state._quick_q = q
                    st.rerun()

    user_input = None
    if hasattr(st.session_state, "_quick_q"):
        user_input = st.session_state._quick_q
        del st.session_state._quick_q

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    ci, cs = st.columns([5, 1])
    with ci:
        typed = st.text_input("輸入問題…", label_visibility="collapsed", placeholder="輸入你的問題，例：推薦我下學期要選哪些課？")
    with cs:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        send = st.button("送出")

    if (send and typed) or user_input:
        question = user_input or typed

        # 組裝 context
        lack_list = []
        if not s["required"]["pass"]:
            lack_list.append(f"系訂必修缺 {s['required']['credits_need']-s['required']['credits_done']} 學分")
        if not s["mgt_required"]["pass"]:
            lack_list.append(f"管院共構必修缺 {s['mgt_required']['credits_need']-s['mgt_required']['credits_done']} 學分")
        if not s["elective_pass"]:
            lack_list.append(f"系選修缺 {s['elective_need']-s['elective_done']} 學分")

        system_prompt = f"""你是長庚大學資管系的 AI 選課顧問。
學生目前狀況：總修 {s['total_credits']} 學分，興趣：{', '.join(interest) if interest else '未指定'}
缺修：{', '.join(lack_list) if lack_list else '全部達標'}
{f'補充：{extra}' if extra else ''}
請用繁體中文回答，語氣友善，具體有條理，適時使用條列說明。"""

        st.session_state.ai_chat.append({"role": "user", "content": question})

        with st.spinner("AI 分析中…"):
            ai_reply = None
            if api_key and api_key.startswith("sk-"):
                try:
                    resp = req_lib.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                        json={"model": "gpt-4o-mini",
                              "messages": [{"role": "system", "content": system_prompt}] +
                                          [{"role": m["role"], "content": m["content"]}
                                           for m in st.session_state.ai_chat],
                              "max_tokens": 600}, timeout=20)
                    ai_reply = resp.json()["choices"][0]["message"]["content"]
                except Exception as e:
                    ai_reply = f"⚠️ API 呼叫失敗：{e}"

            if not ai_reply:
                if "缺修" in question or "分析" in question:
                    ai_reply = f"""根據你的修課紀錄，目前缺修情況：\n\n{''.join(f'• {l}' + chr(10) for l in lack_list) if lack_list else '✓ 所有門檻均已達標！'}
\n建議優先補足缺修學分最多的類別，避免大四壓力過大。"""
                elif "推薦" in question or "選什麼" in question:
                    ai_reply = f"""根據你的興趣（{'、'.join(interest) if interest else '未設定'}），推薦以下方向：

1. **優先補足缺修必修課程** — 這些不能替代，必須修完
2. **選修貼近興趣的課程** — 提升學習動力，也有助就業
3. **選 3 學分的課** — 效益最高，避免小學分課分散精力

可以在左側補充你的具體情況，我會給出更精準的建議！"""
                elif "最快" in question or "畢業" in question:
                    ai_reply = f"""最快達成畢業門檻的策略：

1. **先修必修課** — 系訂必修和管院共構必修沒有彈性，必須完成
2. **集中補系選修** — 目前系選修 {s['elective_done']} 學分，需達 {s['elective_need']} 學分
3. **善用暑期課程** — 可補充部分學分，縮短修業時間
4. **避免重修** — 每門課盡量一次通過，節省時間"""
                else:
                    ai_reply = f"""你好！我是你的 AI 選課顧問 🤖

目前你共修習 **{s['total_credits']} 學分**，{'所有門檻均已達標 🎉' if s['graduation_ok'] else '尚有部分缺修'}。

你可以問我：
• 「幫我分析缺修哪些課」
• 「推薦我下學期選什麼」
• 「如何最快達成畢業門檻」"""

        st.session_state.ai_chat.append({"role": "assistant", "content": ai_reply})
        st.rerun()

    if st.session_state.ai_chat:
        if st.button("🗑️ 清除對話"):
            st.session_state.ai_chat = []
            st.rerun()
