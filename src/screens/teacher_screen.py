import streamlit as st
from src.ui.style_base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard

def teacher_screen():
    style_background_dashboard()
    style_base_layout()

    # Initialize the state cleanly without spaces
    if 'teacher_login_type' not in st.session_state:
        st.session_state.teacher_login_type = "login"

    # Route to the correct screen
    if st.session_state.teacher_login_type == "login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()


def teacher_screen_login():
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    
    with c1:
        header_dashboard()
        
    with c2:
        if st.button("Go back to Home", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()    
            
    st.header('Login using password', anchor=False)
    
    # Use st.write("") to create empty vertical space
    st.write("")
    st.write("")
    
    teacher_username = st.text_input("Enter username", placeholder='shobitkhanna')
    teacher_pass = st.text_input("Enter password", type='password', placeholder='Enter password')
    
    st.divider()
    
    btnc1, btnc2 = st.columns(2)

    with btnc1:
        # Replaced width='stretch' with use_container_width=True
        st.button('Login', icon=":material/passkey:", shortcut='control+enter', use_container_width=True)
        
    with btnc2:
        if st.button('Register Instead', type="primary", icon=":material/passkey:", use_container_width=True):
            st.session_state.teacher_login_type = 'register'
            st.rerun() # Added rerun to switch views instantly    

    footer_dashboard()


def teacher_screen_register():
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    
    with c1:
        header_dashboard()
        
    with c2:
        # Updated key to be unique for this screen
        if st.button("Go back to Home", type='secondary', key='registerbackbtn', shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()
            
    st.header('Register your teacher profile', anchor=False)  
    
    st.write("")
    st.write("")
    
    teacher_username = st.text_input("Enter username", placeholder='khanna_sk45')
    teacher_name = st.text_input("Enter name", placeholder='Shobit Khanna')
    teacher_pass = st.text_input("Enter password", type='password', placeholder='Enter password')
    teacher_pass_confirm = st.text_input("Confirm your password", type='password', placeholder='Enter password')

    st.divider()
    
    btnc1, btnc2 = st.columns(2)

    with btnc1:
        st.button('Register now', icon=":material/passkey:", shortcut='control+enter', use_container_width=True)
        
    with btnc2:
        if st.button('Login Instead', type="primary", icon=":material/passkey:", use_container_width=True):    
            st.session_state.teacher_login_type = 'login'
            st.rerun() # Added rerun here as well

    footer_dashboard()