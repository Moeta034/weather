"""
init_db.py
HW2-1 ~ HW2-3：從 CWA API 獲取天氣預報資料，分析並存入 SQLite3 資料庫。
"""

import requests
import json
import sqlite3

# CWA API 設定
API_KEY = "CWA-23EE6383-F70B-421C-BEEE-3F6D6F3DB674"
API_URL = (
    f"https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-A0010-001"
    f"?Authorization={API_KEY}&downloadType=WEB&format=JSON"
)

def init_db():
    # =========================================================
    # HW2-1: 獲取天氣預報資料
    # =========================================================
    print("=== HW2-1: 獲取天氣預報資料 ===")

    # 使用 Requests 套件調用 CWA API
    requests.packages.urllib3.disable_warnings()
    response = requests.get(API_URL, verify=False)
    data = response.json()

    # 使用 json.dumps 觀察獲得的資料（部分）
    print("Raw Data (weatherElements Subset):")
    print(json.dumps(
        data['cwaopendata']['resources']['resource']['metadata']['weatherElements'],
        indent=2, ensure_ascii=False
    ))

    # =========================================================
    # HW2-2: 分析資料，提取最高與最低氣溫的資料
    # =========================================================
    print("\n=== HW2-2: 分析資料，提取最高與最低氣溫的資料 ===")

    # 資料路徑：cwaopendata > resources > resource > data >
    #           agrWeatherForecasts > weatherForecasts > location
    locations = (
        data['cwaopendata']['resources']['resource']
            ['data']['agrWeatherForecasts']['weatherForecasts']['location']
    )

    extracted_data = []
    for loc in locations:
        region_name = loc['locationName']
        max_t_daily = loc['weatherElements']['MaxT']['daily']
        min_t_daily = loc['weatherElements']['MinT']['daily']

        for i in range(len(max_t_daily)):
            data_date = max_t_daily[i]['dataDate']
            maxt      = max_t_daily[i]['temperature']
            mint      = min_t_daily[i]['temperature']
            extracted_data.append({
                "regionName": region_name,
                "dataDate":   data_date,
                "mint":       mint,
                "maxt":       maxt
            })

    # 使用 json.dumps 觀察提取的資料（前 3 筆）
    print("Extracted Data (Subset):")
    print(json.dumps(extracted_data[:3], indent=2, ensure_ascii=False))

    # =========================================================
    # HW2-3: 將氣溫資料儲存到 SQLite3 資料庫
    # =========================================================
    print("\n=== HW2-3: 將氣溫資料儲存到 SQLite3 資料庫 ===")

    conn   = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # 建立資料表（若不存在）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS TemperatureForecasts (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            regionName TEXT,
            dataDate   TEXT,
            mint       INTEGER,
            maxt       INTEGER
        )
    ''')

    # 清除舊資料後重新寫入，確保資料是最新的
    cursor.execute('DELETE FROM TemperatureForecasts')

    for item in extracted_data:
        cursor.execute('''
            INSERT INTO TemperatureForecasts (regionName, dataDate, mint, maxt)
            VALUES (?, ?, ?, ?)
        ''', (item['regionName'], item['dataDate'],
              int(item['mint']), int(item['maxt'])))

    conn.commit()
    print("資料庫儲存完成。")

    # 查詢驗證 1：列出所有地區名稱
    print("\n列出所有地區名稱:")
    cursor.execute('SELECT DISTINCT regionName FROM TemperatureForecasts')
    for (name,) in cursor.fetchall():
        print(f"  {name}")

    # 查詢驗證 2：列出中部地區的氣溫資料
    print("\n列出中部地區的氣溫資料:")
    cursor.execute(
        'SELECT dataDate, mint, maxt FROM TemperatureForecasts WHERE regionName = ?',
        ('中部地區',)
    )
    for row in cursor.fetchall():
        print(f"  日期: {row[0]}, 最低溫: {row[1]}°C, 最高溫: {row[2]}°C")

    conn.close()


if __name__ == '__main__':
    init_db()
