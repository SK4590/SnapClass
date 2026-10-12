import time
from datetime import datetime
import pandas as pd
import streamlit as st

from src.components.dialog_add_photo import add_photos_dialog
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.footer import footer_dashboard
from src.components.header import header_dashboard
from src.components.subject_card import subject_card
from src.database.db import (
    check_teacher_exists,
    create_teacher,
    get_attendance_for_teacher,
    get_teacher_subjects,
    teacher_login,
)
from src.ui.style_base_layout import style_background_dashboard, style_base_layout


def teacher_screen():
    style_background_dashboard()
    style_base_layout()

    if "teacher_data" in st.session_state and st.session_state.get("is_logged_in"):
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

    st.write("")

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "manage_subjects"

    tab1, tab2, tab3 = st.columns(3)

    with tab1:
        type1 = (
            "primary"
            if st.session_state.current_teacher_tab == "take_attendance"
            else "secondary"
        )
        if st.button(
            "📸 Take Attendance",
            type=type1,
            use_container_width=True,
        ):
            st.session_state.current_teacher_tab = "take_attendance"
            st.rerun()

    with tab2:
        type2 = (
            "primary"
            if st.session_state.current_teacher_tab == "manage_subjects"
            else "secondary"
        )
        if st.button(
            "📚 Manage Subjects",
            type=type2,
            use_container_width=True,
        ):
            st.session_state.current_teacher_tab = "manage_subjects"
            st.rerun()

    with tab3:
        type3 = (
            "primary"
            if st.session_state.current_teacher_tab == "attendance_records"
            else "secondary"
        )
        if st.button(
            "📊 Attendance Records",
            type=type3,
            use_container_width=True,
        ):
            st.session_state.current_teacher_tab = "attendance_records"
            st.rerun()

    st.divider()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()
    elif st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()
    elif st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()

    footer_dashboard()


def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data.get("teacher_id") or st.session_state.teacher_data.get("id")

    col1, col2 = st.columns([3, 1], vertical_alignment="center")
    with col1:
        st.header("Manage Subjects", anchor=False)
    with col2:
        if st.button("➕ Create New Subject", type="primary", use_container_width=True):
            create_subject_dialog(teacher_id)

    try:
        subjects = get_teacher_subjects(teacher_id)
    except Exception as e:
        st.error(f"Error fetching subjects: {str(e)}")
        subjects = []

    if subjects:
        st.write("")
        for sub in subjects:
            stats = [
                ("👥", "Students", sub.get("total_students", 0)),
                ("📅", "Classes", sub.get("total_classes", 0)),
            ]

            def make_share_callback(name=sub["name"], code=sub["subject_code"]):
                def callback():
                    col_share, _ = st.columns([1, 3])
                    with col_share:
                        if st.button(
                            "📲 Share Code & QR",
                            key=f"share_{code}",
                            icon=":material/share:",
                            use_container_width=True,
                        ):
                            share_subject_dialog(name, code)
                return callback

            subject_card(
                name=sub["name"],
                code=sub["subject_code"],
                section=sub["section"],
                stats=stats,
                footer_callback=make_share_callback(sub["name"], sub["subject_code"]),
            )
    else:
        st.info("No subjects found yet. Click 'Create New Subject' above to add your first course!")


def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data.get("teacher_id") or st.session_state.teacher_data.get("id")
    st.header("Take Classroom Attendance", anchor=False)

    if "attendance_images" not in st.session_state:
        st.session_state.attendance_images = []

    try:
        subjects = get_teacher_subjects(teacher_id)
    except Exception as e:
        st.error(f"Error fetching subjects: {str(e)}")
        subjects = []

    if not subjects:
        st.warning("You haven't created any subjects yet! Please create one in 'Manage Subjects' first.")
        return

    subject_options = {
        f"{s['name']} ({s['subject_code']} - Sec {s['section']})": s["subject_id"]
        for s in subjects
    }

    col1, col2 = st.columns([3, 1], vertical_alignment="bottom")

    with col1:
        selected_subject_label = st.selectbox(
            "Select Subject for Attendance", options=list(subject_options.keys())
        )

    with col2:
        if st.button(
            "📸 Add Photos",
            type="primary",
            icon=":material/photo_prints:",
            use_container_width=True,
        ):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.divider()

    if st.session_state.attendance_images:
        st.subheader("Captured Classroom Photos", anchor=False)
        gallery_cols = st.columns(4)
        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4]:
                st.image(img, use_container_width=True, caption=f"Photo {idx+1}")

    has_photos = bool(st.session_state.attendance_images)
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button(
            "🗑️ Clear Photos",
            use_container_width=True,
            type="secondary",
            disabled=not has_photos,
        ):
            st.session_state.attendance_images = []
            st.rerun()

    with c2:
        if st.button(
            "🔍 Run Face Analysis",
            use_container_width=True,
            type="primary",
            icon=":material/analytics:",
            disabled=not has_photos,
        ):
            st.info("Face Recognition AI pipeline will be connected in Phase D!")

    with c3:
        if st.button(
            "🎙️ Voice Attendance",
            use_container_width=True,
            type="secondary",
            icon=":material/mic:",
        ):
            st.info("Voice Attendance pipeline will be connected in Phase D!")


def teacher_tab_attendance_records():
    st.header("Attendance Records & Analytics", anchor=False)
    teacher_id = st.session_state.teacher_data.get("teacher_id") or st.session_state.teacher_data.get("id")

    try:
        records = get_attendance_for_teacher(teacher_id)
    except Exception as e:
        st.error(f"Error fetching attendance records: {str(e)}")
        records = []

    if not records:
        st.info("No attendance sessions recorded yet. Take attendance to see analytics and reports here.")
        return

    data = []
    for r in records:
        ts = r.get("timestamp")
        try:
            formatted_time = (
                datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p")
                if ts
                else "N/A"
            )
        except Exception:
            formatted_time = str(ts)

        data.append({
            "ts_group": ts.split(".")[0] if ts else None,
            "Time": formatted_time,
            "Subject": r.get("subjects", {}).get("name", "Unknown"),
            "Subject Code": r.get("subjects", {}).get("subject_code", "N/A"),
            "Student Name": r.get("students", {}).get("name", "Unknown"),
            "is_present": bool(r.get("is_present", False)),
        })

    df = pd.DataFrame(data)

    summary = (
        df.groupby(["ts_group", "Time", "Subject", "Subject Code"])
        .agg(
            Present_Count=("is_present", "sum"),
            Total_Count=("is_present", "count"),
        )
        .reset_index()
    )

    summary["Attendance Stats"] = (
        "✅ "
        + summary["Present_Count"].astype(str)
        + " / "
        + summary["Total_Count"].astype(str)
        + " Students"
    )

    display_df = summary.sort_values(by="ts_group", ascending=False)[
        ["Time", "Subject", "Subject Code", "Attendance Stats"]
    ]

    st.dataframe(display_df, use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("Subject-wise Detailed Attendance", anchor=False)

    unique_subjects = df["Subject"].unique()
    selected_subject = st.selectbox("Select Subject for Details", unique_subjects)

    if selected_subject:
        subject_df = df[df["Subject"] == selected_subject]
        stu_summary = (
            subject_df.groupby("Student Name")
            .agg(
                Present=("is_present", "sum"),
                Total_Classes=("is_present", "count"),
            )
            .reset_index()
        )
        stu_summary["Attendance %"] = (
            (stu_summary["Present"] / stu_summary["Total_Classes"] * 100)
            .round(1)
            .astype(str)
            + "%"
        )
        st.dataframe(stu_summary, use_container_width=True, hide_index=True)