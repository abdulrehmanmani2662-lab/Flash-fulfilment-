import streamlit as st
import pandas as pd
import os
from datetime import datetime, time, timedelta

# --- DARK/RED STYLE ---
st.markdown("""
    <style>
    .stApp {background-color: #000000; color: #ff4b4b;}
    h1 {color: #ff4b4b !important; text-align: center;}
    div.stButton > button {background-color: #1a1a1a; color: #ff4b4b; border: 2px solid #ff4b4b; font-weight: bold;}
    </style>
""", unsafe_allow_html=True)

DB_FILE = "attendance_data.csv"
st.title("⚡ Flash Attendance Pro")

user = st.text_input("Apna Naam Likhein")

# --- AUTO OT CALCULATOR ---
# Time picker jahan user apni chutti ka time select karega
chutti_time = st.time_input("Chutti ka Time Select Karein (e.g., 07:00 PM)", time(18, 0))

def calculate_ot(end_time):
    duty_end = time(18, 0) # 6 PM fix time
    if end_time > duty_end:
        # OT calculation logic
        dummy_date = datetime.today()
        end_dt = datetime.combine(dummy_date, end_time)
        duty_dt = datetime.combine(dummy_date, duty_end)
        diff = end_dt - duty_dt
        return round(diff.total_seconds() / 3600, 2)
    return 0.0

# --- DATA SAVING ---
if st.button("✅ Mark Attendance & Save OT"):
    if not user:
        st.error("Jani, Naam to likho!")
    else:
        ot_hours = calculate_ot(chutti_time)
        
        # Data structure
        new_entry = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), user, chutti_time.strftime("%H:%M"), ot_hours]], 
                                 columns=["Date", "Name", "Chutti_Time", "OT_Hours"])
        
        if os.path.exists(DB_FILE):
            new_entry.to_csv(DB_FILE, mode='a', header=False, index=False)
        else:
            new_entry.to_csv(DB_FILE, mode='w', header=True, index=False)
            
        st.success(f"Done! Aaj ka OT: {ot_hours} hours")

# --- REPORT VIEW ---
if st.checkbox("Mera Record Dekhein"):
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        st.table(df[df['Name'] == user])
