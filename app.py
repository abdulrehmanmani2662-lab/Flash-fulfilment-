import streamlit as st
import pandas as pd
import os
from datetime import datetime, time

# --- CSS STYLING (Dark/Red theme & Clean UI) ---
st.markdown("""
    <style>
    .stApp {background-color: #000000; color: #ff4b4b;}
    h1 {color: #ff4b4b !important; text-align: center; font-size: 28px;}
    .ot-display {background-color: #1a1a1a; color: #00ff00; font-size: 30px; font-weight: bold; text-align: center; padding: 20px; border-radius: 15px; border: 2px solid #ff4b4b; margin: 20px 0;}
    div.stButton > button {background-color: #ff4b4b; color: #000000; border: none; width: 100%; height: 50px; font-weight: bold; border-radius: 10px;}
    label {color: #ff4b4b !important; font-weight: bold;}
    </style>
""", unsafe_allow_html=True)

DB_FILE = "attendance_data.csv"
st.title("⚡ Flash Attendance Pro")

user = st.text_input("Apna Naam Likhein")

# 12-Hour format ke liye time input
chutti_time = st.time_input("Chutti ka Time Select Karein:")

# --- LOGIC ---
def calculate_ot(time_obj):
    # Duty End 6:00 PM (18:00)
    duty_end_hour = 18
    # Agar 6 baje se upar hai to hi OT
    if time_obj.hour >= duty_end_hour:
        ot_val = (time_obj.hour - duty_end_hour) + (time_obj.minute / 60)
        return round(ot_val, 2)
    return 0.0

# --- SAVE & DISPLAY ---
if st.button("✅ Mark Attendance"):
    if not user:
        st.error("Naam likho jani!")
    else:
        today = datetime.now().strftime("%Y-%m-%d")
        ot = calculate_ot(chutti_time)
        
        # Total OT Display (Beech mein big font)
        st.markdown(f'<div class="ot-display">Total OT: {ot} Hours</div>', unsafe_allow_html=True)
        
        # Save logic
        new_data = pd.DataFrame([[today, user, chutti_time.strftime("%I:%M %p"), ot]], 
                                columns=["Date", "Name", "Time", "OT"])
        if os.path.exists(DB_FILE):
            new_data.to_csv(DB_FILE, mode='a', header=False, index=False)
        else:
            new_data.to_csv(DB_FILE, mode='w', header=True, index=False)

# --- RECORD TABLE ---
if st.checkbox("Mera Record Dekhein"):
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        st.table(df[df['Name'] == user])
