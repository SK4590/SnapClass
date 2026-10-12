import io
import streamlit as st
import segno


@st.dialog("Share Class Link")
def share_subject_dialog(subject_name: str, subject_code: str):
    st.subheader(f"Enrollment for {subject_name}", anchor=False)

    join_url = f"https://snapclass.streamlit.app/?join-code={subject_code}"

    # Generate QR code
    qr = segno.make(join_url)
    out = io.BytesIO()
    qr.save(out, kind="png", scale=10, border=1)

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.markdown("#### Subject Code")
        st.code(subject_code, language="text")
        st.markdown("#### Direct Join URL")
        st.code(join_url, language="text")
        st.info("Students can scan this QR code or enter the code to join.")

    with col2:
        st.markdown("#### Scan to Join")
        st.image(out.getvalue(), caption=f"QR Code for {subject_code}", use_container_width=True)
