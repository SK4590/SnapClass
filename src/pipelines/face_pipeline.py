import dlib
import face_recognition_models
import numpy as np
import streamlit as st

from src.database.db import get_all_students


@st.cache_resource
def load_dlib_models():
    """Load and cache dlib frontal face detector, shape predictor, and recognition models."""
    detector = dlib.get_frontal_face_detector()
    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )
    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )
    return detector, sp, facerec


def get_face_embeddings(image_np):
    """Detect faces and extract 128-dimensional embedding vectors."""
    detector, sp, facerec = load_dlib_models()
    faces = detector(image_np, 1)

    encodings = []
    for face in faces:
        shape = sp(image_np, face)
        face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1)
        encodings.append(np.array(face_descriptor))
    return encodings


@st.cache_resource
def get_trained_model():
    """Load all registered students and their face embeddings from Supabase."""
    X = []
    y = []

    student_db = get_all_students()
    if not student_db:
        return None

    for student in student_db:
        embedding = student.get("face_embedding")
        if embedding:
            X.append(np.array(embedding))
            y.append(student.get("student_id"))

    if len(X) == 0:
        return None

    return {"X": X, "y": y}


def train_classifier():
    """Clear cached student embeddings model and reload from Supabase."""
    st.cache_resource.clear()
    model_data = get_trained_model()
    return bool(model_data)


def predict_attendance(class_image_np):
    """Detect all faces in an image and match them against registered student embeddings."""
    encodings = get_face_embeddings(class_image_np)
    detected_student = {}

    model_data = get_trained_model()
    if not model_data:
        return detected_student, [], len(encodings)

    X_train = model_data["X"]
    y_train = model_data["y"]
    all_students = sorted(list(set(y_train)))

    for encoding in encodings:
        best_match_score = float("inf")
        predicted_id = None

        for i, student_embedding in enumerate(X_train):
            score = np.linalg.norm(student_embedding - encoding)
            if score < best_match_score:
                best_match_score = score
                predicted_id = y_train[i]

        resemblance_threshold = 0.6
        if predicted_id is not None and best_match_score <= resemblance_threshold:
            detected_student[predicted_id] = True

    return detected_student, all_students, len(encodings)
