import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. Data Save karne ke liye File (Database ki tarah)
DB_FILE = "attendance_data.csv"

# 2. Page Design
st.set_page_config(page_title="Flash Attendance", layout="centered")
st.title("Flash Attendance System")

# 3. User Login (Basic)
user = st.text_input("Apna Naam Likhein")

# 4. Buttons (Green/Red logic)
col1, col2, col3 = st.columns(3)

def save_data(name, status, ot=0):
    df = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d %H:%M"), name, status, ot]], 
                      columns=["Time", "Name", "Status", "OT_Hours"])
    if os.path.exists(DB_FILE):
        df.to_csv(DB_FILE, mode='a', header=False, index=False)
    else:
        df.to_csv(DB_FILE, mode='w', header=True, index=False)
    st.success("Save hogya!")

with col1:
    if st.button("✅ Present"):
        save_data(user, "Present")
with col2:
    ot_val = st.number_input("OT Hours", min_value=0.0)
    if st.button("🚀 Submit OT"):
        save_data(user, "OT", ot_val)
with col3:
    if st.button("❌ Chuti"):
        save_data(user, "Chuti")

# 5. Report (Table view)
if st.checkbox("Mera Record Dekhein"):
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        my_data = df[df['Name'] == user]
        st.table(my_data)
