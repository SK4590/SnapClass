import time
import streamlit as st
from src.database.config import supabase
from src.database.db import enroll_student_to_subject


@st.dialog("Quick Enrollment")
def auto_enroll_dialog(subject_code: str):
    student_data = st.session_state.get("student_data", {})
    student_id = student_data.get("student_id") or student_data.get("id")

    code_clean = subject_code.strip().upper()
    res = (
        supabase.table("subjects")
        .select("subject_id, name")
        .eq("subject_code", code_clean)
        .execute()
    )

    if not res.data:
        st.error(f"Subject code '{subject_code}' not found!")
        if st.button("Close", use_container_width=True):
            st.query_params.clear()
            st.rerun()
        return

    subject = res.data[0]
    check = (
        supabase.table("subject_students")
        .select("*")
        .eq("subject_id", subject["subject_id"])
        .eq("student_id", student_id)
        .execute()
    )

    if check.data:
        st.info(f"You are already enrolled in **{subject['name']}**!")
        if st.button("Got it!", use_container_width=True):
            st.query_params.clear()
            st.rerun()
        return

    st.markdown(f"Would you like to enroll in **{subject['name']}**?")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("No thanks", use_container_width=True):
            st.query_params.clear()
            st.rerun()

    with col2:
        if st.button("Yes, enroll now!", type="primary", use_container_width=True):
            enroll_student_to_subject(student_id, subject["subject_id"])
            st.success(f"Enrolled in {subject['name']} successfully!")
            st.query_params.clear()
            time.sleep(1.5)
            st.rerun()
