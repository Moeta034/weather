# 對話輸入紀錄 (Development Log)

## 階段一：API 測試與資料抓取 (HW2-1)
*   **目標**: 測試 CWA API 的連線與 JSON 資料獲取。
*   **過程**: 使用了提供的 API Key 進行連線，發現原始的預設 URL 無法取得開放資料平台上的特定 Dataset。經過調整後，使用 `opendataapi` 結點，並加上 `downloadType=WEB&format=JSON` 成功取得了 `F-A0010-001` 的 JSON 資料。為避免 SSL 驗證錯誤，加上了 `verify=False` 參數。
*   **結果**: 成功獲取一週農業氣象預報資料，並透過 `json.dumps()` 觀察資料結構，確認天氣資料放在 `['cwaopendata']['resources']['resource']['data']['agrWeatherForecasts']['weatherForecasts']['location']` 節點中。

## 階段二：資料清洗與萃取 (HW2-2)
*   **目標**: 解析 JSON，找出最高溫 (`MaxT`) 與最低溫 (`MinT`)。
*   **過程**: 撰寫迴圈歷遍所有地區（北部、中部、南部、東北部、東部、東南部），對應日期將 `temperature` 取出，並重組為易於存入資料庫的 List of Dictionaries 格式。
*   **結果**: 成功提取出各地區、每天的最高與最低溫度。

## 階段三：建置 SQLite 資料庫 (HW2-3)
*   **目標**: 將資料持久化至 `data.db` 的 `TemperatureForecasts` 表中。
*   **過程**: 建立 `sqlite3` 連線，設定欄位（包含 `id` 主鍵、`regionName`、`dataDate`、`mint`、`maxt`）。為避免重複插入資料，每次執行腳本前會先做 `DELETE FROM TemperatureForecasts`。
*   **結果**: 完成資料插入，並寫入測試 SQL 查詢指令驗證（`SELECT DISTINCT regionName...` 以及 `SELECT ... WHERE regionName='中部地區'`）。

## 階段四：Streamlit 網頁應用與地圖視覺化 (HW2-4)
*   **目標**: 打造使用者介面，支援下拉選單與圖表展示。
*   **過程**: 
    1.  設計基本架構，使用 `st.columns` 切分左右兩大區塊。
    2.  左側讀取 SQLite 資料庫，實現下拉選單選地區功能，並利用 `st.line_chart` 與 `st.dataframe` 展示該區域的一週氣溫趨勢。
    3.  右側實作互動式地圖，引入 `folium` 與 `streamlit-folium`，先定義各地區大約經緯度，並根據使用者在下拉選單選擇的時間（日期），動態產生所有地區在當天的氣溫標記。並根據均溫加上不同顏色的樣式以達到「圖像化」要求。
*   **結果**: 順利完成流暢的 Web App，完全符合 HW2 的所有作業需求。
    *   **Live Demo**: [點此查看 (Streamlit Cloud)](https://weather-unbfmmyjszbvdw7ufeo3ja.streamlit.app/)
