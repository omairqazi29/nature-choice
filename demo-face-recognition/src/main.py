from taipy.gui import Gui
from webcam import Webcam
import cv2

import PIL.Image
import io

import logging
import uuid
from pathlib import Path

logging.basicConfig(level=logging.DEBUG)

training_data_folder = Path("images")

show_capture_dialog = False
capture_image = False

captured_image = None


def on_action_captured_image(state, id, action, payload):
    print("Captured image")
    choice = payload["args"][0]
    if choice == 0:
        # Add image to training data:
        img = state.captured_image
        file_name = str(uuid.uuid4()) + ".jpg"
        image_path = Path(training_data_folder, file_name)
        with image_path.open("wb") as f:
            f.write(img)

    state.captured_image = None
    state.show_capture_dialog = False


def handle_image(state, action, args, value):
    print("Handling image...")
    payload = value["args"][0]
    bytes = payload["data"]
    logging.debug(f"Received data: {len(bytes)}")

    temp_path = "temp.png"

    # Write Data into temp file
    image = PIL.Image.open(io.BytesIO(bytes))
    image.save(temp_path)
    # Load image file
    try:
        img = cv2.imread(temp_path, cv2.IMREAD_UNCHANGED)
    except cv2.error as e:
        logging.error(f"Failed to read image file: {e}")
        return

    # Capture image
    if state.capture_image:
        state.captured_image = cv2.imencode(".jpg", img)[1].tobytes()
        state.show_capture_dialog = True
        state.capture_image = False


webcam_md = """<|toggle|theme|>

<container|container|part|

# Webcam Photo Capture Demo

This demo uses [Taipy](https://taipy.io/) and a [custom GUI component](https://docs.taipy.io/en/latest/manuals/gui/extension/) to capture photos from your webcam.

<br/>

<card|card p-half|part|
## **Webcam**{: .color-primary} component

<|text-center|part|
<|webcam.Webcam|classname=webcam_capture|id=my_webcam|on_data_receive=handle_image|sampling_rate=100|>

<|Capture|button|on_action={lambda s: s.assign("capture_image", True)}|>
>
|card>
|container>

<|{show_capture_dialog}|dialog|labels=Validate;Cancel|on_action=on_action_captured_image|title=Add new photo|
<|{captured_image}|image|>
|>
"""

if __name__ == "__main__":
    # Create dir where the pictures will be stored
    if not training_data_folder.exists():
        training_data_folder.mkdir()

    gui = Gui(webcam_md)
    gui.add_library(Webcam())
    gui.run(port=9090)
