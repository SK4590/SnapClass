import time
import streamlit as st
from src.ui.style_base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.database.db import (
    check_teacher_exists,
    create_teacher,
    teacher_login,
)


def teacher_screen():
    style_background_dashboard()
    style_base_layout()

    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif st.session_state.get("teacher_login_type", "login") == "login":
        teacher_screen_login()
    elif st.session_state.get("teacher_login_type") == "register":
        teacher_screen_register()


def login_teacher(username: str, password: str):
    """Authenticate teacher and set session state."""
    if not username or not password:
        return False, "Please enter both username and password."

    try:
        teacher = teacher_login(username, password)
        if teacher:
            st.session_state.user_role = "teacher"
            st.session_state.teacher_data = teacher
            st.session_state.is_logged_in = True
            return True, "Welcome back!"
        return False, "Invalid username or password combo."
    except Exception as e:
        return False, f"Database error: {str(e)}"


def register_teacher(
    username: str, name: str, password: str, password_confirm: str
):
    """Validate and register a new teacher."""
    if not username or not name or not password or not password_confirm:
        return False, "All fields are required!"
    if password != password_confirm:
        return False, "Passwords do not match!"

    try:
        if check_teacher_exists(username):
            return False, "Username already taken. Please choose another."

        create_teacher(username, password, name)
        return True, "Account successfully created! Please log in."
    except Exception as e:
        return False, f"Database error: {str(e)}"


def teacher_screen_login():
    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")

    with c1:
        header_dashboard()

    with c2:
        if st.button(
            "Go back to Home",
            type="secondary",
            key="loginbackbtn",
            shortcut="control+backspace",
        ):
            st.session_state["login_type"] = None
            st.rerun()

    st.header("Login using password", anchor=False)

    st.write("")
    st.write("")

    teacher_username = st.text_input(
        "Enter username", placeholder="shobitkhanna"
    )
    teacher_pass = st.text_input(
        "Enter password", type="password", placeholder="Enter password"
    )

    st.divider()

    btnc1, btnc2 = st.columns(2)

    with btnc1:
        if st.button(
            "Login",
            icon=":material/passkey:",
            shortcut="control+enter",
            use_container_width=True,
        ):
            success, msg = login_teacher(teacher_username, teacher_pass)
            if success:
                st.toast(msg, icon="👋")
                time.sleep(1)
                st.rerun()
            else:
                st.error(msg)

    with btnc2:
        if st.button(
            "Register Instead",
            type="primary",
            icon=":material/passkey:",
            use_container_width=True,
        ):
            st.session_state.teacher_login_type = "register"
            st.rerun()

    footer_dashboard()


def teacher_screen_register():
    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")

    with c1:
        header_dashboard()

    with c2:
        if st.button(
            "Go back to Home",
            type="secondary",
            key="registerbackbtn",
            shortcut="control+backspace",
        ):
            st.session_state["login_type"] = None
            st.rerun()

    st.header("Register your teacher profile", anchor=False)

    st.write("")
    st.write("")

    teacher_username = st.text_input(
        "Enter username", placeholder="khanna_sk45"
    )
    teacher_name = st.text_input("Enter name", placeholder="Shobit Khanna")
    teacher_pass = st.text_input(
        "Enter password", type="password", placeholder="Enter password"
    )
    teacher_pass_confirm = st.text_input(
        "Confirm your password",
        type="password",
        placeholder="Enter password",
    )

    st.divider()

    btnc1, btnc2 = st.columns(2)

    with btnc1:
        if st.button(
            "Register now",
            icon=":material/passkey:",
            shortcut="control+enter",
            use_container_width=True,
        ):
            success, message = register_teacher(
                teacher_username,
                teacher_name,
                teacher_pass,
                teacher_pass_confirm,
            )
            if success:
                st.success(message)
                time.sleep(1.5)
                st.session_state.teacher_login_type = "login"
                st.rerun()
            else:
                st.error(message)

    with btnc2:
        if st.button(
            "Login Instead",
            type="primary",
            icon=":material/passkey:",
            use_container_width=True,
        ):
            st.session_state.teacher_login_type = "login"
            st.rerun()

    footer_dashboard()


def teacher_dashboard():
    teacher_data = st.session_state.get("teacher_data", {})
    teacher_name = teacher_data.get("name", "Teacher")

    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")

    with c1:
        header_dashboard()

    with c2:
        st.subheader(f"Welcome, {teacher_name}!")
        if st.button(
            "Logout",
            type="secondary",
            key="teacher_logout_btn",
            shortcut="control+backspace",
        ):
            st.session_state.pop("teacher_data", None)
            st.session_state["is_logged_in"] = False
            st.rerun()

    st.divider()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "manage_subjects"

    tab1, tab2, tab3 = st.tabs(
        ["📸 Take Attendance", "📚 Manage Subjects", "📊 Attendance Records"]
    )

    with tab1:
        st.info("Attendance session pipeline will be available in Phase B & D.")

    with tab2:
        st.info("Subject management will be available in Phase B.")

    with tab3:
        st.info("Attendance records & analytics will be available in Phase B.")

    footer_dashboard()