import streamlit as st
from src.database.db import create_subject

@st.dialog("Create new Subject")
def create_subject_dialog(teacher_id):
    st.header("Enter the details of Subjects")
    sub_id=st.text_input("Subject Code",placeholder="ME-221")
    sub_name=st.text_input("Subject Name",placeholder="KOM")
    sub_section=st.text_input("Section",placeholder="B")

    if st.button("Create subject Noe",width="stretch",type="primary"):
        if sub_id and sub_name and sub_section:
            try:
                create_subject(sub_id,sub_name,sub_section,teacher_id)
                st.toast("Subject Created Successfully")
                st.rerun()
            except Exception as e:
                st.error(f"Error:{str(e)}")
        else:
            st.warning("Please fill all the fields !!")
                        
