import streamlit as st
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.footer import footer_dashboard
from src.components.header import header_dashboard
from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import predict_attendance,get_face_embeddings,train_classifier
from src.database.db import get_all_students,create_students,get_student_subjects,get_student_attendance,unenroll_student_to_subject
from src.pipelines.voice_pipeline import get_voice_embeddings

from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card

def student_dashboard():
    student_data=st.session_state.student_data
    print(student_data)
    print(type(student_data))
    student_id=student_data['student_id']

    c1,c2=st.columns(2,vertical_alignment="center", gap="xxlarge")
    with c1:
        header_dashboard()


    with c2:
        st.subheader(f"""Welcome,{student_data['name']}""")
        if st.button("Logout", type="secondary", key="loginbackbtn" , shortcut="control+backspace"):
            st.session_state.clear() 
            # st.session_state['is_logged_in']=False
            # if "teacher_data" in st.session_state:
            #     del st.session_state.teacher_data
        
            st.rerun()  

    st.space()

    c1,c2=st.columns(2)
    with c1:
        st.header("Your Enrolled Subject")

    with c2:
         if st.button('Enroll In Subject',type="primary",width="stretch"):
             enroll_dialog()

    st.divider() 

    with st.spinner("Loading Your Subjects..."):
        subjects=get_student_subjects(student_id)
        logs=get_student_attendance(student_id)

    stats_map={}

    for log in logs:
        sid=log['subject_id']

        if sid not in stats_map:
            stats_map[sid]={"total":0,"attended":0}    

        stats_map[sid]['total']+=1

        if log.get('is_present'):
            stats_map[sid]['attended']+=1

    cols=st.columns(2)
    for i,sub_node in enumerate(subjects):
        sub=sub_node['subjects']
        sid=sub['subject_id']

        stats=stats_map.get(sid,{"total":0,"attended":0})
        def unenroll_button():
            if st.button("Unenroll",type="tertiary",width="stretch",icon=":material/delete_forever:",key=f'unenroll_{sid}'):
                unenroll_student_to_subject(student_id,sid)
                st.toast(f'Unenrolled from {sub["name"]} Successfully!')
                st.rerun()


        with cols[i%2]:
            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=[
                    ('📅','Total',stats['total']),
                    ('✅','Attended',stats['attended'])
                ],
                footer_callback=unenroll_button
            )            

        


    footer_dashboard()

def student_screen():
    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return
    
    c1,c2=st.columns(2,vertical_alignment="center", gap="xxlarge")
    with c1:
        header_dashboard()


    with c2:
        if st.button("Go back to Home", type="secondary", key="loginbackbtn" , shortcut="control+backspace"): 
            st.session_state['login_type']="None"
            st.rerun()     
    
    st.header("Login Using FaceID",text_alignment="center")
    st.space()
    st.space()
    if "show_registration" not in st.session_state:
        st.session_state.show_registration = False
    photo_source=st.camera_input("Position your face in center")
    if photo_source:
        img=np.array(Image.open(photo_source))
        
        with st.spinner("AI Is Scanning.."):
            detected,all_ids,num_faces=predict_attendance(img)

            if num_faces==0:
                st.warning("Face Not Found!")
                st.session_state.show_registration = True
            elif num_faces>1:
                st.warning("Multiple Faces Found!")
            else:
                if detected:
                    student_id=list(detected.keys())[0]
                    all_students=get_all_students()  
                    student=next((s for s in all_students if s["student_id"]==student_id),None)
                    if student:
                        st.session_state.is_logged_in=True
                        st.session_state.user_role="student"
                        st.session_state.student_data=student
                        st.toast(f"Welcome Back {student['name']}") 
                        import time
                        time.sleep(2)
                        st.rerun()  

                else:
                    st.info("Face Not Detected.You Might Be A New Studenr!")
                    st.session_state.show_registration = True

    if st.session_state.show_registration:
        with st.container(border=True):
            st.header("Register new Profile!")
            new_name=st.text_input("Enter your Name",placeholder="E.g. Rishi Shukla")

            st.subheader("Optional:Voice Enrollment")
            st.info("Enroll yourself for voice only attendance")

            audio_data=None

            try:
                audio_data=st.audio_input("Record a short phrase like i am present.My name is Abhay.")
            except Exception:
                st.error("Audio Data Failed!")

               

            if st.button("Create Account",type="primary"):
                st.write("clicked")
                print("clicked")
                if new_name:
                    print("2 anme entered")
                    with st.spinner("Creating profile..."):
                        img=np.array(Image.open(photo_source))
                        print("image shape=",img.shape)
                        print("3 image loaded")
                        encodings=get_face_embeddings(img)
                        print("encodings=",len(encodings))
                        print("4 encodings=", encodings)
                        if encodings:
                            print("5 inside encodings")
                            face_emb=encodings[0].tolist()
                            voice_emb=None
                            if audio_data:
                                voice_emb=get_voice_embeddings(audio_data.read())

                            response_data=create_students(new_name,face_embedding=face_emb,voice_embedding=voice_emb)
                            print(" 6 response_data=",response_data)

                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in=True
                                st.session_state.user_role="student"
                                st.session_state.student_data=response_data
                                st.toast(f"Profile Created! Hi {new_name}!") 
                                import time
                                time.sleep(2)
                                st.rerun()  

                            else:
                                st.error("Couldn't capture your facial features for registration!")    

                else:
                    st.warning("Please enter your name!")



                    
    footer_dashboard()

    
    

