import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- DARK/RED STYLE (Full Professional) ---
st.markdown("""
    <style>
    .stApp {background-color: #000000; color: #ff4b4b;}
    h1 {color: #ff4b4b !important; text-align: center; font-size: 24px;}
    div.stButton > button {background-color: #1a1a1a; color: #ff4b4b; border: 2px solid #ff4b4b; width: 100%; border-radius: 10px;}
    .stTimeInput label {color: #ff4b4b !important;}
    </style>
""", unsafe_allow_html=True)

DB_FILE = "attendance_data.csv"
st.title("⚡ Flash Attendance Pro")

user = st.text_input("Apna Naam Likhein")

# --- TIME INPUT (12-Hour format fix) ---
# Streamlit ka time_input automatically AM/PM dikhata hai agar browser language English ho
chutti_time = st.time_input("Chutti ka Time Select Karein:")

# --- LOGIC ---
def get_ot(time_obj):
    # Duty End 6:00 PM (18:00)
    duty_end_hour = 18
    if time_obj.hour >= duty_end_hour:
        ot_val = (time_obj.hour - duty_end_hour) + (time_obj.minute / 60)
        return round(ot_val, 2)
    return 0.0

# --- SAVE LOGIC ---
if st.button("✅ Mark Attendance & Save OT"):
    if not user:
        st.error("Naam to likho jani!")
    else:
        # Check double entry
        today = datetime.now().strftime("%Y-%m-%d")
        if os.path.exists(DB_FILE):
            df_check = pd.read_csv(DB_FILE)
            if not df_check[(df_check['Name'] == user) & (df_check['Date'] == today)].empty:
                st.warning("Jani, aaj ki entry pehle ho chuki ha!")
            else:
                ot = get_ot(chutti_time)
                new_data = pd.DataFrame([[today, user, chutti_time.strftime("%I:%M %p"), ot]], 
                                        columns=["Date", "Name", "Chutti_Time", "OT_Hours"])
                new_data.to_csv(DB_FILE, mode='a', header=not os.path.exists(DB_FILE), index=False)
                st.success(f"Done! Aaj ka OT: {ot} hours")
        else:
            # First time save
            ot = get_ot(chutti_time)
            pd.DataFrame([[today, user, chutti_time.strftime("%I:%M %p"), ot]], 
                         columns=["Date", "Name", "Chutti_Time", "OT_Hours"]).to_csv(DB_FILE, index=False)
            st.success("Done!")

# --- RECORD TABLE ---
if st.checkbox("Mera Record Dekhein"):
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        st.table(df[df['Name'] == user])
