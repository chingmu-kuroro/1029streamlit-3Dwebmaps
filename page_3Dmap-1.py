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
# 使用 pandas 的 DataFrame 功能建立一個名為 data 的表格狀資料結構
data = pd.DataFrame({
    # 定義 'lat' (緯度) 欄位：
    'lat': 25.0478 +        # 以 25.0478 (大約台北車站的緯度) 為基準點
           np.random.randn(1000) / 50,  # 加上 1000 個服從標準常態分佈 (均值0, 標準差1) 的隨機數。
                                        # np.random.randn(1000) 產生 1000 個這樣的數。
                                        # 除以 50 是為了縮小這些隨機數的範圍 (標準差變為 1/50)，使它們的值更接近 0。
                                        # 結果：產生 1000 個在 25.0478 附近隨機小幅波動的緯度值。

    # 定義 'lon' (經度) 欄位：
    'lon': 121.5170 +        # 以 121.5170 (大約台北車站的經度) 為基準點
           np.random.randn(1000) / 50,  # 加上另外 1000 個服從標準常態分佈的隨機數。
                                        # 同樣除以 50 以縮小隨機偏移的範圍。
                                        # 結果：產生 1000 個在 121.5170 附近隨機小幅波動的經度值。
})

# 小結：
# 這段程式碼創建了一個名為 `data` 的 pandas DataFrame。
# 這個 DataFrame 有 1000 列 (代表 1000 個點) 和 2 欄 ('lat', 'lon')。
# 這 1000 個點的座標是以台北車站 (25.0478, 121.5170) 為中心，
# 在其周圍進行常態分佈的隨機偏移，且偏移量不大，
# 因此這些點會密集地分佈在台北車站附近，用來模擬地理空間上的點資料群集。

# --- 2. 設定 Pydeck 圖層 (Layer) ---
layer = pdk.Layer(
    'HexagonLayer',          # 圖層類型：六角柱圖層
    data=data,               # 使用我們之前建立的 DataFrame 作為資料來源
    get_position='[lon, lat]', # 告訴 Pydeck 哪兩欄是經緯度
    radius=100,              # 每個六角形的半徑（單位：公尺）
    elevation_scale=4,       # 高度乘數：點越密集，柱子越高，這個值會放大高度差異
    elevation_range=[0, 1000],# 高度範圍限制（單位：公尺），柱子最高不會超過 1000 公尺
    pickable=True,           # 允許滑鼠懸停互動 (例如顯示 tooltip)
    extruded=True,           # ***核心：設為 True 才會產生 3D 的擠出效果（變成立體柱子）***
)

# --- 3. 設定攝影機視角 (View State) ---
view_state = pdk.ViewState(
    latitude=25.0478,     # 地圖初始中心點的緯度 (台北車站附近)
    longitude=121.5170,    # 地圖初始中心點的經度 (台北車站附近)
    zoom=12,              # 地圖初始縮放層級 (數值越大越近)
    pitch=50,             # ***核心：攝影機的傾斜角度 (0=俯視, 建議 45-60 來看 3D)***
)

# --- 4. 組合圖層和視角並顯示 ---
r = pdk.Deck(
    layers=[layer],                 # 要顯示在地圖上的圖層列表 (這裡只有一個 HexagonLayer)
    initial_view_state=view_state,  # 套用我們剛才設定的初始視角
    tooltip={"text": "這個區域有 {elevationValue} 個熱點"} # 設定滑鼠懸停時顯示的提示文字
)
# (後續會用 st.pydeck_chart(r) 將這個地圖物件顯示在 Streamlit 頁面上)