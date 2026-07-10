import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client, Client
import os

# --- DATABASE SETUP (Supabase) ---
# Ye link aur key aapko Render ki settings mein daalni hogi
SUPABASE_URL = os.environ.get("SUPABASE_URL", "YAHAN_APNA_URL_AYEGA")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "YAHAN_APNI_KEY_AYEGI")

# Database se connect karna
@st.cache_resource
def init_connection():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

# Agar URL aur Key mojood hain tabhi connect kare
if SUPABASE_URL != "YAHAN_APNA_URL_AYEGA":
    supabase: Client = init_connection()

# --- PRO BOMB DESIGN (Dark Mode, Glow, Animation) ---
st.markdown("""
    <style>
    .stApp { background-color: #0c0c0c; }
    @keyframes spin { 100% { transform: rotate(360deg); } }
    .spin-clock { display: inline-block; animation: spin 3s linear infinite; font-size: 45px; margin-right: 15px; vertical-align: middle; }
    .main-heading { text-align: center; color: #ff3333; font-size: 50px; font-weight: 900; text-shadow: 0px 0px 15px #ff3333; margin-bottom: 25px; border-bottom: 2px solid #ff3333; padding-bottom: 10px; }
    div.stButton > button { background: linear-gradient(45deg, #ff3b3b, #cc0000) !important; color: #fff200 !important; width: 150px; height: 55px; font-size: 22px !important; font-weight: 900 !important; border-radius: 12px; border: 2px solid #ffaaaa; box-shadow: 0px 0px 15px #ff0000; transition: 0.3s; }
    div.stButton > button:hover { box-shadow: 0px 0px 25px #ff0000; transform: scale(1.05); color: white !important; }
    .total-ot-box { background: linear-gradient(90deg, #ff1a1a, #990000); color: white; font-size: 38px; font-weight: 900; text-align: center; border-radius: 15px; padding: 20px; margin-top: 30px; box-shadow: 0px 0px 25px #ff1a1a; border: 2px solid #ff4d4d; text-transform: uppercase; letter-spacing: 3px; }
    .stTextInput label, .stTimeInput label { color: #ffcccc !important; font-size: 18px !important; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-heading'><span class='spin-clock'>🕐</span> Attendance</div>", unsafe_allow_html=True)

# Inputs
user = st.text_input("Apna Naam Likhein:")
chutti_time = st.time_input("Chutti ka Time:")

# Save Ot Button
if st.button("Save Ot"):
    if user.strip() == "":
        st.error("⚠️ Pehle apna naam likhein!")
    else:
        duty_end_hour = 18 
        ot = 0.0
        
        if chutti_time.hour >= duty_end_hour:
            ot = (chutti_time.hour - duty_end_hour) + (chutti_time.minute / 60)
        
        # Data tayar karna
        new_data = {
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Name": user,
            "Time": chutti_time.strftime("%I:%M %p"),
            "OT": round(ot, 2)
        }
        
        # Database mein save karna
        try:
            supabase.table("attendance").insert(new_data).execute()
            st.success("✅ Record Database Mein Save Ho Gaya!")
        except Exception as e:
            st.error("⚠️ Database connection error. Settings check karein.")

# Table & Total OT Section
if st.checkbox("Mera Record", value=True):
    try:
        # Database se data mangwana
        response = supabase.table("attendance").select("*").execute()
        
        if len(response.data) > 0:
            df_record = pd.DataFrame(response.data)
            
            # Agar id column aaye toh usko hide kar do
            if 'id' in df_record.columns:
                df_record = df_record.drop(columns=['id'])
                
            st.dataframe(df_record, use_container_width=True, hide_index=True)
            
            total_ot_sum = df_record['OT'].sum()
            st.markdown(f'''
                <div class="total-ot-box">
                    TOTAL OT: {round(total_ot_sum, 2)}
                </div>
            ''', unsafe_allow_html=True)
        else:
            st.info("Abhi tak koi record save nahi hua.")
    except Exception as e:
        st.warning("⚠️ Database connect nahi hai.")
