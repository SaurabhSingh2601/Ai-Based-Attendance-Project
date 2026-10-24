import src.pkg_resources_shim  # Compatibility shim for face_recognition_models
import streamlit as st
import io
import numpy as np
from PIL import Image
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.footer import footer_dashboard
from src.components.header import header_dashboard
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
        try:
            subjects = get_student_subjects(student_id)
            logs = get_student_attendance(student_id)
        except Exception as e:
            st.error(f"Failed to load subjects: {str(e)}")
            subjects = []
            logs = []

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
                    try:
                        unenroll_student_to_subject(student_id, subj_id)
                        st.toast(f'Unenrolled from {subj_name} successfully!')
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to unenroll: {str(e)}")
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

    if "student_tab" not in st.session_state:
        st.session_state.student_tab = "login"

    tab_col1, tab_col2 = st.columns(2)
    with tab_col1:
        type_login = "primary" if st.session_state.student_tab == "login" else "tertiary"
        if st.button("FaceID Login", type=type_login, width="stretch", icon=":material/face:"):
            st.session_state.student_tab = "login"
            st.rerun()

    with tab_col2:
        type_reg = "primary" if st.session_state.student_tab == "register" else "tertiary"
        if st.button("Register New Student", type=type_reg, width="stretch", icon=":material/person_add:"):
            st.session_state.student_tab = "register"
            st.rerun()

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    # ==========================
    # 1. FACEID LOGIN TAB
    # ==========================
    if st.session_state.student_tab == "login":
        st.header("Login Using FaceID", text_alignment="center")
        st.write("Position your face in the camera to log in.")

        photo_source = st.camera_input("Capture Face Snapshot", key="student_login_cam")
        if photo_source:
            photo_bytes = photo_source.getvalue()
            pil_img = Image.open(io.BytesIO(photo_bytes)).convert('RGB')
            img_np = np.array(pil_img)

            with st.spinner("AI is verifying your identity..."):
                detected, all_ids, num_faces = predict_attendance(img_np)

            if num_faces == 0:
                st.warning("No face detected! Please ensure your face is well lit and facing the camera.")
            elif num_faces > 1:
                st.warning("Multiple faces detected! Please ensure only one person is in front of the camera.")
            else:
                if detected:
                    matched_id = list(detected.keys())[0]
                    try:
                        all_students = get_all_students()
                    except Exception as e:
                        st.error(f"Database error: {str(e)}")
                        all_students = []

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
                    st.info("Face not recognized in the database. Please register your profile!")
                    if st.button("Register as New Student Instead", type="primary"):
                        st.session_state.student_tab = "register"
                        st.rerun()

    # ==========================
    # 2. REGISTER NEW STUDENT TAB
    # ==========================
    elif st.session_state.student_tab == "register":
        st.header("Register New Student Profile", text_alignment="center")

        with st.container(border=True):
            new_name = st.text_input("Enter your Full Name *", placeholder="E.g. Saurabh Singh", key="reg_full_name")

            st.markdown("### 1. Capture Your Face *")
            reg_photo = st.camera_input("Take a clear photo of your face", key="reg_face_cam")

            st.markdown("### 2. Optional: Voice Sample")
            st.info("Record a short phrase (e.g. 'I am present. My name is [Your Name]').")
            audio_data = None
            try:
                audio_data = st.audio_input("Record Voice Sample (Optional)", key="reg_voice_sample")
            except Exception:
                st.info("Audio recording is not supported on this device/browser.")

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

            if st.button("Create Account & Save Profile", type="primary", width="stretch"):
                if not new_name.strip():
                    st.warning("Please enter your Full Name!")
                elif not reg_photo:
                    st.warning("Please capture a photo of your face using the camera above!")
                else:
                    with st.spinner("Extracting facial features..."):
                        photo_bytes = reg_photo.getvalue()
                        pil_img = Image.open(io.BytesIO(photo_bytes)).convert('RGB')
                        img_np = np.array(pil_img)
                        encodings = get_face_embeddings(img_np)

                    if not encodings:
                        st.error("No face detected in the captured photo! Please ensure good lighting, look straight at the camera, and take the photo again.")
                    else:
                        with st.spinner("Saving your account to database..."):
                            face_emb = encodings[0].tolist() if hasattr(encodings[0], 'tolist') else list(encodings[0])
                            voice_emb = None

                            if audio_data is not None:
                                try:
                                    audio_bytes = audio_data.getvalue() if hasattr(audio_data, 'getvalue') else audio_data.read()
                                    if audio_bytes and len(audio_bytes) > 500:
                                        voice_emb = get_voice_embeddings(audio_bytes)
                                except Exception:
                                    voice_emb = None

                            try:
                                response_data = create_students(
                                    new_name.strip(),
                                    face_embedding=face_emb,
                                    voice_embedding=voice_emb
                                )
                            except Exception as e:
                                st.error(f"Database Error: {str(e)}")
                                response_data = None

                            if response_data and len(response_data) > 0:
                                # Re-train student classifier cache
                                train_classifier()
                                new_student = response_data[0]
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = "student"
                                st.session_state.student_data = new_student
                                st.toast(f"Account Created! Welcome, {new_name.strip()}!")
                                import time
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("Failed to save profile. Please check database connection.")

    footer_dashboard()
