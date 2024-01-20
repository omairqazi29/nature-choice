from taipy.gui import Gui
from webcam import Webcam
import cv2

import PIL.Image
import io

import logging
import uuid
from pathlib import Path
from demo.faces import detect_faces, recognize_face, train_face_recognizer


logging.basicConfig(level=logging.DEBUG)

training_data_folder = Path("images")

show_capture_dialog = False
capture_image = False
show_add_captured_images_dialog = False

labeled_faces = []  # Contains rect with label (for UI component)

captured_image = None
captured_label = ""


def on_action_captured_image(state, id, action, payload):
    print("Captured image")
    choice = payload["args"][0]
    if choice == 0:
        # Add image to training data:
        img = state.captured_image
        file_name = str(uuid.uuid4()) + ".jpg"
        label = state.captured_label
        image_path = Path(training_data_folder, file_name)
        with image_path.open("wb") as f:
            f.write(img)
        label_file_path = Path(training_data_folder, "data.csv")
        with label_file_path.open("a") as f:
            f.write(f"{file_name},{label}\n")

    state.captured_image = None
    state.captured_label = ""
    state.show_capture_dialog = False


def process_image(state, frame):
    print("Processing image...")
    found = detect_faces(frame)

    labeled_images = []
    for rect, img in found:
        (label, _) = recognize_face(img)
        labeled_images.append((img, rect, label))

    # Return this to the UI component so that it can display a rect around recognized faces:
    state.labeled_faces = [str([*rect, label]) for (_, rect, label) in labeled_images]

    # Capture image (actually we consider only the first detected face)
    if state.capture_image and len(labeled_images) > 0:
        img = labeled_images[0][0]
        label = labeled_images[0][2]
        state.captured_image = cv2.imencode(".jpg", img)[1].tobytes()
        state.captured_label = label
        state.show_capture_dialog = True
        state.capture_image = False


def handle_image(state, action, args, value):
    print("Handling image...")
    payload = value["args"][0]
    bytes = payload["data"]
    logging.debug(f"Received data: {len(bytes)}")

    temp_path = "temp.png"

    # Write Data into temp file (OpenCV is unable to load from memory)
    image = PIL.Image.open(io.BytesIO(bytes))
    image.save(temp_path)
    # Load image file
    try:
        img = cv2.imread(temp_path, cv2.IMREAD_UNCHANGED)
    except cv2.error as e:
        logging.error(f"Failed to read image file: {e}")
        return
    process_image(state, img)
    # Finish. Tempfile is removed.


def button_retrain_clicked(state):
    print("Retraining...")
    train_face_recognizer(training_data_folder)


webcam_md = """<|toggle|theme|>

<container|container|part|

# Face **recognition**{: .color-primary}

This demo shows how to use [Taipy](https://taipy.io/) with a [custom GUI component](https://docs.taipy.io/en/latest/manuals/gui/extension/) to capture video from your webcam and do realtime face detection. What this application demonstrates:

- How to build a complex custom UI component for Taipy.

- How to detect and recognize faces in the image in real time using [OpenCV](https://opencv.org/).

<br/>

<card|card p-half|part|
## **Webcam**{: .color-primary} component

<|text-center|part|
<|webcam.Webcam|faces={labeled_faces}|classname=face_detector|id=my_face_detector|on_data_receive=handle_image|sampling_rate=100|>

<|Capture|button|on_action={lambda s: s.assign("capture_image", True)}|>
<|RE-train|button|on_action=button_retrain_clicked|>
>
|card>
|container>


<|{show_capture_dialog}|dialog|labels=Validate;Cancel|on_action=on_action_captured_image|title=Add new training image|
<|{captured_image}|image|width=300px|height=300px|>

<|{captured_label}|input|>
|>
"""

if __name__ == "__main__":
    # Create dir where the pictures will be stored
    if not training_data_folder.exists():
        training_data_folder.mkdir()

    train_face_recognizer(training_data_folder)

    gui = Gui(webcam_md)
    gui.add_library(Webcam())
    gui.run(port=9090)