import streamlit as st
import sys, os, json, requests
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.data import get_student_taken, compute_status, ELECTIVE_DOMAINS

st.set_page_config(page_title="AI 選課顧問", page_icon="🤖", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700;900&family=Space+Mono:wght@400;700&display=swap');
:root{--bg:#0d0f14;--surface:#151820;--surface2:#1c2030;--border:#2a2f42;
     --accent:#4f8ef7;--accent2:#7c5cfc;--green:#2ecc8a;--red:#ff4d6d;
     --yellow:#f5c518;--text:#e8ecf4;--muted:#7a8099;--radius:12px;}
html,body,[data-testid="stAppViewContainer"]{background:var(--bg)!important;color:var(--text)!important;font-family:'Noto Sans TC',sans-serif!important;}
[data-testid="stSidebar"]{background:var(--surface)!important;border-right:1px solid var(--border)!important;}
[data-testid="stSidebar"] *{color:var(--text)!important;}
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:20px 24px;margin-bottom:14px;}
.badge{display:inline-block;padding:3px 10px;border-radius:999px;font-size:11px;font-weight:700;}
.badge-pass{background:#0e3d2a;color:#2ecc8a;border:1px solid #2ecc8a;}
.badge-fail{background:#3d0e1a;color:#ff4d6d;border:1px solid #ff4d6d;}
.badge-info{background:#0e2040;color:#4f8ef7;border:1px solid #4f8ef7;}
.badge-warn{background:#3d3000;color:#f5c518;border:1px solid #f5c518;}
.section-heading{font-size:11px;font-weight:800;letter-spacing:3px;text-transform:uppercase;color:#7a8099;padding:6px 0 12px;border-bottom:1px solid var(--border);margin-bottom:20px;}
.chat-user{background:#1a2a4a;border:1px solid #2a3f6f;border-radius:12px 12px 4px 12px;padding:14px 18px;margin:10px 0;margin-left:20%;}
.chat-ai{background:#1c2030;border:1px solid #2a2f42;border-radius:12px 12px 12px 4px;padding:14px 18px;margin:10px 0;margin-right:20%;line-height:1.7;}
[data-baseweb="input"] input{background:#1c2030!important;border-color:#2a2f42!important;color:var(--text)!important;}
textarea{background:#1c2030!important;border-color:#2a2f42!important;color:var(--text)!important;border-radius:8px!important;}
.stButton>button{background:linear-gradient(135deg,#4f8ef7,#7c5cfc)!important;color:#fff!important;border:none!important;border-radius:8px!important;font-weight:700!important;}
#MainMenu,footer,header{visibility:hidden;}[data-testid="stDecoration"]{display:none;}
</style>
""", unsafe_allow_html=True)

student = st.session_state.get("student", {"id":"B1344062","name":"示範學生","grade":"大三"})
taken   = get_student_taken(student)
s       = compute_status(taken)

st.markdown(f"""
<div style='padding:24px 0 16px'>
  <div style='font-size:11px;letter-spacing:3px;color:#7c5cfc;font-weight:700;text-transform:uppercase'>AI 選課顧問</div>
  <h2 style='font-size:26px;font-weight:900;margin:4px 0'>個人化選課建議</h2>
  <p style='color:#7a8099;font-size:14px'>AI 依據你的修課紀錄與缺少學分，提供最適合的選課建議</p>
</div>
""", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1.6], gap="large")

# ── 左欄：缺修摘要 ───────────────────────────────────────
with col_left:
    st.markdown("<div class='section-heading'>⚠️ 目前缺修狀況</div>", unsafe_allow_html=True)

    for domain, info in s["domains"].items():
        if not info["pass"]:
            lack = info["need"] - info["done"]
            st.markdown(f"""
            <div class='card' style='padding:14px 18px;border-left:3px solid {info["color"]}'>
              <div style='font-weight:700;font-size:14px'>{domain}</div>
              <div style='color:#7a8099;font-size:12px;margin-top:3px'>
                缺 <b style='color:{info["color"]}'>{lack} 學分</b> ｜ 已修 {info["done"]}/{info["need"]}
              </div>
            </div>
            """, unsafe_allow_html=True)

    miss_req = s["required"]["miss"] + s["mgt_required"]["miss"]
    if miss_req:
        st.markdown(f"""
        <div class='card' style='border-left:3px solid #ff4d6d;padding:14px 18px'>
          <div style='font-weight:700;font-size:14px'>必修課程</div>
          <div style='color:#7a8099;font-size:12px;margin-top:3px'>
            缺 <b style='color:#ff4d6d'>{len(miss_req)} 門</b> 必修課
          </div>
        </div>
        """, unsafe_allow_html=True)

    if all(v["pass"] for v in s["domains"].values()) and not miss_req:
        st.markdown("""<div class='card' style='border-left:3px solid #2ecc8a;padding:14px 18px;text-align:center'>
            <div style='font-size:22px;margin-bottom:4px'>🎉</div>
            <div style='font-weight:700;color:#2ecc8a'>已達所有門檻</div>
            <div style='font-size:12px;color:#7a8099;margin-top:4px'>可詢問進階或跨域課程建議</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div class='section-heading' style='margin-top:16px'>設定 AI 偏好</div>", unsafe_allow_html=True)

    interest = st.multiselect(
        "我的興趣方向",
        ["AI / 機器學習", "資安", "前後端開發", "數據分析", "企業管理", "金融科技", "醫療資訊"],
        default=["AI / 機器學習", "數據分析"]
    )
    extra_context = st.text_area(
        "補充說明（選填）",
        placeholder="例：我想往數據科學發展，希望推薦需要程式基礎的課程…",
        height=80
    )
    api_key = st.text_input(
        "OpenAI / Gemini API Key（選填）",
        type="password",
        placeholder="sk-…（留空使用內建回應）"
    )

# ── 右欄：AI 聊天介面 ────────────────────────────────────
with col_right:
    st.markdown("<div class='section-heading'>💬 AI 選課顧問對話</div>", unsafe_allow_html=True)

    # 聊天紀錄
    if "ai_chat" not in st.session_state:
        st.session_state.ai_chat = []

    # 顯示對話
    for msg in st.session_state.ai_chat:
        if msg["role"] == "user":
            st.markdown(f"<div class='chat-user'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-ai'>🤖 {msg['content']}</div>", unsafe_allow_html=True)

    # 快捷問題
    if not st.session_state.ai_chat:
        st.markdown("<div style='color:#7a8099;font-size:13px;margin-bottom:12px'>💡 快速提問：</div>", unsafe_allow_html=True)
        q_cols = st.columns(2)
        quick_questions = [
            "幫我分析缺修哪些選修課",
            "推薦最適合我的三門課",
            "大三下學期應該選什麼",
            "如何最快達成畢業門檻",
        ]
        for i, q in enumerate(quick_questions):
            with q_cols[i % 2]:
                if st.button(q, key=f"q_{i}", use_container_width=True):
                    st.session_state._quick_q = q
                    st.rerun()

    # 處理快捷問題
    if hasattr(st.session_state, "_quick_q"):
        user_input = st.session_state._quick_q
        del st.session_state._quick_q
    else:
        user_input = None

    # 輸入框
    col_input, col_send = st.columns([5, 1])
    with col_input:
        typed = st.text_input("輸入你的問題…", label_visibility="collapsed",
                              placeholder="例：推薦我下學期要選哪些課？")
    with col_send:
        send = st.button("送出", use_container_width=True)

    if (send and typed) or user_input:
        question = user_input or typed

        # 組裝 context
        lack_domains = [f"{d}（缺 {v['need']-v['done']} 學分）"
                        for d, v in s["domains"].items() if not v["pass"]]
        avail_courses = []
        for domain, info in s["domains"].items():
            for c in info["missing"][:5]:
                avail_courses.append(f"{c['name']}（{domain}，{c['credits']} 學分）")

        system_prompt = f"""你是長庚大學資管系的 AI 選課顧問，幫助學生規劃修課。
學生資料：
- 姓名：{student['name']}，年級：{student.get('grade','大三')}
- 興趣方向：{', '.join(interest) if interest else '未指定'}
- 缺修領域：{', '.join(lack_domains) if lack_domains else '全部達標'}
- 可選修課程（部分）：{', '.join(avail_courses[:15])}
{f'補充說明：{extra_context}' if extra_context else ''}

請用繁體中文回答，語氣友善，回答要具體、有條理，適時使用條列式說明。"""

        st.session_state.ai_chat.append({"role": "user", "content": question})

        with st.spinner("AI 分析中…"):
            ai_reply = None

            # ── 嘗試呼叫 OpenAI API ──────────────────────
            if api_key and api_key.startswith("sk-"):
                try:
                    resp = requests.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                        json={
                            "model": "gpt-4o-mini",
                            "messages": [
                                {"role": "system", "content": system_prompt},
                                *[{"role": m["role"], "content": m["content"]}
                                  for m in st.session_state.ai_chat],
                            ],
                            "max_tokens": 600,
                        }, timeout=20
                    )
                    ai_reply = resp.json()["choices"][0]["message"]["content"]
                except Exception as e:
                    ai_reply = f"⚠️ API 呼叫失敗：{e}"

            # ── Fallback：規則式回應 ──────────────────────
            if not ai_reply:
                if "缺修" in question or "分析" in question:
                    if lack_domains:
                        ai_reply = f"""根據你的修課紀錄，目前在以下領域仍有缺修：

{chr(10).join(f'• {d}' for d in lack_domains)}

**建議優先修習：**
{chr(10).join(f'• {c}' for c in avail_courses[:6])}

建議大三下學期優先補足缺修學分最多的領域，避免大四選課壓力過大。"""
                    else:
                        ai_reply = "🎉 恭喜！你的各領域選修學分均已達標，可以考慮選修進階或跨領域課程豐富學習歷程！"

                elif "推薦" in question or "選什麼" in question:
                    recs = avail_courses[:3] if avail_courses else ["數據處理基礎（數據創新與智能互動）", "資訊安全導論（資通訊安全）"]
                    interests_str = "、".join(interest) if interest else "你的興趣方向"
                    ai_reply = f"""根據你的興趣（{interests_str}）及缺修狀況，推薦以下 3 門課：

1. **{recs[0].split('（')[0] if recs else '雲端機器學習'}**
   — 與 AI 方向高度相關，且可補足領域學分

2. **{recs[1].split('（')[0] if len(recs)>1 else '資料視覺化'}**
   — 實務性強，畢業後求職加分明顯

3. **{recs[2].split('（')[0] if len(recs)>2 else '區塊鏈實務與應用'}**
   — 跨領域熱門課程，與目前產業趨勢契合

建議先確認各課程的選課人數與老師評價，再做最終決定 🎯"""

                elif "最快" in question or "畢業" in question:
                    ai_reply = f"""要最快達成畢業門檻，建議以下策略：

**1. 優先補足缺修必修課**（不能延畢）
{chr(10).join(f'   • {c["name"]}' for c in (s["required"]["miss"] + s["mgt_required"]["miss"])[:3]) or '   • 目前必修已全部完成 ✓'}

**2. 集中火力在缺學分最多的領域**
{chr(10).join(f'   • {d}' for d in lack_domains[:2]) if lack_domains else '   • 各領域均已達標 ✓'}

**3. 選擇 3 學分課程**效益最高，避免 1-2 學分小課分散學期修課精力。

**4. 暑期選修**也可補充部分學分，建議善用暑假課程。"""

                else:
                    ai_reply = f"""你好！我是你的 AI 選課顧問 🤖

關於「{question}」—

目前你共修習了 **{s['total_credits']} 學分**，{'各領域均已達標 🎉' if not lack_domains else f'有 {len(lack_domains)} 個領域尚未達標'}。

你可以問我：
• 「幫我分析缺修哪些課」—— 查看詳細缺修狀況
• 「推薦我下學期選什麼」—— 依興趣個人化推薦
• 「如何最快達成畢業門檻」—— 規劃最短路徑策略

也可以在左側設定興趣方向，讓建議更精準！"""

        st.session_state.ai_chat.append({"role": "assistant", "content": ai_reply})
        st.rerun()

    # 清除對話按鈕
    if st.session_state.ai_chat:
        if st.button("🗑️  清除對話紀錄"):
            st.session_state.ai_chat = []
            st.rerun()
