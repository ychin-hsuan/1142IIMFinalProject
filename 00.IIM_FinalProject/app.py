import streamlit as st
from main import get_database_info, calculate_credits

# 網頁基本設定
st.set_page_config(page_title="CGU 學分檢核系統", page_icon="🎓", layout="wide")

st.title("🎓 個人學分檢核系統")
st.markdown("### 資訊管理導論期末專題")

# 側邊欄設定
st.sidebar.header("系統設定")
graduation_goal = st.sidebar.number_input("畢業門檻學分", value=128)

# 主畫面按鈕
if st.button("🔄 立即同步 Notion 資料庫"):
    with st.spinner("連線中..."):
        db_id = get_database_info()
        
        if db_id:
            semester_data, total_all = calculate_credits(db_id)
            
            # --- 頂部數據看板 ---
            st.divider()
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("已累積學分", f"{total_all} / {graduation_goal}")
            with col2:
                progress = min(total_all / graduation_goal, 1.0)
                st.metric("達成率", f"{progress:.1%}")
            with col3:
                remaining = max(graduation_goal - total_all, 0)
                st.metric("尚差學分", f"{remaining}")
            
            st.progress(progress)

            # --- 學期分頁顯示 ---
            st.write("## 📅 歷年修課明細")
            sorted_sems = sorted(semester_data.keys())
            
            if not sorted_sems:
                st.warning("資料庫內目前沒有課程資料。")
            else:
                tabs = st.tabs(sorted_sems)
                for i, sem in enumerate(sorted_sems):
                    with tabs[i]:
                        st.subheader(f"{sem} 學期")
                        sem_total = 0
                        
                        # 建立該學期的清單
                        for course in semester_data[sem]:
                            c1, c2 = st.columns([3, 1])
                            c1.write(f"📖 {course['name']}")
                            c2.write(f"`{course['credit']}` 學分")
                            sem_total += course['credit']
                        
                        st.divider()
                        st.success(f"**本學期小計：{sem_total} 學分**")
        else:
            st.error("❌ 找不到資料庫！請確認 Notion 頁面已 Connect to 你的 Integration。")

else:
    st.info("請點擊上方按鈕開始同步您的修課紀錄。")