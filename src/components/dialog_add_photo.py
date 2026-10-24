import streamlit as st
from PIL import Image

@st.dialog("Capture Or Upload Photos")
def add_photos_dialog():
    st.write("Add classroom photos to scan for attendance")

    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    if 'photo_tab' not in st.session_state:
        st.session_state.photo_tab = 'camera'

    t1, t2 = st.columns(2)

    with t1:
        type_camera = "primary" if st.session_state.photo_tab == 'camera' else "tertiary"
        if st.button('Camera', type=type_camera, width="stretch"):
            st.session_state.photo_tab = 'camera'
            st.rerun()

    with t2:
        type_upload = "primary" if st.session_state.photo_tab == 'upload' else "tertiary"
        if st.button('Upload Photos', type=type_upload, width="stretch"):
            st.session_state.photo_tab = 'upload'
            st.rerun()

    if st.session_state.photo_tab == 'camera':
        cam_photo = st.camera_input('Take Snapshot', key='dialog_cam')
        if cam_photo:
            img = Image.open(cam_photo)
            st.session_state.attendance_images.append(img)
            st.toast('Photo Captured!')

    if st.session_state.photo_tab == 'upload':
        uploaded_files = st.file_uploader(
            'Choose image files',
            type=['jpg', 'png', 'jpeg'],
            accept_multiple_files=True,
            key='dialog_upload'
        )

        if uploaded_files:
            if st.button('Add Uploaded Photos to Gallery', type="primary", width="stretch"):
                for f in uploaded_files:
                    st.session_state.attendance_images.append(Image.open(f))
                st.success(f"{len(uploaded_files)} photos added successfully!")
                import time
                time.sleep(1)
                st.rerun()

    st.divider()
    if st.button('Done', type="secondary", width="stretch"):
        st.rerun()
