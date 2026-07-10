import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- PRO BOMB DESIGN (Dark Mode, Glow, Animation) ---
st.markdown("""
    <style>
    /* Base Dark Theme */
    .stApp { background-color: #0c0c0c; }
    
    /* Main Heading & Spinning Clock Animation */
    @keyframes spin { 100% { transform: rotate(360deg); } }
    .spin-clock {
        display: inline-block;
        animation: spin 3s linear infinite;
        font-size: 45px;
        margin-right: 15px;
        vertical-align: middle;
    }
    .main-heading {
        text-align: center;
        color: #ff3333;
        font-size: 50px;
        font-weight: 900;
        text-shadow: 0px 0px 15px #ff3333;
        margin-bottom: 25px;
        border-bottom: 2px solid #ff3333;
        padding-bottom: 10px;
    }

    /* Save OT Button Styling */
    div.stButton > button {
        background: linear-gradient(45deg, #ff3b3b, #cc0000) !important;
        color: #fff200 !important;
        width: 150px;
        height: 55px;
        font-size: 22px !important;
        font-weight: 900 !important;
        border-radius: 12px;
        border: 2px solid #ffaaaa;
        box-shadow: 0px 0px 15px #ff0000;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        box-shadow: 0px 0px 25px #ff0000;
        transform: scale(1.05);
        color: white !important;
    }

    /* Total OT Bottom Glowing Box */
    .total-ot-box {
        background: linear-gradient(90deg, #ff1a1a, #990000);
        color: white;
        font-size: 38px;
        font-weight: 900;
        text-align: center;
        border-radius: 15px;
        padding: 20px;
        margin-top: 30px;
        box-shadow: 0px 0px 25px #ff1a1a;
        border: 2px solid #ff4d4d;
        text-transform: uppercase;
        letter-spacing: 3px;
    }
    
    /* Input Labels */
    .stTextInput label, .stTimeInput label { 
        color: #ffcccc !important; 
        font-size: 18px !important; 
        font-weight: bold; 
    }
    </style>
""", unsafe_allow_html=True)

# Animated Heading with Spinning Clock
st.markdown("<div class='main-heading'><span class='spin-clock'>🕐</span> Attendance</div>", unsafe_allow_html=True)

# Inputs
user = st.text_input("Apna Naam Likhein:")
chutti_time = st.time_input("Chutti ka Time:")

# Save Ot Button
if st.button("Save Ot"):
    if user.strip() == "":
        st.error("⚠️ Pehle apna naam likhein!")
    else:
        # OT Calculation (6 PM yaani 18:00 ke baad count hoga)
        duty_end_hour = 18 
        ot = 0.0
        
        # Agar chutti ka time 6 PM ya uske baad ka hai tabhi OT milega
        if chutti_time.hour >= duty_end_hour:
            ot = (chutti_time.hour - duty_end_hour) + (chutti_time.minute / 60)
        
        # Save to CSV
        data = [[datetime.now().strftime("%Y-%m-%d"), user, chutti_time.strftime("%I:%M %p"), round(ot, 2)]]
        df = pd.DataFrame(data, columns=["Date", "Name", "Time", "OT"])
        
        if os.path.exists("attendance_data.csv"):
            df.to_csv("attendance_data.csv", mode='a', header=False, index=False)
        else:
            df.to_csv("attendance_data.csv", index=False)
            
        st.success("✅ Record Saved Successfully!")

# Table & Total OT Section
if st.checkbox("Mera Record", value=True):
    if os.path.exists("attendance_data.csv"):
        df_record = pd.read_csv("attendance_data.csv")
        
        # Table show karana (hide_index=True se wo extra 0,1,2 wale number gayab ho jayenge)
        st.dataframe(df_record, use_container_width=True, hide_index=True)
        
        # Calculate Grand Total OT
        total_ot_sum = df_record['OT'].sum()
        
        # TOTAL OT Bottom Box
        st.markdown(f'''
            <div class="total-ot-box">
                TOTAL OT: {round(total_ot_sum, 2)}
            </div>
        ''', unsafe_allow_html=True)
    else:
        st.info("Abhi tak koi record save nahi hua.")
