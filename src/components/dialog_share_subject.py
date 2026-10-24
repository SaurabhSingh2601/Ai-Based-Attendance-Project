import streamlit as st
import segno
import io

@st.dialog("Share Subject Code & QR")
def share_subject_dialog(subject_name, subject_code):
    st.subheader(f"{subject_name} ({subject_code})")
    st.write("Share this code or QR with your students so they can enroll.")

    join_url = f"?join-code={subject_code}"
    qr = segno.make(join_url)
    out = io.BytesIO()
    qr.save(out, kind="png", scale=10, border=1)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('### Subject Code')
        st.code(subject_code, language="text")
        st.info("Students can enter this code in their 'Enroll In Subject' dialog.")

    with col2:
        st.markdown('### Scan to Join')
        st.image(out.getvalue(), width=200, caption=f'QR for {subject_name}')
