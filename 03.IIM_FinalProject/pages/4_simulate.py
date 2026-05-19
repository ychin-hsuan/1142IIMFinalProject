import streamlit as st
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.data import get_student_taken, compute_status, ELECTIVE_DOMAINS, REQUIRED_COURSES, MGT_REQUIRED

st.set_page_config(page_title="模擬選課規劃", page_icon="🔮", layout="wide")

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
.prog-wrap{background:#2a2f42;border-radius:999px;height:10px;overflow:hidden;margin-top:6px;}
.prog-fill{height:10px;border-radius:999px;transition:width .5s ease;}
.section-heading{font-size:11px;font-weight:800;letter-spacing:3px;text-transform:uppercase;color:#7a8099;padding:6px 0 12px;border-bottom:1px solid var(--border);margin-bottom:20px;}
[data-baseweb="checkbox"] label{color:var(--text)!important;}
[data-baseweb="checkbox"] div[aria-checked="true"]{background:#4f8ef7!important;border-color:#4f8ef7!important;}
.stButton>button{background:linear-gradient(135deg,#4f8ef7,#7c5cfc)!important;color:#fff!important;border:none!important;border-radius:8px!important;font-weight:700!important;}
#MainMenu,footer,header{visibility:hidden;}[data-testid="stDecoration"]{display:none;}
</style>
""", unsafe_allow_html=True)

student = st.session_state.get("student", {"id":"B1344062","name":"示範學生","grade":"大三"})
taken   = get_student_taken(student)
s       = compute_status(taken)

st.markdown(f"""
<div style='padding:24px 0 16px'>
  <div style='font-size:11px;letter-spacing:3px;color:#7c5cfc;font-weight:700;text-transform:uppercase'>模擬選課規劃</div>
  <h2 style='font-size:26px;font-weight:900;margin:4px 0'>勾選課程，即時預覽畢業門檻達成狀況</h2>
  <p style='color:#7a8099;font-size:14px'>將未來欲修課程打勾後，右側進度即時更新</p>
</div>
""", unsafe_allow_html=True)

# ── 初始化模擬清單 ────────────────────────────────────────
if "sim_courses" not in st.session_state:
    st.session_state.sim_courses = set()

col_select, col_preview = st.columns([1.2, 1], gap="large")

# ── 左欄：選課面板 ────────────────────────────────────────
with col_select:
    st.markdown("<div class='section-heading'>📌 選擇欲修課程</div>", unsafe_allow_html=True)

    # 必修缺修
    miss_req = s["required"]["miss"] + s["mgt_required"]["miss"]
    if miss_req:
        with st.expander(f"⚠️ 缺修必修課程（{len(miss_req)} 門）", expanded=True):
            for c in miss_req:
                key = f"sim_req_{c['name']}"
                checked = c["name"] in st.session_state.sim_courses
                if st.checkbox(f"📚 {c['name']}（{c['credits']} 學分）", value=checked, key=key):
                    st.session_state.sim_courses.add(c["name"])
                elif c["name"] in st.session_state.sim_courses:
                    st.session_state.sim_courses.discard(c["name"])

    # 各領域選修
    for domain, info in ELECTIVE_DOMAINS.items():
        lack = info["need"] - s["domains"][domain]["done"]
        badge = f"✓ 達標" if s["domains"][domain]["pass"] else f"缺 {lack} 學分"
        color = info["color"]

        with st.expander(f"{domain}　　{badge}", expanded=not s["domains"][domain]["pass"]):
            missing_in_domain = [c for c in info["courses"]
                                 if c["name"] not in s["taken_names"]]
            if not missing_in_domain:
                st.markdown("<span style='color:#2ecc8a;font-size:13px'>✓ 此領域已全部達標</span>",
                            unsafe_allow_html=True)
            else:
                for c in missing_in_domain:
                    key = f"sim_{domain}_{c['name']}"
                    checked = c["name"] in st.session_state.sim_courses
                    if st.checkbox(f"{c['name']}（{c['credits']} 學分）", value=checked, key=key):
                        st.session_state.sim_courses.add(c["name"])
                    elif c["name"] in st.session_state.sim_courses:
                        st.session_state.sim_courses.discard(c["name"])

    if st.button("🔄  清除所有模擬選課", use_container_width=True):
        st.session_state.sim_courses = set()
        st.rerun()

# ── 右欄：即時預覽 ────────────────────────────────────────
with col_preview:
    st.markdown("<div class='section-heading'>📊 畢業達成率預覽</div>", unsafe_allow_html=True)

    # 計算「修習 + 模擬選課」後的狀態
    sim_taken = dict(taken)
    for name in st.session_state.sim_courses:
        if name not in sim_taken:
            # 找出學分數
            for c in REQUIRED_COURSES + MGT_REQUIRED:
                if c["name"] == name:
                    sim_taken[name] = {"credits": c["credits"], "grade": "（預定）", "score": ""}
            for info in ELECTIVE_DOMAINS.values():
                for c in info["courses"]:
                    if c["name"] == name:
                        sim_taken[name] = {"credits": c["credits"], "grade": "（預定）", "score": ""}

    sim_s = compute_status(sim_taken)

    # 模擬選課摘要
    sim_count = len(st.session_state.sim_courses)
    sim_credits = sum(
        sim_taken[n]["credits"] for n in st.session_state.sim_courses
        if n in sim_taken
    )
    st.markdown(f"""
    <div class='card' style='background:linear-gradient(135deg,#0e2040,#1a1a35);
         border-color:#2a3f6f;margin-bottom:20px;text-align:center'>
      <div style='font-size:12px;color:#7a8099;margin-bottom:8px'>模擬新增選課</div>
      <div style='font-family:Space Mono,monospace;font-size:32px;font-weight:700;color:#4f8ef7'>
        +{sim_credits}
      </div>
      <div style='color:#7a8099;font-size:13px'>學分 ｜ {sim_count} 門課程</div>
    </div>
    """, unsafe_allow_html=True)

    # 各領域進度對比
    for domain, info in sim_s["domains"].items():
        orig   = s["domains"][domain]
        new_done = info["done"]
        need     = info["need"]
        old_done = orig["done"]
        color    = info["color"]
        diff     = new_done - old_done

        if orig["pass"] and not diff:
            badge = "<span class='badge badge-pass'>達標</span>"
        elif info["pass"]:
            badge = "<span class='badge badge-pass'>模擬達標 ✓</span>"
        else:
            badge = f"<span class='badge badge-fail'>缺 {need-new_done} 學分</span>"

        diff_html = f"<span style='color:#2ecc8a;font-size:11px'> +{diff}</span>" if diff > 0 else ""

        pct_new = min(100, int(new_done / need * 100))
        pct_old = min(100, int(old_done / need * 100))

        st.markdown(f"""
        <div style='margin-bottom:18px'>
          <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:5px'>
            <span style='font-size:13px;font-weight:600'>{domain}</span>
            {badge}
          </div>
          <div style='display:flex;align-items:center;gap:12px'>
            <div style='flex:1;position:relative'>
              <div class='prog-wrap'>
                <div class='prog-fill' style='width:{pct_old}%;background:#2a2f42;position:absolute;top:0;left:0'></div>
                <div class='prog-fill' style='width:{pct_new}%;background:{color}'></div>
              </div>
            </div>
            <span style='font-family:Space Mono,monospace;font-size:12px;color:#7a8099;white-space:nowrap'>
              {new_done}/{need}{diff_html}
            </span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # 圓餅圖
    st.markdown("<div class='section-heading' style='margin-top:8px'>整體學分分布（模擬後）</div>", unsafe_allow_html=True)

    fig = go.Figure(go.Bar(
        x=list(sim_s["domains"].keys()),
        y=[v["done"] for v in sim_s["domains"].values()],
        marker_color=[v["color"] for v in sim_s["domains"].values()],
        text=[f"{v['done']}/{v['need']}" for v in sim_s["domains"].values()],
        textposition="outside",
        textfont=dict(color="#e8ecf4", size=11),
        hovertemplate="%{x}: %{y} 學分<extra></extra>",
    ))
    # 需求線
    for i, (domain, info) in enumerate(sim_s["domains"].items()):
        fig.add_shape(type="line", x0=i-0.4, x1=i+0.4,
                      y0=info["need"], y1=info["need"],
                      line=dict(color="#ff4d6d", width=2, dash="dot"))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=30, b=10, l=0, r=0), height=220,
        xaxis=dict(showgrid=False, tickfont=dict(color="#7a8099", size=10)),
        yaxis=dict(showgrid=True, gridcolor="#2a2f42", tickfont=dict(color="#7a8099")),
        bargap=0.3,
        annotations=[dict(x=0.5, y=1.1, xref="paper", yref="paper",
                          text="<span style='color:#ff4d6d'>— 紅虛線為最低修課門檻</span>",
                          showarrow=False, font=dict(size=10, color="#ff4d6d"))]
    )
    st.plotly_chart(fig, use_container_width=True)

    # 最終判斷
    all_domain_pass = all(v["pass"] for v in sim_s["domains"].values())
    req_all_pass    = not sim_s["required"]["miss"] and not sim_s["mgt_required"]["miss"]
    if all_domain_pass and req_all_pass:
        st.markdown("""<div style='background:linear-gradient(135deg,#0e3d2a,#0b2e20);
            border:1px solid #2ecc8a;border-radius:12px;padding:16px 20px;text-align:center'>
            <div style='font-size:28px;margin-bottom:4px'>🎓</div>
            <div style='font-weight:700;color:#2ecc8a;font-size:15px'>模擬結果：可申請畢業！</div>
            <div style='color:#7a8099;font-size:12px;margin-top:4px'>所有畢業門檻均已達標</div>
        </div>""", unsafe_allow_html=True)
    else:
        still_lack = [d for d, v in sim_s["domains"].items() if not v["pass"]]
        st.markdown(f"""<div style='background:#1c2030;border:1px solid #2a2f42;
            border-radius:12px;padding:16px 20px'>
            <div style='font-weight:700;color:#f5c518;margin-bottom:8px'>📋 模擬後仍有缺修</div>
            <div style='font-size:13px;color:#7a8099'>
              {'、'.join(still_lack) if still_lack else ''} 等領域需繼續補修
            </div>
        </div>""", unsafe_allow_html=True)
