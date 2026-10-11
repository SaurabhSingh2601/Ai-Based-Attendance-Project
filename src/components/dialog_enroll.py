import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase

@st.dialog("Enroll In Subject")
def enroll_dialog():
    st.write("Enter The Code Provided By Your Teacher To Enroll")
    join_code=st.text_input('Subject Code',placeholder='Eg-ME-221')

    if st.button('Enroll Now',type="primary",width="stretch"):
        if join_code:
            res=supabase.table('subjects').select('subject_id,name,subject_code').eq('subject_code',join_code).execute()
            if res.data:
                subject=res.data[0]
                student_id=st.session_state.student_data['student_id']

                check=supabase.table('subject_students').select("*").eq('subject_id',subject['subject_id']).eq('student_id',student_id).execute()
                if check.data:
                    st.warning("You Are Already Enrolled In This Subject")
                else:
                    enroll_student_to_subject(student_id,subject['subject_id'])
                    st.success("Successfully Enrolled")
                    import time
                    time.sleep(1)
                    st.rerun()

        else:
            st.warning("Please Enter A Subject Code")            


    
                        