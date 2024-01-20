import cv2
from pathlib import Path
import os
import numpy as np
import logging
from .image import crop_image
import pandas as pd

logging.basicConfig(level=logging.DEBUG)

# Create our face detector. Both HAAR and LBP classifiers are somehow equivelent and both give good results.
# Up to you to choose one or the other.
face_detector = cv2.CascadeClassifier("classifiers/haarcascade_frontalface_default.xml")
# face_cascade = cv2.CascadeClassifier("classifiers/lbpcascade_frontalface_improved.xml")

# Create our face recognizer
face_recognizer = cv2.face.LBPHFaceRecognizer_create()

# The subjects that can be recognized
subjects = {}

FACE_DETECTOR_SCALE_FACTOR = 1.1
FACE_DETECTOR_MIN_NEIGHBORS = 5


def detect_faces(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    detected_faces = face_detector.detectMultiScale(
        gray_image,
        scaleFactor=FACE_DETECTOR_SCALE_FACTOR,
        minNeighbors=FACE_DETECTOR_MIN_NEIGHBORS,
    )
    if len(detected_faces) == 0:
        return []

    return [(rect, crop_image(image, rect)) for rect in detected_faces]


def recognize_face(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if len(subjects) == 0:
        # No subject, the model hasn't been trained, let's do nothing.
        return (None, None)
    try:
        face = face_recognizer.predict(gray_image)
    except Exception:
        logging.warning("Could not run face recognizer", exc_info=True)
    # Return the name of the recognize subject and the confident level
    return (subjects[face[0]], face[1])


def train_face_recognizer(training_data_directory="images"):
    data_file_path = Path(training_data_directory, "data.csv")
    if not data_file_path.exists():
        # Create file
        with data_file_path.open("w") as f:
            f.write("image,label\n")

    # Load file as CSV file
    data = pd.read_csv(data_file_path, delimiter=",", header=0).to_numpy()

    # Subjects that can be recognized from these data:
    identified_subjects = np.unique(data[:, 1])
    global subjects

    if len(identified_subjects) == 0:
        # No subject... We stop here
        subjects = {}
        return
    else:
        # Update subjects (persons who can be recognized)
        subjects = {e[0]: e[1] for e in enumerate(identified_subjects)}

    # Prepare training data
    faces, labels = [], []
    for row in data:
        file_name = row[0]
        label = np.where(identified_subjects == row[1])[0][0]
        file_path = Path(training_data_directory, file_name)
        if os.path.exists(file_path):
            img = cv2.imread(str(file_path), cv2.IMREAD_GRAYSCALE)
            faces.append(img)
            labels.append(label)

    # Run training!
    logging.debug(f"Run training for {subjects}...")
    face_recognizer.train(faces, np.array(labels))
