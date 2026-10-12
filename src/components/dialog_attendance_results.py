import streamlit as st
from src.database.db import create_attendance


def show_attendance_result(df, logs):
    st.write("Please review attendance results before confirming:")
    st.dataframe(df, hide_index=True, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Discard", use_container_width=True):
            st.session_state.attendance_images = []
            st.session_state.voice_attendance_results = None
            st.rerun()

    with col2:
        if st.button("Confirm & Save", use_container_width=True, type="primary"):
            try:
                create_attendance(logs)
                st.toast("Attendance successfully recorded!", icon="✅")
                st.session_state.attendance_images = []
                st.session_state.voice_attendance_results = None
                st.rerun()
            except Exception as e:
                st.error(f"Sync failed: {str(e)}")


@st.dialog("Attendance Results")
def attendance_result_dialog(df, logs):
    show_attendance_result(df, logs)
