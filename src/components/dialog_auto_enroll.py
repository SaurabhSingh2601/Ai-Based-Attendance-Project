import streamlit as st
from src.database.config import supabase
from src.database.db import enroll_student_to_subject

@st.dialog("Quick Enrollment")
def auto_enroll_dialog(subject_code):
    student_data = st.session_state.student_data
    if isinstance(student_data, list):
        student_data = student_data[0]
    student_id = student_data.get('id') if student_data.get('id') is not None else student_data.get('student_id')

    res = supabase.table('subjects').select('*').eq('subject_code', subject_code.strip()).execute()
    if not res.data:
        st.error("Subject Code Not Found!")
        if st.button('Close'):
            st.query_params.clear()
            st.rerun()
        return

    subject = res.data[0]
    subj_id = subject.get('id') if subject.get('id') is not None else subject.get('subject_id')

    check = supabase.table('subject_students').select("*").eq('subject_id', subj_id).eq('student_id', student_id).execute()
    if check.data:
        st.info("You Are Already Enrolled in this subject!")
        if st.button('Got It!'):
            st.query_params.clear()
            st.rerun()
        return

    st.markdown(f'Would you like to enroll in **{subject.get("name")}**?')

    col1, col2 = st.columns(2)
    with col1:
        if st.button('No Thanks!'):
            st.query_params.clear()
            st.rerun()

    with col2:
        if st.button('Yes, enroll now!', type="primary", width="stretch"):
            enroll_student_to_subject(student_id, subj_id)
            st.success('Joined Successfully!')
            st.query_params.clear()
            import time
            time.sleep(1.5)
            st.rerun()
