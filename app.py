import streamlit as st
import pandas as pd
import os
from datetime import datetime, time

# --- CSS (Dark Mode & Professional Layout) ---
st.markdown("""
    <style>
    .stApp {background-color: #000000; color: #ff4b4b;}
    .ot-box {background: #1a1a1a; border: 2px solid #ff4b4b; padding: 15px; text-align: center; border-radius: 10px; margin: 10px 0;}
    .ot-text {font-size: 24px; font-weight: bold; color: #00ff00;}
    div.stButton > button {background-color: #ff4b4b; color: #000000; width: 100%; height: 50px; font-weight: bold;}
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Flash Attendance Pro")
user = st.text_input("Naam:")
chutti_time = st.time_input("Chutti ka Time Select Karein:")

if st.button("✅ Mark Attendance"):
    # Duty End 6:00 PM (18:00)
    duty_end = time(18, 0)
    # Convert input to comparable time
    if chutti_time > duty_end:
        # OT Calculation
        diff = (chutti_time.hour - duty_end.hour) + ((chutti_time.minute - duty_end.minute) / 60)
        ot = round(diff, 2)
    else:
        ot = 0.0
    
    # UI Output
    st.markdown(f'<div class="ot-box">Total OT: <span class="ot-text">{ot} Hours</span></div>', unsafe_allow_html=True)
    
    # Save Data
    df = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), user, chutti_time.strftime("%I:%M %p"), ot]],
                      columns=["Date", "Name", "Time", "OT"])
    
    if os.path.exists("attendance_data.csv"):
        df.to_csv("attendance_data.csv", mode='a', header=False, index=False)
    else:
        df.to_csv("attendance_data.csv", index=False)

# Table display
if st.checkbox("Mera Record Dekhein"):
    if os.path.exists("attendance_data.csv"):
        st.table(pd.read_csv("attendance_data.csv"))
