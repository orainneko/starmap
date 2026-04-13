# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 14:43:22 2026

@author: USER
"""

import streamlit as st
import pandas as pd
import base64
import tomllib as toml
import matplotlib.pyplot as plt
import os
import datetime

#sys.path.append(os.path.dirname(__file__))
from starmap_main import get_star_recommendations, draw_compass

# ----------------------
# 初始化 session
# ----------------------
if "results" not in st.session_state:
    st.session_state.results = None

if "condition" not in st.session_state:
    st.session_state.condition = None

# ----------------------
# Config
# ----------------------
toml_path = os.path.join(os.path.dirname(__file__), "config.toml")
with open(toml_path, "rb") as f:
    config = toml.load(f)

# ----------------------
# Sidebar
# ----------------------
with st.sidebar:
    st.header("🔭 觀測設定")

    now = datetime.datetime.now()

    date = st.date_input("日期", value=now.date())
    time = st.time_input("時間", value=now.time())
    dt = datetime.datetime.combine(date, time)

    st.subheader("📍 地點")
    country = st.text_input("國家", value=config["default"]["country"])
    city = st.text_input("縣市", value=config["default"]["city"])
    district = st.text_input("區", value=config["default"]["district"])

    go_clicked = st.button("🔥開始觀測🔥")

    # GIF
    file_path = os.path.join(os.path.dirname(__file__), "gif", "mogu.gif")
    with open(file_path, "rb") as file_:
        contents = file_.read()

    data_url = base64.b64encode(contents).decode("utf-8")
    st.markdown(
        f"""
        <div style="text-align: right;">
            <img src="data:image/gif;base64,{data_url}" width="100">
        </div>
        """,
        unsafe_allow_html=True
    )

# ----------------------
# Title
# ----------------------
st.markdown(f"<h2 style='text-align: center;'>{config['app']['title']}</h2>", unsafe_allow_html=True)

# ----------------------
# 按鈕觸發
# ----------------------
hint_box = st.empty()
hint_box.info("點擊左上角的按鈕輸入觀測資訊，開始尋找適合觀測的星體！")
if go_clicked:
    hint_box.empty()
    address = f"{country} {city} {district}"
    t = dt.strftime("%Y-%m-%d %H:%M:%S")

    with st.spinner("正在計算星體位置..."):
        results, condition = get_star_recommendations(None, address, t)

    st.session_state.results = results
    st.session_state.condition = condition

    st.success("計算完成！")

# ----------------------
# 顯示結果（不依賴按鈕）
# ----------------------
if st.session_state.condition is False:
    st.error("找不到該地點，請重新輸入。")

elif st.session_state.results is not None:

    results = st.session_state.results

    st.subheader("📍 觀測資訊")
    st.write(f"時間：{dt}")
    st.write(f"地點：{country} {city} {district}")

    st.divider()

    # ----------------------
    # 卡片式星體
    # ----------------------
    st.subheader("✨ 推薦觀測星體")

    cols = st.columns(3)
    star_names = []

    for i, (_, row) in enumerate(results.iterrows()):
        name = row['proper'] if pd.notna(row['proper']) else f"HR {row['HR']}"
        star_names.append(name)

        with cols[i]:
            st.markdown(f"### 🌟 第 {i+1} 名")
            st.metric("名稱", name)
            st.metric("亮度", f"{row['Vmag']:.2f}")
            st.metric("仰角", f"{row['altitude']:.1f}°")
            st.metric("方位", f"{row['azimuth']:.1f}°")

    st.divider()

    # ----------------------
    # 天空分布圖（視覺化🔥）
    # ----------------------
    st.subheader("🌌 天空位置分布")

    fig, ax = plt.subplots()
    ax.scatter(results['azimuth'], results['altitude'])

    for i, row in results.iterrows():
        name = row['proper'] if pd.notna(row['proper']) else f"HR {row['HR']}"
        ax.text(row['azimuth'], row['altitude'], name)

    ax.set_xlabel("Azimuth")
    ax.set_ylabel("Altitude")
    ax.set_title("Star position")

    st.pyplot(fig)

    st.divider()

    # ----------------------
    # 選星 + 羅盤
    # ----------------------
    st.subheader("🧭 觀測方向指引")

    selected = st.selectbox("選擇星體", star_names)

    selected_row = results.iloc[star_names.index(selected)]

    fig2 = draw_compass(selected_row['azimuth'])
    st.pyplot(fig2)
     
    