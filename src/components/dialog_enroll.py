import time
import streamlit as st
from src.database.config import supabase
from src.database.db import enroll_student_to_subject


@st.dialog("Enroll in Subject")
def enroll_dialog():
    st.write("Enter the subject code provided by your teacher to enroll:")
    join_code = st.text_input("Subject Code", placeholder="e.g. CS101")

    if st.button("Enroll Now", type="primary", use_container_width=True):
        if join_code:
            code_clean = join_code.strip().upper()
            res = (
                supabase.table("subjects")
                .select("subject_id, name, subject_code")
                .eq("subject_code", code_clean)
                .execute()
            )
            if res.data:
                subject = res.data[0]
                student_data = st.session_state.get("student_data", {})
                student_id = student_data.get("student_id") or student_data.get("id")

                check = (
                    supabase.table("subject_students")
                    .select("*")
                    .eq("subject_id", subject["subject_id"])
                    .eq("student_id", student_id)
                    .execute()
                )
                if check.data:
                    st.warning(f"You are already enrolled in {subject['name']}.")
                else:
                    enroll_student_to_subject(student_id, subject["subject_id"])
                    st.success(f"Successfully enrolled in {subject['name']}!")
                    time.sleep(1)
                    st.rerun()
            else:
                st.error("Invalid subject code. Please check with your teacher.")
        else:
            st.warning("Please enter a subject code.")
