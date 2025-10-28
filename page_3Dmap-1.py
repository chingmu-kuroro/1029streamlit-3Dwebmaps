# 顯示台北市某個區域的 1000 個 GPS 點(例如 iRent 熱點)的「3D 密度」。
# HexagonLayer (六角柱圖層) 是這個情境的完美選擇。

import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

st.title("Pydeck 3D 地圖 (向量 - 密度圖)")

# 0. 檢查並讀取 Mapbox 金鑰
if "mapbox_api_key" not in st.secrets:
    st.error("Mapbox API Key 未設定！請在雲端 Secrets 中設定。")
else:
    MAPBOX_KEY = st.secrets["mapbox_api_key"]

    # --- 1. 生成範例資料 (向量) ---
    # 在台北車站 (25.04, 121.51) 附近生成 1000 個隨機點
    data = pd.DataFrame({
        'lat': 25.0478 + np.random.randn(1000) / 50,  # 緯度
        'lon': 121.5170 + np.random.randn(1000) / 50, # 經度
    })

    # --- 2. 設定 Pydeck 圖層 (Layer) ---
    layer = pdk.Layer(
        'HexagonLayer',
        data=data,
        get_position='[lon, lat]',
        radius=100,         # 每個六角形的半徑 (公尺)
        elevation_scale=4,  # 高度乘數
        elevation_range=[0, 1000], # 高度範圍 (公尺)
        pickable=True,      # 允許滑鼠懸停
        extruded=True,      # *** 關鍵：設為 True 以啟用 3D 擠出 ***
    )

    # --- 3. 設定攝影機視角 (View State) ---
    view_state = pdk.ViewState(
        latitude=25.0478,
        longitude=121.5170,
        zoom=12,
        pitch=50,  # *** 關鍵：設定傾斜角度 (0-60度) 來觀看 3D ***
    )

    # --- 4. 組合圖層和視角並顯示 ---
    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        mapbox_key=MAPBOX_KEY,
        tooltip={"text": "這個區域有 {elevationValue} 個熱點"}
    )
    st.pydeck_chart(r)