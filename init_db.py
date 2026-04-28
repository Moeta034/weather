import requests
import json
import sqlite3
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def init_db():
    print("=== HW2-1: 獲取天氣預報資料 ===")
    url = "https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-A0010-001?Authorization=CWA-23EE6383-F70B-421C-BEEE-3F6D6F3DB674&downloadType=WEB&format=JSON"
    requests.packages.urllib3.disable_warnings()
    response = requests.get(url, verify=False)
    data = response.json()
    
    print("Raw Data (Subset):")
    print(json.dumps(data['cwaopendata']['resources']['resource']['metadata']['weatherElements'], indent=2, ensure_ascii=False))

    print("\n=== HW2-2: 分析資料，提取最高與最低氣溫的資料 ===")
    locations = data['cwaopendata']['resources']['resource']['data']['agrWeatherForecasts']['weatherForecasts']['location']
    
    extracted_data = []
    for loc in locations:
        region_name = loc['locationName']
        max_t_daily = loc['weatherElements']['MaxT']['daily']
        min_t_daily = loc['weatherElements']['MinT']['daily']
        
        for i in range(len(max_t_daily)):
            data_date = max_t_daily[i]['dataDate']
            maxt = max_t_daily[i]['temperature']
            mint = min_t_daily[i]['temperature']
            extracted_data.append({
                "regionName": region_name,
                "dataDate": data_date,
                "mint": mint,
                "maxt": maxt
            })
    
    print("Extracted Data (Subset):")
    print(json.dumps(extracted_data[:3], indent=2, ensure_ascii=False))

    print("\n=== HW2-3: 將氣溫資料儲存到 SQLite3 資料庫 ===")
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS TemperatureForecasts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            regionName TEXT,
            dataDate TEXT,
            mint INTEGER,
            maxt INTEGER
        )
    ''')
    
    cursor.execute('DELETE FROM TemperatureForecasts')
    
    for item in extracted_data:
        cursor.execute('''
            INSERT INTO TemperatureForecasts (regionName, dataDate, mint, maxt)
            VALUES (?, ?, ?, ?)
        ''', (item['regionName'], item['dataDate'], int(item['mint']), int(item['maxt'])))
    
    conn.commit()
    print("資料庫儲存完成。")
    
    print("\n列出所有地區名稱:")
    cursor.execute('SELECT DISTINCT regionName FROM TemperatureForecasts')
    regions = cursor.fetchall()
    for r in regions:
        print(r[0])
        
    print("\n列出中部地區的氣溫資料:")
    cursor.execute('SELECT dataDate, mint, maxt FROM TemperatureForecasts WHERE regionName = ?', ('中部地區',))
    central_data = cursor.fetchall()
    for row in central_data:
        print(f"日期: {row[0]}, 最低溫: {row[1]}°C, 最高溫: {row[2]}°C")
        
    conn.close()

if __name__ == '__main__':
    init_db()
