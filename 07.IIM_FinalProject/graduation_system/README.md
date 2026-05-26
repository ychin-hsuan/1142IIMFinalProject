# 🎓 畢業初審系統

### 長庚大學資管系 ｜ 114 入學版

基於 Streamlit 的畢業學分自動審查網站，整合 Notion API 與 AI 選課建議。

### 如何開啟網站

```
cd graduation_system
pip install streamlit
streamlit hello
streamlit run app.py

```

---

## 📁 專案結構

```
graduation_system/
├── app.py                   # 首頁 / 學生登入
├── requirements.txt
├── utils/
│   └── data.py              # 課程地圖資料 + 示範修課紀錄 + 計算邏輯
└── pages/
    ├── 1_dashboard.py       # 畢業進度儀表板
    ├── 2_courses.py         # 修課明細查詢
    ├── 3_ai_advisor.py      # AI 選課顧問
    └── 4_simulate.py        # 模擬選課規劃
```

---

## 🚀 快速啟動

```bash
# 1. 安裝相依套件
pip install -r requirements.txt

# 2. 啟動開發伺服器
streamlit run app.py
```

瀏覽器開啟 `http://localhost:8501`

---

## 🔌 Notion API 串接（選用）

1. 前往 [notion.so/my-integrations](https://www.notion.so/my-integrations) 建立 Integration
2. 複製 **Internal Integration Token**（`secret_xxx...`）
3. 在你的修課紀錄 Notion Database 頁面，點選右上角「...」→「Add connections」→ 選你的 Integration
4. 複製 Database URL 中的 32 位 ID
5. 在網站首頁輸入 Token 與 Database ID

> 若不填寫，系統會使用示範資料（B1344062 楊沁璇）

---

## 🤖 AI 功能設定

### OpenAI（推薦）

在 AI 選課顧問頁面輸入你的 `sk-...` API Key

### Google Gemini

修改 `pages/3_ai_advisor.py` 中的 API 呼叫區段：

```python
# 將 OpenAI endpoint 替換為：
"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
```

---

## ☁️ 部署到 Streamlit Cloud

1. Push 此專案到 GitHub
2. 前往 [share.streamlit.io](https://share.streamlit.io)
3. 選擇 repo，Main file path 填 `app.py`
4. 在 **Secrets** 中可設定：
   ```toml
   OPENAI_API_KEY = "sk-..."
   NOTION_TOKEN   = "secret_..."
   ```

---

## 📋 畢業門檻規則（114 入學）

| 類別                        | 最低要求  |
| --------------------------- | --------- |
| 系必修                      | 全部通過  |
| 管院共必修                  | 全部通過  |
| 企業管理 領域選修           | ≥ 9 學分  |
| 資訊技術 領域選修           | ≥ 9 學分  |
| 資通訊安全 領域選修         | ≥ 6 學分  |
| 數據創新與智能互動 領域選修 | ≥ 9 學分  |
| 企業資訊應用 領域選修       | ≥ 6 學分  |
| 實習（校外/企業/台塑）      | 至少 1 種 |
| 通識                        | ≥ 18 學分 |

---

## 🛠 未來擴充方向

- [ ] Notion OCR：上傳成績單圖片自動辨識
- [ ] 多學年版本支援（112/113 入學）
- [ ] 學號驗證與個人隱私保護
- [ ] 班級統計後台（老師視角）
- [ ] Email 通知缺修提醒
