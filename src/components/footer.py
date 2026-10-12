import streamlit as st

def footer_home():
    logo_url = "https://i.ibb.co/4r5X1FY/apnacollege.png"

    st.markdown(f"""
        <div style="margin-top:2rem; display:flex; gap:6px; justify-content:center; items-align:center">
            <p style="font-weight:bold; color:white;"> Created with ❤️ by </p>
            <img src='{logo_url}' style='max-height:25px' />
        </div>
        
        """, unsafe_allow_html=True)
    
def footer_dashboard():
    logo_url = "https://i.ibb.co/4r5X1FY/apnacollege.png"

    st.markdown(f"""
        <div style="margin-top:2rem; display:flex; gap:6px; justify-content:center; items-align:center">
            <p style="font-weight:bold; color:black;"> Created with ❤️ by </p>
            <img src='{logo_url}' style='max-height:25px' />
        </div>
        
        """, unsafe_allow_html=True)    