import streamlit as st
import sqlite3
import pandas as pd
import folium
import os
from streamlit_folium import st_folium
from init_db import init_db

# 座標對應 (大致中心點)
REGION_COORDS = {
    "北部地區": [25.0330, 121.5654], # 台北
    "中部地區": [24.1477, 120.6736], # 台中
    "南部地區": [22.9997, 120.2270], # 台南
    "東北部地區": [24.7523, 121.7516], # 宜蘭
    "東部地區": [23.9872, 121.6016], # 花蓮
    "東南部地區": [22.7972, 121.1219] # 台東
}

def load_data(region_name=None):
    conn = sqlite3.connect('data.db')
    if region_name:
        query = f"SELECT dataDate, mint, maxt FROM TemperatureForecasts WHERE regionName = '{region_name}'"
        df = pd.read_sql_query(query, conn)
    else:
        query = "SELECT * FROM TemperatureForecasts"
        df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def main():
    st.set_page_config(page_title="HW2 氣溫預報 Web App", layout="wide")
    st.title("氣溫預報 Web App (使用 CWA API)")
    
    # 若資料庫不存在，自動從 CWA API 獲取資料並建立資料庫
    if not os.path.exists('data.db'):
        with st.spinner("首次啟動，正在從 CWA API 獲取資料..."):
            init_db()
    
    # 提供手動重新抓取按鈕
    if st.sidebar.button("🔄 重新抓取最新資料"):
        init_db()
        st.rerun()
    
    # 載入資料庫中的所有地區資料
    all_data = load_data()
    if all_data.empty:
        st.error("資料庫中沒有資料，請先執行 init_db.py")
        return
        
    regions = all_data['regionName'].unique()
    dates = all_data['dataDate'].unique()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1. 地區一週氣溫預報")
        selected_region = st.selectbox("請選擇地區", regions)
        
        region_df = load_data(selected_region)
        
        # 繪製折線圖
        # 將資料轉換為 Streamlit line_chart 支援的格式
        chart_data = region_df.set_index('dataDate')[['mint', 'maxt']]
        chart_data.columns = ['最低氣溫 (MinT)', '最高氣溫 (MaxT)']
        st.line_chart(chart_data)
        
        # 顯示表格
        st.write(f"**{selected_region}** 氣溫資料表：")
        st.dataframe(region_df.rename(columns={'dataDate': '日期', 'mint': '最低氣溫', 'maxt': '最高氣溫'}), width='stretch')

    with col2:
        st.subheader("2. 各地氣溫地圖圖像化")
        selected_date = st.selectbox("請選擇時間", dates)
        
        # 篩選所選日期的所有地區資料
        date_df = all_data[all_data['dataDate'] == selected_date]
        
        # 建立可縮放地圖 (Folium)
        m = folium.Map(location=[23.6978, 120.9605], zoom_start=7, tiles="CartoDB positron")
        
        for _, row in date_df.iterrows():
            reg = row['regionName']
            if reg in REGION_COORDS:
                mint = row['mint']
                maxt = row['maxt']
                avg_temp = (mint + maxt) / 2
                
                # 根據溫度決定顏色
                if avg_temp < 20:
                    color = 'blue'
                elif avg_temp < 28:
                    color = 'green'
                else:
                    color = 'red'
                    
                popup_text = f"<b>{reg}</b><br>最低溫: {mint}°C<br>最高溫: {maxt}°C"
                
                folium.CircleMarker(
                    location=REGION_COORDS[reg],
                    radius=15,
                    popup=folium.Popup(popup_text, max_width=200),
                    tooltip=f"{reg}: {mint}°C ~ {maxt}°C",
                    color=color,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.7
                ).add_to(m)
                
                # 加上文字標籤
                folium.Marker(
                    location=REGION_COORDS[reg],
                    icon=folium.DivIcon(
                        icon_size=(150,36),
                        icon_anchor=(0,0),
                        html=f'<div style="font-size: 10pt; font-weight: bold; color: black; text-shadow: 1px 1px 2px white;">{reg}<br>{maxt}°C / {mint}°C</div>',
                    )
                ).add_to(m)

        st_folium(m, width=600, height=500)

if __name__ == '__main__':
    main()
