import streamlit as st
from src.database.db import create_subject


@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
    st.write("Enter the details of your new subject:")
    sub_code = st.text_input("Subject Code", placeholder="e.g. CS101")
    sub_name = st.text_input(
        "Subject Name", placeholder="e.g. Introduction to Computer Science"
    )
    sub_section = st.text_input("Section", placeholder="e.g. A")

    st.write("")
    if st.button("Create Subject Now", type="primary", use_container_width=True):
        if sub_code and sub_name and sub_section:
            try:
                create_subject(sub_code.strip().upper(), sub_name.strip(), sub_section.strip(), teacher_id)
                st.toast("Subject Created Successfully!", icon="🎉")
                st.rerun()
            except Exception as e:
                st.error(f"Error creating subject: {str(e)}")
        else:
            st.warning("Please fill out all fields.")
