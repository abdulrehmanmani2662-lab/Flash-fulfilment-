import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- UI STYLE (Full Black & Red) ---
st.markdown("""
    <style>
    .stApp {background-color: #000000; color: #ff4b4b;}
    h1 {color: #ff4b4b !important; text-align: center;}
    .ot-box {background: #1a1a1a; border: 2px solid #ff4b4b; padding: 20px; text-align: center; font-size: 24px; color: #00ff00; border-radius: 10px; margin: 20px 0;}
    div.stButton > button {background-color: #ff4b4b; color: #000000; width: 100%; font-weight: bold;}
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Flash Attendance")
user = st.text_input("Apna Naam:")
chutti_time = st.time_input("Chutti ka Time:")

if st.button("✅ Mark Attendance"):
    # Logic: 6:00 PM (18:00) ke baad OT shuru
    duty_end_hour = 18
    selected_hour = chutti_time.hour
    
    # OT Calculation
    ot = 0.0
    if selected_hour >= duty_end_hour:
        ot = (selected_hour - duty_end_hour) + (chutti_time.minute / 60)
    
    # Total OT show karo
    st.markdown(f'<div class="ot-box">Total OT: {round(ot, 2)} Hours</div>', unsafe_allow_html=True)
    
    # Save Data
    df = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), user, chutti_time.strftime("%I:%M %p"), round(ot, 2)]],
                      columns=["Date", "Name", "Time", "OT"])
    
    if os.path.exists("attendance_data.csv"):
        df.to_csv("attendance_data.csv", mode='a', header=False, index=False)
    else:
        df.to_csv("attendance_data.csv", index=False)
