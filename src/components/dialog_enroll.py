import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase

@st.dialog("Enroll In Subject")
def enroll_dialog():
    st.write("Enter The Code Provided By Your Teacher To Enroll")
    join_code = st.text_input('Subject Code', placeholder='Eg-ME-221')

    if st.button('Enroll Now', type="primary", width="stretch"):
        if join_code:
            res = supabase.table('subjects').select('*').eq('subject_code', join_code.strip()).execute()
            if res.data:
                subject = res.data[0]
                subj_id = subject.get('id') if subject.get('id') is not None else subject.get('subject_id')

                student_data = st.session_state.student_data
                if isinstance(student_data, list):
                    student_data = student_data[0]
                student_id = student_data.get('id') if student_data.get('id') is not None else student_data.get('student_id')

                check = supabase.table('subject_students').select("*").eq('subject_id', subj_id).eq('student_id', student_id).execute()
                if check.data:
                    st.warning("You Are Already Enrolled In This Subject")
                else:
                    enroll_student_to_subject(student_id, subj_id)
                    st.success("Successfully Enrolled!")
                    import time
                    time.sleep(1)
                    st.rerun()
            else:
                st.error("No subject found with this code!")
        else:
            st.warning("Please Enter A Subject Code")
