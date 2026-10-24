import streamlit as st
from src.database.db import create_subject
from src.pipelines.voice_pipeline import process_bulk_audio
from src.database.config import supabase
from datetime import datetime
import pandas as pd
from src.components.dialog_attendance_results import show_attendance_result

@st.dialog("Voice Attendance")
def voice_attendance_dialog(selected_subject_id):
    st.write('Record audio of students saying "I am present". The AI will recognize the speakers!')

    audio_data = st.audio_input('Record Classroom Audio')

    if st.button('Analyze Audio', type="primary", width="stretch"):
        if audio_data is None:
            st.warning("Please record classroom audio before analyzing!")
            return

        with st.spinner('Processing Audio Data...'):
            enrolled_res = supabase.table('subject_students').select('*,students(*)').eq('subject_id', selected_subject_id).execute()
            enrolled_students = enrolled_res.data

            if not enrolled_students:
                st.warning('No students enrolled in this course.')
                return

            candidates_dict = {}
            for s in enrolled_students:
                stu = s.get('students', {})
                sid = stu.get('id') if stu.get('id') is not None else stu.get('student_id')
                voice_emb = stu.get('voice_embeddings')
                if voice_emb and sid is not None:
                    candidates_dict[sid] = voice_emb

            if not candidates_dict:
                st.error('No enrolled students have a voice profile registered.')
                return

            try:
                audio_bytes = audio_data.read()
                detected_scores = process_bulk_audio(audio_bytes, candidates_dict)
            except Exception as e:
                st.error(f"Voice analysis failed: {str(e)}")
                return

            results, attendance_to_log = [], []
            current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

            for node in enrolled_students:
                student = node.get('students', {})
                sid = student.get('id') if student.get('id') is not None else student.get('student_id')
                score = detected_scores.get(sid, 0.0)
                is_present = bool(score > 0)

                results.append({
                    "Name": student.get('name', 'Unknown'),
                    "ID": sid,
                    "Match Score": f"{score:.2f}" if is_present else "-",
                    "Status": " ✅ Present" if is_present else " ❌ Absent"
                })

                attendance_to_log.append({
                    "student_id": sid,
                    "subject_id": selected_subject_id,
                    "timestamp": current_timestamp,
                    "is_present": bool(is_present)
                })

            st.session_state.voice_attendance_results = (pd.DataFrame(results), attendance_to_log)

    if st.session_state.get('voice_attendance_results'):
        st.divider()
        df_results, logs = st.session_state.voice_attendance_results
        st.dataframe(df_results, width="stretch")
        show_attendance_result(df_results, logs)
