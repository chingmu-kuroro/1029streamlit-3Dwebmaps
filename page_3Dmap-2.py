import streamlit as st
import plotly.express as px
import pandas as pd

st.title("Plotly 3D 地圖 (向量 - 地球儀)")

# --- 1. 載入 Plotly 內建的範例資料 ---
df = px.data.gapminder().query("year == 2007")

# --- 2. 建立 3D 地理散點圖 (scatter_geo) ---
fig = px.scatter_geo(
    df,
    locations="iso_alpha",  # 國家代碼
    color="continent",      # 依據洲別上色
    hover_name="country",   # 滑鼠懸停時顯示國家名稱
    size="pop",             # 點的大小代表人
    
    # *** 關鍵：使用 "orthographic" 投影法來建立 3D 地球儀 ***
    projection="orthographic"
)

# --- 3. 在 Streamlit 中顯示 ---
st.plotly_chart(fig, use_container_width=True)