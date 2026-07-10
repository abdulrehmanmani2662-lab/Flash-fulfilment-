import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- FULL PRO DESIGN (Black/Red/Highlight) ---
st.markdown("""
    <style>
    .stApp {background-color: #000000;}
    h1 {color: #ff4b4b !important; text-align: center; border-bottom: 2px solid #ff4b4b; padding-bottom: 10px;}
    .input-box {background: #1a1a1a; padding: 15px; border-radius: 10px; border: 1px solid #333;}
    .ot-box {background: #000000; border: 2px solid #ff4b4b; padding: 20px; text-align: center; border-radius: 15px; margin: 20px 0; box-shadow: 0px 0px 10px #ff4b4b;}
    .ot-val {font-size: 32px; font-weight: bold; color: #00ff00;}
    div.stButton > button {background-color: #ff4b4b; color: #000000; width: 100%; height: 50px; font-weight: bold; border-radius: 8px;}
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Flash Attendance")

# Inputs
user = st.text_input("Apna Naam Likhein:")
chutti_time = st.time_input("Chutti ka Time:")

if st.button("✅ Mark Attendance"):
    # 1. Khali Naam ki Warning
    if user.strip() == "":
        st.warning("⚠️ Please apna naam zaroor likhein!")
    else:
        # OT Calculation
        duty_end_hour = 18 # 6 PM
        ot = 0.0
        if chutti_time.hour >= duty_end_hour:
            ot = (chutti_time.hour - duty_end_hour) + (chutti_time.minute / 60)
        
        # Highlighted Display Box
        st.markdown(f'''
            <div class="ot-box">
                Total OT<br>
                <span class="ot-val">{round(ot, 2)} Hours</span>
            </div>
        ''', unsafe_allow_html=True)
        
        # Save to CSV
        data = [[datetime.now().strftime("%Y-%m-%d"), user, chutti_time.strftime("%I:%M %p"), round(ot, 2)]]
        df = pd.DataFrame(data, columns=["Date", "Name", "Time", "OT"])
        
        if os.path.exists("attendance_data.csv"):
            df.to_csv("attendance_data.csv", mode='a', header=False, index=False)
        else:
            df.to_csv("attendance_data.csv", index=False)
            
        st.success("✅ Attendance lag gayi!")

# Table & Download Section
if st.checkbox("Mera Record"):
    if os.path.exists("attendance_data.csv"):
        # Data read karna
        df_record = pd.read_csv("attendance_data.csv")
        st.table(df_record)
        
        # 2. Data Download karne ka Button
        csv = df_record.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Record Download Karein",
            data=csv,
            file_name='attendance_data.csv',
            mime='text/csv',
        )
    else:
        st.info("Abhi tak koi record save nahi hua.")
