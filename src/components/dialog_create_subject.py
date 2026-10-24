import streamlit as st
from src.database.db import create_subject

@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
    st.header("Enter Subject Details")
    sub_code = st.text_input("Subject Code", placeholder="e.g. CS-101")
    sub_name = st.text_input("Subject Name", placeholder="e.g. Data Structures")
    sub_section = st.text_input("Section", placeholder="e.g. A")

    if st.button("Create Subject Now", width="stretch", type="primary"):
        if sub_code and sub_name:
            try:
                create_subject(sub_code.strip(), sub_name.strip(), sub_section.strip() if sub_section else "", teacher_id)
                st.toast("Subject Created Successfully!")
                import time
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please fill in both Subject Code and Subject Name!")
