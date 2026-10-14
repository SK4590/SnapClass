import time
import numpy as np
from PIL import Image
import streamlit as st

from src.components.dialog_enroll import enroll_dialog
from src.components.footer import footer_dashboard
from src.components.header import header_dashboard
from src.components.subject_card import subject_card
from src.database.db import (
    create_student,
    get_all_students,
    get_student_attendance,
    get_student_subjects,
    unenroll_student_to_subject,
)
from src.pipelines.face_pipeline import (
    get_face_embeddings,
    predict_attendance,
    train_classifier,
)
from src.pipelines.voice_pipeline import get_voice_embedding
from src.ui.style_base_layout import style_background_dashboard, style_base_layout


def student_screen():
    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state and st.session_state.get("is_logged_in"):
        student_dashboard()
        return

    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")
    with c1:
        header_dashboard()
    with c2:
        if st.button(
            "Go back to Home",
            type="secondary",
            key="student_back_btn",
            shortcut="control+backspace",
        ):
            st.session_state["login_type"] = None
            st.rerun()

    st.header("Login using FaceID", anchor=False)
    st.write("Position your face directly in the camera frame to authenticate:")

    show_registration = False
    photo_source = st.camera_input("Position your face in the center", key="student_cam")

    if photo_source:
        img = np.array(Image.open(photo_source).convert("RGB"))

        with st.spinner("AI is scanning facial features..."):
            detected, all_ids, num_faces = predict_attendance(img)

            if num_faces == 0:
                st.warning("No face detected! Please ensure your room is well lit and look directly at the camera.")
            elif num_faces > 1:
                st.warning("Multiple faces detected! Please ensure only one student is in the frame.")
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next(
                        (s for s in all_students if s.get("student_id") == student_id or s.get("id") == student_id),
                        None,
                    )

                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = "student"
                        st.session_state.student_data = student
                        st.toast(f"Welcome back, {student['name']}!", icon="👋")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Face recognized, but student profile could not be loaded from database.")
                else:
                    st.info("Face not recognized. If you are a new student, please complete your registration below:")
                    show_registration = True

    if show_registration and photo_source:
        st.write("")
        with st.container(border=True):
            st.subheader("Register New Student Profile", anchor=False)
            st.write("We will register your face embedding from the snapshot above.")

            new_name = st.text_input("Full Name", placeholder="e.g. Rahul Sharma")

            st.write("")
            audio_data = None
            try:
                audio_data = st.audio_input(
                    "Optional Voice Enrollment: Record a short phrase (e.g. 'I am present, my name is Rahul')"
                )
            except Exception:
                pass

            st.write("")
            if st.button("Create Account & Save Biometrics", type="primary", use_container_width=True):
                if not new_name.strip():
                    st.warning("Please enter your name!")
                else:
                    with st.spinner("Generating biometric embedding and creating profile..."):
                        img = np.array(Image.open(photo_source).convert("RGB"))
                        encodings = get_face_embeddings(img)
                        if encodings:
                            face_emb = encodings[0].tolist()

                            voice_emb = None
                            if audio_data:
                                try:
                                    voice_emb = get_voice_embedding(audio_data.read())
                                except Exception:
                                    voice_emb = None

                            response_data = create_student(
                                new_name.strip(),
                                face_embedding=face_emb,
                                voice_embedding=voice_emb,
                            )

                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = "student"
                                st.session_state.student_data = response_data[0]
                                st.toast(f"Profile created! Welcome, {new_name}!", icon="🎉")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("Failed to save student profile to database.")
                        else:
                            st.error("Could not capture facial features for registration. Please take a clearer snapshot.")

    footer_dashboard()


def student_dashboard():
    student_data = st.session_state.get("student_data", {})
    student_id = student_data.get("student_id") or student_data.get("id")
    student_name = student_data.get("name", "Student")

    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"Welcome, {student_name}!")
        if st.button(
            "Logout",
            type="secondary",
            key="student_logout_btn",
            shortcut="control+backspace",
        ):
            st.session_state["is_logged_in"] = False
            st.session_state.pop("student_data", None)
            st.rerun()

    st.write("")

    col_title, col_action = st.columns([3, 1], vertical_alignment="center")
    with col_title:
        st.header("Your Enrolled Subjects", anchor=False)
    with col_action:
        if st.button("➕ Enroll in Subject", type="primary", use_container_width=True):
            enroll_dialog()

    st.divider()

    with st.spinner("Loading your enrolled subjects and attendance logs..."):
        try:
            subjects = get_student_subjects(student_id)
        except Exception as e:
            st.error(f"Error fetching enrolled subjects: {str(e)}")
            subjects = []

        try:
            logs = get_student_attendance(student_id)
        except Exception:
            logs = []

    stats_map = {}
    for log in logs:
        sid = log.get("subject_id")
        if sid not in stats_map:
            stats_map[sid] = {"total": 0, "attended": 0}
        stats_map[sid]["total"] += 1
        if log.get("is_present"):
            stats_map[sid]["attended"] += 1

    if not subjects:
        st.info("You haven't enrolled in any subjects yet. Click 'Enroll in Subject' above to join your first course!")
    else:
        cols = st.columns(2, gap="large")
        for i, sub_node in enumerate(subjects):
            sub = sub_node.get("subjects") or {}
            sid = sub.get("subject_id")
            sub_name = sub.get("name", "Subject")
            sub_code = sub.get("subject_code", "N/A")
            sub_section = sub.get("section", "A")

            stats = stats_map.get(sid, {"total": 0, "attended": 0})
            total = stats["total"]
            attended = stats["attended"]
            pct = f"{(attended / total * 100):.1f}%" if total > 0 else "N/A"

            def make_unenroll_callback(current_sid=sid, current_sub_name=sub_name):
                def callback():
                    if st.button(
                        "🗑️ Unenroll from course",
                        type="secondary",
                        use_container_width=True,
                        key=f"unenroll_{current_sid}",
                    ):
                        try:
                            unenroll_student_to_subject(student_id, current_sid)
                            st.toast(f"Unenrolled from {current_sub_name} successfully!", icon="✅")
                            time.sleep(0.8)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Unenroll failed: {str(e)}")
                return callback

            with cols[i % 2]:
                subject_card(
                    name=sub_name,
                    code=sub_code,
                    section=sub_section,
                    stats=[
                        ("📅", "Total Classes", total),
                        ("✅", "Attended", attended),
                        ("📈", "Attendance Rate", pct),
                    ],
                    footer_callback=make_unenroll_callback(sid, sub_name),
                )

    footer_dashboard()