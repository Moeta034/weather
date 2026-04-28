# HW2 氣溫預報 Web App

這是一個使用 CWA 氣象局 API 製作的氣溫預報 Web App 作業，包含資料爬取、分析、存儲與視覺化呈現。

## 功能

*   **資料獲取與分析 (`init_db.py`)**: 
    *   從 CWA API (F-A0010-001) 獲取台灣各區一週氣象預報 JSON 資料。
    *   分析並提取各區域的每日最高氣溫與最低氣溫。
    *   將清理後的資料存入 SQLite3 資料庫 (`data.db`) 中，以供後續查詢。
*   **Web App 視覺化 (`app.py`)**:
    *   基於 Streamlit 建立的網頁應用。
    *   使用者可透過下拉選單選擇「地區」，並在折線圖與表格中查看該地區一週氣溫變化。
    *   提供縮放地圖功能（Folium），根據選擇的日期，以圖像化標記顯示全台各區的氣溫分佈。

## 本地執行指南

1.  **安裝依賴套件**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **初始化資料庫 (獲取最新資料)**:
    ```bash
    python init_db.py
    ```
3.  **啟動 Web App**:
    ```bash
    streamlit run app.py
    ```

## 檔案結構
*   `init_db.py`: 處理 HW2-1 ~ HW2-3 的核心腳本。
*   `app.py`: 處理 HW2-4 的 Streamlit 前端與資料庫查詢腳本。
*   `requirements.txt`: Python 依賴清單。
*   `development_log.md`: 開發日誌記錄。
