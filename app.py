import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- CUSTOM DESIGN BAASED ON YOUR PICTURE ---
st.markdown("""
    <style>
    /* Background and Headers */
    .stApp {background-color: #000000;}
    h1 {color: #ff4b4b !important; text-align: center; font-size: 45px; font-weight: 900; font-family: sans-serif;}
    
    /* Save Ot Button (Red Background, Yellow Text) */
    div.stButton > button {
        background-color: #ff4b4b !important; 
        color: #ffe600 !important; 
        width: 100%; 
        height: 60px; 
        font-size: 32px !important;
        font-weight: 900 !important; 
        border-radius: 12px;
        border: none;
    }
    
    /* Total OT Box at the bottom */
    .total-ot-box {
        background-color: #ff4b4b; 
        color: white; 
        font-size: 28px; 
        font-weight: 900; 
        text-align: center; 
        border-radius: 10px; 
        padding: 15px; 
        margin-top: 20px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    </style>
""", unsafe_allow_html=True)

# Top Heading
st.markdown("<h1>Attendance</h1>", unsafe_allow_html=True)

# Inputs
user = st.text_input("Apna Naam Likhein:")

# Time input with Watch Emoji to match your design
st.markdown("#### ⌚ Chutti ka Time:")
chutti_time = st.time_input("", label_visibility="collapsed")

# Save Ot Button
if st.button("Save Ot"):
    # OT Calculation (6 PM ke baad)
    duty_end_hour = 18 
    ot = 0.0
    if chutti_time.hour >= duty_end_hour:
        ot = (chutti_time.hour - duty_end_hour) + (chutti_time.minute / 60)
    
    # Save to CSV
    data = [[datetime.now().strftime("%Y-%m-%d"), user, chutti_time.strftime("%I:%M %p"), round(ot, 2)]]
    df = pd.DataFrame(data, columns=["Date", "Name", "Time", "OT"])
    
    if os.path.exists("attendance_data.csv"):
        df.to_csv("attendance_data.csv", mode='a', header=False, index=False)
    else:
        df.to_csv("attendance_data.csv", index=False)
        
    st.success("✅ Record Saved!")

# Table & Total OT Section
if st.checkbox("Mera Record", value=True):
    if os.path.exists("attendance_data.csv"):
        # Dark Table
        df_record = pd.read_csv("attendance_data.csv")
        st.dataframe(df_record, use_container_width=True)
        
        # Calculate Grand Total OT from the table
        total_ot_sum = df_record['OT'].sum()
        
        # TOTAL OT Bottom Box
        st.markdown(f'''
            <div class="total-ot-box">
                TOTAL OT: {round(total_ot_sum, 2)}
            </div>
        ''', unsafe_allow_html=True)
    else:
        st.info("Abhi tak koi record save nahi hua.")
