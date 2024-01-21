from taipy.gui import Gui
from webcam import Webcam
from pathlib import Path
import cv2
import PIL.Image
import io

import logging
import uuid
from pathlib import Path
#from demo.faces import detect_faces, recognize_face, train_face_recognizer

import base64
import requests

from esg_db import *
from gpt import *

logging.basicConfig(level=logging.DEBUG)

training_data_folder = Path("images")

show_capture_dialog = False
capture_image = False
show_add_captured_images_dialog = False

labeled_faces = []  # Contains rect with label (for UI component)

captured_image = None
captured_brand = ""
captured_esg = ""

# uploads the picture to a server so open ai can work with it
# def upload_picture(img_file):
#     print(img_file)
#     with open(img_file, "rb") as file:
#         url = "https://api.imgbb.com/1/upload"
#         payload = {
#             "expiry": 600,
#             "key": 'aeee233388a1e3d25fc67e1266807b69',
#             "image": base64.b64encode(file.read()),
#         }
#
#         res = requests.post(url, payload)
#         res_json = res.json()
#         print(res_json['data']['url'])

def on_action_captured_image(state, id, action, payload):
    choice = payload["args"][0]
    if choice == 0:
         # Add image to training data:
        img = state.captured_image
        file_name = str(uuid.uuid4()) + ".jpg"
        # label = state.captured_label
        image_path = Path(training_data_folder, file_name)
        with image_path.open("wb") as f:
            file_path = f.name
            f.write(img)

        label_file_path = Path(training_data_folder, "data.csv")
        with label_file_path.open("a") as f:
            f.write(f"{file_name},{label}\n")

    state.captured_image = None
    state.captured_brand = ""
    state.captured_esg = ""
    state.show_capture_dialog = False



def process_image(state, frame):
    #print("Processing image...")
    # found = detect_faces(frame)
    #
    # labeled_images = []
    # for rect, img in found:
    #     (label, _) = recognize_face(img)
    #     labeled_images.append((img, rect, label))

    # Return this to the UI component so that it can display a rect around recognized faces:
    # state.labeled_faces = [str([*rect, label]) for (_, rect, label) in labeled_images]

    # Capture image (actually we consider only the first detected face)
    # if state.capture_image and len(labeled_images) > 0:
    if state.capture_image:
        # print(labeled_images[0][0])
        # img = labeled_images[0][0]
        img = frame
        # label = labeled_images[0][2]
        state.captured_image = cv2.imencode(".jpg", img)[1].tobytes()
        #state.captured_brand = label
        state.show_capture_dialog = True
        state.capture_image = False

        #Somewhere here
        img = state.captured_image
        file_name = str(uuid.uuid4()) + ".jpg"
        label = state.captured_brand
        image_path = Path(training_data_folder, file_name)
        with image_path.open("wb") as f:
            f.write(img)

        state.captured_brand = get_brand(image_path)
        state.captured_esg = find_esg_value_by_name(state.captured_brand)
        print(state.captured_brand, state.captured_esg)


def handle_image(state, action, args, value):
    #print("Handling image...")
    payload = value["args"][0]
    bytes = payload["data"]
    #logging.debug(f"Received data: {len(bytes)}")

    temp_path = "temp.png"

    # Write Data into temp file (OpenCV is unable to load from memory)
    image = PIL.Image.open(io.BytesIO(bytes))
    image.save(temp_path)
    image_path = Path(training_data_folder, 'test.jpg')
    with image_path.open("wb") as f:
        f.write(image.tobytes())

# Load image file
    try:
        img = cv2.imread(temp_path, cv2.IMREAD_UNCHANGED)
    except cv2.error as e:
        #logging.error(f"Failed to read image file: {e}")
        return
    process_image(state, img)
    # Finish. Tempfile is removed.


#def button_retrain_clicked(state):
    #print("Retraining...")
    #train_face_recognizer(training_data_folder)

#<|toggle|theme|id=main_bg|>

webcam_md = """
<container|container|part|

# **Nature's**{: .title} **Choice**{: .alt-title}
<|{"./nature.png"}|image|class_name=item|>

A lightweight, intuitive, and user friendly website designed to facilitate eco-friendly decision making.
{: .slogan}

Make the right choice, make *Nature's* ***Choice**{: .alt-title}*

<br/>

<card|card p-half|part|id=cam_card|
<|text-center|part|
## **Scan Product**{: .sub_title}
>
<|text-center|part|

<|webcam.Webcam|faces={labeled_faces}|classname=face_detector|id=my_face_detector|on_data_receive=handle_image|sampling_rate=100|>

<|Capture|button|on_action={lambda s: s.assign("capture_image", True)}|>
>
|card>
|container>

<|{show_capture_dialog}|dialog|labels=OK|class=custom-label|on_action=on_action_captured_image|title= Sustainability Score|
<|{captured_image}|image|width=300px|height=300px|>

<|Product: {captured_brand}|text|>

<|Nature Score: {captured_esg}|text|>
|>
"""

if __name__ == "__main__":
    # Create dir where the pictures will be stored
    if not training_data_folder.exists():
        training_data_folder.mkdir()

    #train_face_recognizer(training_data_folder)
    my_theme = {
        "palette": {
            "background": {"default": "#002626"},
            "primary": {"main": "#0e4749"},
        }
    }
    gui = Gui(webcam_md)
    gui.add_library(Webcam())
    gui.run(port=9090, theme=my_theme)
