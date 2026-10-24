import src.pkg_resources_shim  # Compatibility shim for face_recognition_models
import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st
from src.database.db import get_all_students

@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector()
    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )
    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )
    return detector, sp, facerec

def get_face_embeddings(image_np):
    detector, sp, facerec = load_dlib_models()
    faces = detector(image_np, 1)
    encodings = []

    for face in faces:
        shape = sp(image_np, face)
        face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1)
        encodings.append(np.array(face_descriptor))

    return encodings

@st.cache_resource
def get_trained_models():
    X = []
    y = []

    student_db = get_all_students()

    if not student_db:
        return None

    for student in student_db:
        embedding = student.get("face_embeddings")
        if embedding:
            X.append(np.array(embedding))
            s_id = student.get("id") if student.get("id") is not None else student.get("student_id")
            y.append(s_id)

    if len(X) == 0:
        return None

    all_distinct = set(y)
    clf = None
    if len(all_distinct) >= 2:
        clf = SVC(kernel="linear", probability=True, class_weight="balanced")
        try:
            clf.fit(X, y)
        except Exception:
            clf = None

    return {'clf': clf, 'X': X, 'y': y}

def train_classifier():
    st.cache_resource.clear()
    model_data = get_trained_models()
    return bool(model_data)

def predict_attendance(class_image_np):
    encodings = get_face_embeddings(class_image_np)
    detected_students = {}
    model_data = get_trained_models()

    if not model_data:
        return detected_students, [], len(encodings)

    clf = model_data.get('clf')
    X_train = model_data['X']
    y_train = model_data['y']

    all_students = sorted(set(
        int(y) for y in y_train if y is not None
    ))

    if not all_students:
        return detected_students, [], len(encodings)

    resemblance_threshold = 0.6

    for encoding in encodings:
        # If classifier exists and multiple classes are present, use SVM prediction
        if clf is not None and len(all_students) >= 2:
            try:
                prediction = clf.predict([encoding])[0]
                if prediction is not None:
                    predicted_id = int(prediction)
                    if predicted_id in y_train:
                        student_embedding = X_train[y_train.index(predicted_id)]
                        best_match_score = np.linalg.norm(student_embedding - encoding)
                        if best_match_score <= resemblance_threshold:
                            detected_students[predicted_id] = True
                            continue
            except Exception:
                pass

        # Fallback / Single-student: find nearest neighbor by Euclidean distance
        best_id = None
        min_dist = float('inf')
        for idx, train_emb in enumerate(X_train):
            dist = np.linalg.norm(train_emb - encoding)
            if dist < min_dist:
                min_dist = dist
                best_id = y_train[idx]

        if min_dist <= resemblance_threshold and best_id is not None:
            detected_students[int(best_id)] = True

    return detected_students, all_students, len(encodings)
