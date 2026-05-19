import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from dotenv import load_dotenv
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(_root, ".env"), override=True)
import utils.data as _data
_data.NOTION_TOKEN = os.getenv("NOTION_TOKEN", "")
_data.NOTION_DB_ID = os.getenv("NOTION_DB_ID", "")

from utils.data import (get_student_taken, fetch_inprogress_courses,
                         compute_status, REQUIRED_COURSES, MGT_REQUIRED,
                         ALL_ELECTIVES, DOMAIN_COLORS, ELECTIVE_MIN_TOTAL)

st.set_page_config(page_title="模擬選課規劃", page_icon="🔮", layout="wide")

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

if 'sim_courses' not in st.session_state:
    st.session_state.sim_courses = {}

col_select, col_preview = st.columns([1.2, 1], gap='large')

# ── 左欄：選課面板 ────────────────────────────────────────
with col_select:
    st.markdown("<div class='section-heading'>📌 選擇欲修課程</div>", unsafe_allow_html=True)

    done_and_prog = s["taken_names"] | s["inprogress_names"]

    # 缺修必修
    miss_req = [c for c in (REQUIRED_COURSES + MGT_REQUIRED)
                if c["name"] not in done_and_prog]
    if miss_req:
        with st.expander(f"⚠️ 缺修必修（{len(miss_req)} 門）", expanded=True):
            for c in miss_req:
                is_mgt = c in MGT_REQUIRED
                checked = c["name"] in st.session_state.sim_courses
                label = f"{'[管院] ' if is_mgt else ''}{c['name']}（{c['credits']} 學分）"
                if st.checkbox(label, value=checked, key=f"sim_req_{c['name']}"):
                    st.session_state.sim_courses[c["name"]] = {
                        "credits": c["credits"],
                        "belonging": ["管院共構"] if is_mgt else ["系必修"],
                        "elective_domain": None,
                    }
                else:
                    st.session_state.sim_courses.pop(c["name"], None)

    # 各領域系選修（從 ALL_ELECTIVES 清單，排除已修/修習中）
    for domain, courses in ALL_ELECTIVES.items():
        color = DOMAIN_COLORS.get(domain, "#78716c")
        domain_done = s["domains"].get(domain, {}).get("done", 0)
        avail = [c for c in courses if c["name"] not in done_and_prog
                 and c["name"] not in st.session_state.sim_courses]
        sim_in_domain = {n: v for n, v in st.session_state.sim_courses.items()
                         if v.get("elective_domain") == domain}

        label = f"{domain}　{domain_done} 學分已修"
        if sim_in_domain:
            label += f"　+{sum(v['credits'] for v in sim_in_domain.values())} 模擬"

        with st.expander(label, expanded=False):
            # 已加入模擬的課程
            for cname, cinfo in list(sim_in_domain.items()):
                if not st.checkbox(
                    f"✓ {cname}（{cinfo['credits']} 學分）",
                    value=True, key=f"sim_sel_{cname}"
                ):
                    st.session_state.sim_courses.pop(cname, None)
                    st.rerun()

            # 可選的課程
            if avail:
                st.markdown(f"<div style='font-size:11px;color:#78716c;margin:8px 0 4px'>可選課程：</div>",
                            unsafe_allow_html=True)
                for c in avail:
                    if st.checkbox(
                        f"{c['name']}（{c['credits']} 學分，{c['semester']}）",
                        value=False, key=f"sim_avail_{c['name']}"
                    ):
                        st.session_state.sim_courses[c["name"]] = {
                            "credits": c["credits"],
                            "belonging": ["系選修"],
                            "elective_domain": domain,
                        }
                        st.rerun()
            else:
                st.markdown("<div style='font-size:12px;color:#16a34a'>✓ 此領域課程均已修或已加入模擬</div>",
                            unsafe_allow_html=True)

    if st.button("🔄 清除所有模擬選課"):
        st.session_state.sim_courses = {}
        st.rerun()

