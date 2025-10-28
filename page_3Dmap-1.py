# 顯示台北市某個區域的 1000 個 GPS 點(例如 iRent 熱點)的「3D 密度」。
# HexagonLayer (六角柱圖層) 是這個情境的完美選擇。

import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

st.title("Pydeck 3D 地圖 (向量 - 密度圖)")

# 0. 檢查 Mapbox 金鑰是否存在於 Secrets 中 (名稱應為 MAPBOX_API_KEY)
#    注意：我們不再需要將它讀取到 Python 變數中，
#    因為 st.secrets 會自動將其設為環境變數，pydeck 會自己去讀。
if "MAPBOX_API_KEY" not in st.secrets: # <-- 檢查大寫的 Secret 名稱
    st.error("Mapbox API Key (名稱需為 MAPBOX_API_KEY) 未設定！請在雲端 Secrets 中設定。")
    st.stop() # 如果沒有金鑰，停止執行

# --- 1. 生成範例資料 (向量) ---
data = pd.DataFrame({
    'lat': 25.0478 + np.random.randn(1000) / 50,
    'lon': 121.5170 + np.random.randn(1000) / 50,
})

# --- 2. 設定 Pydeck 圖層 (Layer) ---
layer = pdk.Layer(
    'HexagonLayer',
    data=data,
    get_position='[lon, lat]',
    radius=100,
    elevation_scale=4,
    elevation_range=[0, 1000],
    pickable=True,
    extruded=True,
)

# --- 3. 設定攝影機視角 (View State) ---
view_state = pdk.ViewState(
    latitude=25.0478,
    longitude=121.5170,
    zoom=12,
    pitch=50,
)

# --- 4. 組合圖層和視角並顯示 ---
# 【修正點】移除 mapbox_key 參數
r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    # mapbox_key=MAPBOX_KEY, # <-- 移除這一行
    tooltip={"text": "這個區域有 {elevationValue} 個熱點"}
)
st.pydeck_chart(r)