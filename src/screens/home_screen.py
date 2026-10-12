import streamlit as st
from src.components.header import header_home
from src.ui.style_base_layout import style_base_layout,style_background_home
from src.components.footer import footer_home
def home_screen():
    header_home()
    style_background_home()
    style_base_layout()

    col1, col2 = st.columns(2,gap="large")
    with col1:
        st.header("I'm Student")
        st.markdown("""
        <div style="height: 160px; display: flex; align-items: center; justify-content: center;">
            <img src="https://i.ibb.co/844D9Lrt/mascot-student.png" style="width: 120px;">
        </div>
    """, unsafe_allow_html=True)
        if st.button('Student Portal',type='primary',icon=':material/arrow_outward:', icon_position="right"):
            st.session_state['login_type']='student'
            st.rerun()

    with col2:
        st.header("I'm Teacher")
        st.markdown("""
        <div style="height: 160px; display: flex; align-items: center; justify-content: center;">
            <img src="https://i.ibb.co/CsmQQV6X/mascot-prof.png" style="width: 120px;">
        </div>
    """, unsafe_allow_html=True)
        if st.button('Teacher Portal',type='primary',icon=':material/arrow_outward:', icon_position="right"):
            st.session_state['login_type']='teacher'
            st.rerun()
    footer_home()