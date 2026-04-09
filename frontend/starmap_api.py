# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 14:43:22 2026

@author: USER
"""

import streamlit as st
import pandas as pd
import base64
import tomllib as toml
import os

#from backend.py import get_star_position

toml_path = os.path.join(os.path.dirname(__file__),"config.toml")
with open(toml_path, "rb") as f:
    config = toml.load(f)

# My first app
st.markdown(f"""
            
            <h3 style='text-align: center;'>{config["app"]["title"]}</h3>
            
            """, unsafe_allow_html=True)

##
ct = st.container()
with ct:
    ct.divider()

    ct.write("選擇觀測**時間** (24小時制)")
    col1_1, col1_2 = ct.columns([1,1])  # 分2個欄位

    with col1_1:
        hr = ct.selectbox("時", range(24),index=config["default"]["hour"])
    
    with col1_2:
        mins = ct.selectbox("分", range(61),index=config["default"]["minute"])
##

##
ct2 = st.container()
with ct2:
    ct2.divider()
    ct2.write("選擇觀測**地點**")
    loca = [ct2.text_input("國家",value=config["default"]["country"]),
            ct2.text_input("縣市",value=config["default"]["city"]),
            ct2.text_input("鄉鎮市區",value=config["default"]["district"]),
            ct2.text_input("其他(選填)",value=config["default"]["option"])]
    ct2.divider()
##

##
placeholder = st.empty()

go_clicked = st.button("GO!")

if go_clicked:
    with placeholder.container():
        st.subheader("結果:")
        st.write("我啥都還沒開始寫，但我可以告訴你你輸入了", hr,"點", mins,"分")
        st.write(loca[0], loca[1], loca[2],loca[3])
        st.divider()
        st.subheader("建議最佳地點一覽:")
        st.write("google map")
        st.divider()
   
##
 
##
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
    unsafe_allow_html=True)
##
