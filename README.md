# HW2 氣溫預報 Web App

這是一個使用 CWA 氣象局 API 製作的氣溫預報 Web App 作業，包含資料爬取、分析、存儲與視覺化呈現。

---

## 功能說明

| 部分 | 說明 |
|------|------|
| **HW2-1** | 使用 `requests` 套件呼叫 CWA API（F-A0010-001），取得台灣北、中、南、東北、東、東南部六區一週氣象預報 JSON 資料 |
| **HW2-2** | 解析 JSON，提取每日 `MaxT`（最高氣溫）與 `MinT`（最低氣溫），以 `json.dumps` 觀察結果 |
| **HW2-3** | 建立 SQLite3 資料庫 `data.db`，建立 `TemperatureForecasts` 表並寫入資料，附查詢驗證 |
| **HW2-4** | Streamlit Web App：下拉選單、折線圖、表格、Folium 可縮放地圖（依日期顯示各區氣溫標記） |

---

## 檔案結構

```
氣象局/
├── app.py              # HW2-4：Streamlit Web App 主程式
├── init_db.py          # HW2-1 ~ HW2-3：資料抓取、分析與資料庫建立
├── requirements.txt    # Python 套件依賴清單
├── development_log.md  # 開發日誌
└── README.md           # 本說明文件
```

---

## 本地執行步驟

### 1. 安裝依賴套件

```bash
pip install -r requirements.txt
```

### 2. 初始化資料庫（HW2-1 ~ HW2-3）

從 CWA API 抓取最新氣象資料並存入 `data.db`：

```bash
python init_db.py
```

執行後會在終端機看到：
- 原始 API 回傳的 JSON 片段（HW2-1 觀察）
- 提取出的最高/最低氣溫資料（HW2-2 觀察）
- 資料庫儲存完成確認 + 查詢驗證（HW2-3）

### 3. 啟動 Web App（HW2-4）

```bash
python -m streamlit run app.py
```

開啟瀏覽器前往：**http://localhost:8501**

> **備註**：若 `data.db` 不存在，App 啟動時會自動呼叫 `init_db()` 建立資料庫。
> 側邊欄也有 **🔄 重新抓取最新資料** 按鈕可手動更新。

---

## Streamlit Cloud 部署（Live Demo）

1. 前往 [share.streamlit.io](https://share.streamlit.io) 並以 GitHub 帳號登入
2. 點「New app」，填入：
   - **Repository**: `Moeta034/weather`
   - **Branch**: `main`
   - **Main file path**: `app.py`
3. 點「Deploy!」即可，首次啟動會自動建立資料庫

---

## 使用的技術

- **API**: [CWA 氣象資料開放平台](https://opendata.cwa.gov.tw)（資料集：F-A0010-001）
- **語言**: Python 3
- **套件**: `requests`, `sqlite3`, `streamlit`, `pandas`, `folium`, `streamlit-folium`
