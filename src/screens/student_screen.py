import streamlit as st
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.footer import footer_dashboard
from src.components.header import header_dashboard
from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.database.db import get_all_students, create_students, get_student_subjects, get_student_attendance, unenroll_student_to_subject
from src.pipelines.voice_pipeline import get_voice_embeddings
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card


def student_dashboard():
    student_data = st.session_state.student_data
    if isinstance(student_data, list):
        student_data = student_data[0]
        st.session_state.student_data = student_data

    student_id = student_data.get('id') if student_data.get('id') is not None else student_data.get('student_id')

    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")
    with c1:
        header_dashboard()

    with c2:
        st.subheader(f"Welcome, {student_data.get('name')}")
        if st.button("Logout", type="secondary", key="studentlogoutbtn", shortcut="control+backspace"):
            st.session_state.clear()
            st.rerun()

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.header("Your Enrolled Subjects")

    with c2:
        if st.button('Enroll In Subject', type="primary", width="stretch"):
            enroll_dialog()

    st.divider()

    with st.spinner("Loading Your Subjects..."):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    stats_map = {}
    for log in logs:
        sid = log.get('subject_id')
        if sid not in stats_map:
            stats_map[sid] = {"total": 0, "attended": 0}

        stats_map[sid]['total'] += 1
        if log.get('is_present'):
            stats_map[sid]['attended'] += 1

    if not subjects:
        st.info("You haven't enrolled in any subjects yet. Click 'Enroll In Subject' above!")

    cols = st.columns(2)
    for i, sub_node in enumerate(subjects):
        sub = sub_node.get('subjects', {})
        sid = sub.get('id') if sub.get('id') is not None else sub.get('subject_id')
        stats = stats_map.get(sid, {"total": 0, "attended": 0})

        def make_unenroll_btn(subj_id, subj_name):
            def unenroll_button():
                if st.button("Unenroll", type="tertiary", width="stretch", icon=":material/delete_forever:", key=f'unenroll_{subj_id}'):
                    unenroll_student_to_subject(student_id, subj_id)
                    st.toast(f'Unenrolled from {subj_name} successfully!')
                    st.rerun()
            return unenroll_button

        with cols[i % 2]:
            subject_card(
                name=sub.get('name', 'Unknown'),
                code=sub.get('subject_code', ''),
                section=sub.get('section', ''),
                stats=[
                    ('📅', 'Total', stats['total']),
                    ('✅', 'Attended', stats['attended'])
                ],
                footer_callback=make_unenroll_btn(sid, sub.get('name', ''))
            )

    footer_dashboard()


def student_screen():
    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state and st.session_state.get('is_logged_in'):
        student_dashboard()
        return

    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")
    with c1:
        header_dashboard()

    with c2:
        if st.button("Go back to Home", type="secondary", key="studentbackbtn", shortcut="control+backspace"):
            st.session_state['login_type'] = "None"
            st.rerun()

    st.header("Login Using FaceID", text_alignment="center")
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    if "show_registration" not in st.session_state:
        st.session_state.show_registration = False

    photo_source = st.camera_input("Position your face in center")
    if photo_source:
        img = np.array(Image.open(photo_source))

        with st.spinner("AI Is Scanning..."):
            detected, all_ids, num_faces = predict_attendance(img)

            if num_faces == 0:
                st.warning("No face detected! Please ensure your face is well lit and centered.")
                st.session_state.show_registration = True
            elif num_faces > 1:
                st.warning("Multiple faces detected! Please ensure only one person is in the frame.")
            else:
                if detected:
                    matched_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next(
                        (s for s in all_students if (s.get("id") == matched_id or s.get("student_id") == matched_id)),
                        None
                    )
                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = "student"
                        st.session_state.student_data = student
                        st.toast(f"Welcome Back, {student.get('name')}!")
                        import time
                        time.sleep(1)
                        st.rerun()
                else:
                    st.info("Face not recognized in the database. Please register below!")
                    st.session_state.show_registration = True

    if st.session_state.show_registration:
        with st.container(border=True):
            st.header("Register New Profile")
            new_name = st.text_input("Enter your Full Name", placeholder="E.g. Rishi Shukla")

            st.subheader("Optional: Voice Enrollment")
            st.info("Record a short phrase (e.g. 'I am present. My name is [Your Name]').")

            audio_data = None
            try:
                audio_data = st.audio_input("Record Voice Sample")
            except Exception:
                st.info("Voice recording is optional or not supported on this browser.")

            if st.button("Create Account", type="primary"):
                if not new_name:
                    st.warning("Please enter your name!")
                elif not photo_source:
                    st.warning("Please capture a photo first using the camera above!")
                else:
                    with st.spinner("Creating profile..."):
                        img = np.array(Image.open(photo_source))
                        encodings = get_face_embeddings(img)
                        if encodings:
                            face_emb = encodings[0].tolist()
                            voice_emb = None
                            if audio_data is not None:
                                try:
                                    voice_emb = get_voice_embeddings(audio_data.read())
                                except Exception:
                                    voice_emb = None

                            response_data = create_students(new_name, face_embedding=face_emb, voice_embedding=voice_emb)

                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = "student"
                                st.session_state.student_data = response_data[0] if isinstance(response_data, list) else response_data
                                st.toast(f"Profile Created! Hi {new_name}!")
                                import time
                                time.sleep(1.5)
                                st.rerun()
                            else:
                                st.error("Failed to save profile in database.")
                        else:
                            st.error("Couldn't extract facial features from the captured photo. Please try again with better lighting!")

    footer_dashboard()
