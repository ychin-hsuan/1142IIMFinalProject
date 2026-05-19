import streamlit as st
# 假設你把剛才的邏輯寫成函式放在 main.py，可以直接 import 過來
# from main import get_database_info, calculate_credits

st.set_page_config(page_title="CGU 學分檢核系統", page_icon="🎓")

st.title("🎓 個人學分檢核系統")
st.subheader("長庚資管二 - 楊沁璇 (Kiki)")

# 模擬目前的總學分 (之後改為從 API 抓取的變數)
total_credits = 28 
graduation_threshold = 128 # 假設畢業門檻

# --- 製作進度條 (編號 7 的視覺化儀表板) ---
progress_ratio = total_credits / graduation_threshold

col1, col2 = st.columns(2)
with col1:
    st.metric(label="目前累積學分", value=f"{total_credits} / {graduation_threshold}")
with col2:
    st.metric(label="達成率", value=f"{progress_ratio:.1%}")

st.progress(progress_ratio)

if total_credits < 50:
    st.warning("⚠️ 提醒：目前學分進度較慢，記得確認通識領域是否修齊喔！")
else:
    st.success("✅ 進度良好，繼續保持！")