# ── 右欄：即時預覽 ────────────────────────────────────────
with col_preview:
    st.markdown("<div class='section-heading'>📊 畢業達成率預覽</div>", unsafe_allow_html=True)

    # 合併模擬進去計算
    sim_taken = dict(taken)
    for name, info in st.session_state.sim_courses.items():
        if name not in sim_taken:
            sim_taken[name] = {
                "credits":         info["credits"],
                "score":           0,
                "pass_fail":       False,
                "belonging":       info["belonging"],
                "elective_domain": info.get("elective_domain"),
            }
    sim_s = compute_status(sim_taken, inprogress)


    # 摘要
    sim_count = len(st.session_state.sim_courses)
    sim_cr    = sum(v["credits"] for v in st.session_state.sim_courses.values())
    st.markdown(f"""<div class='card' style='background:linear-gradient(135deg,#eff6ff,#eff6ff);
         border-color:#93c5fd;margin-bottom:20px;text-align:center'>
      <div style='font-size:12px;color:#78716c;margin-bottom:6px'>模擬新增選課</div>
      <div style='font-family:'DM Mono',monospace;font-size:32px;font-weight:700;color:#2563eb'>+{sim_cr}</div>
      <div style='color:#78716c;font-size:13px'>學分 ｜ {sim_count} 門課程</div>
    </div>""", unsafe_allow_html=True)

    # 必修進度條
    for label, orig, sim_val, need in [
        ("系訂必修",    s["required"]["credits_done"],     sim_s["required"]["credits_done"],     sim_s["required"]["credits_need"]),
        ("管院共構必修",s["mgt_required"]["credits_done"], sim_s["mgt_required"]["credits_done"], sim_s["mgt_required"]["credits_need"]),
    ]:
        pct   = min(100, int(sim_val / need * 100))
        diff  = sim_val - orig
        color = "#2ecc8a" if sim_val >= need else "#f5c518"
        badge = "<span class='badge badge-pass'>達標</span>" if sim_val >= need \
               else f"<span class='badge badge-fail'>缺 {need-sim_val}</span>"
        dhtml = f"<span style='color:#16a34a;font-size:11px'> +{diff}</span>" if diff > 0 else ""
        st.markdown(f"""<div style='margin-bottom:16px'>
          <div style='display:flex;justify-content:space-between;margin-bottom:5px'>
            <span style='font-size:13px;font-weight:600'>{label}</span>{badge}
          </div>
          <div style='display:flex;align-items:center;gap:10px'>
            <div class='prog-wrap' style='flex:1'>
              <div class='prog-fill' style='width:{pct}%;background:{color}'></div>
            </div>
            <span style='font-family:'DM Mono',monospace;font-size:12px;color:#78716c'>{sim_val}/{need}{dhtml}</span>
          </div></div>""", unsafe_allow_html=True)

    # 系選修總計
    ep    = min(100, int(sim_s["elective_done"] / ELECTIVE_MIN_TOTAL * 100))
    ed    = sim_s["elective_done"] - s["elective_done"]
    ec    = "#2ecc8a" if sim_s["elective_pass"] else "#ff4d6d"
    badge = "<span class='badge badge-pass'>達標</span>" if sim_s["elective_pass"] \
           else f"<span class='badge badge-fail'>缺 {ELECTIVE_MIN_TOTAL-sim_s['elective_done']}</span>"
    dhtml = f"<span style='color:#16a34a;font-size:11px'> +{ed}</span>" if ed > 0 else ""
    st.markdown(f"""<div style='margin-bottom:8px'>
      <div style='display:flex;justify-content:space-between;margin-bottom:5px'>
        <span style='font-size:13px;font-weight:600'>系選修總計</span>{badge}
      </div>
      <div style='display:flex;align-items:center;gap:10px'>
        <div class='prog-wrap' style='flex:1'>
          <div class='prog-fill' style='width:{ep}%;background:{ec}'></div>
        </div>
        <span style='font-family:'DM Mono',monospace;font-size:12px;color:#78716c'>{sim_s["elective_done"]}/{ELECTIVE_MIN_TOTAL}{dhtml}</span>
      </div></div>""", unsafe_allow_html=True)

    # 各領域明細
    st.markdown("<div style='margin-top:12px'>", unsafe_allow_html=True)
    for domain, info in sim_s["domains"].items():
        color = info["color"]
        orig_done = s["domains"].get(domain, {}).get("done", 0)
        diff  = info["done"] - orig_done
        dhtml = f"<span style='color:#16a34a;font-size:10px'> +{diff}</span>" if diff > 0 else ""
        st.markdown(f"""<div style='margin-bottom:10px;padding:8px 12px;background:#f5f4f1;border-radius:8px;
            border-left:3px solid {color}'>
          <div style='display:flex;justify-content:space-between'>
            <span style='font-size:12px'>{domain}</span>
            <span style='font-family:'DM Mono',monospace;font-size:12px;color:{color}'>{info["done"]} 學分{dhtml}</span>
          </div></div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 最終判斷
    st.markdown("<div style='margin-top:16px'>", unsafe_allow_html=True)
    if sim_s["graduation_ok"]:
        st.markdown("""<div style='background:linear-gradient(135deg,#dcfce7,#dcfce7);
            border:1px solid #86efac;border-radius:12px;padding:16px 20px;text-align:center'>
            <div style='font-size:28px;margin-bottom:4px'>🎓</div>
            <div style='font-weight:700;color:#16a34a;font-size:15px'>模擬結果：可申請畢業！</div>
            <div style='color:#78716c;font-size:12px;margin-top:4px'>所有畢業門檻均已達標</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div style='background:#f5f4f1;border:1px solid #e2e0d9;
            border-radius:12px;padding:16px 20px'>
            <div style='font-weight:700;color:#d97706;margin-bottom:6px'>📋 模擬後仍有缺修</div>
            <div style='font-size:13px;color:#78716c'>繼續在左側勾選欲修課程</div>
        </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
