import streamlit as st
from src.database.db import create_attendance
from src.database.config import supabase
def show_attendance_result(df,logs):
    col1,col2=st.columns(2)

    with col1:
        if st.button('Discard', width="stretch"):
            st.session_state.voice_attendance_results=None
            st.session_state.attendance_images=None
            st.rerun()

    with col2:
        if st.button("Confirm & Save",type="primary",width="stretch"):
            try:
                create_attendance(logs)
                st.toast("Attendance Taken")
                st.session_state.attendance_images=[]
                st.session_state.voice_attendance_results=None
                st.rerun()
            except Exception as e:
                st.error("Sync Failed!") 

@st.dialog("Attendance Reports")
def attendance_result_dialog(df,logs):
    show_attendance_result(df,logs)

      


    