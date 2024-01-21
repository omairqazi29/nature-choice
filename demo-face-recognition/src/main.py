from taipy.gui import Gui
from webcam import Webcam
import cv2

import PIL.Image
import io

import logging
import uuid
from pathlib import Path

from serpapi import GoogleSearch

from sp_api.api import Catalog
from sp_api.base import Marketplaces

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
            getBrand(getASIN(file_name))

    state.captured_image = None
    state.show_capture_dialog = False

def getASIN(file):
    params = {
    "engine": "google_lens",
    "url": "https://i.imgur.com/Jydn4Wb.jpeg",
    "api_key": "1e24556cfe05605f06f5fec311156615979876f6e1d3e9de4be1f6b9c39d7e35"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    knowledge_graph = results["knowledge_graph"]

    amazon_link = None
    for web in data["knowledge_graph"][0]["shopping_results"]:
        if "amazon" in web["source"].lower(): \
        amazon_link = web["link"]
        break

    asin = amazon_link.split('/dp/')[-1] if amazon_link else None

    return asin

def getBrand(asin):
    credentials = dict(
        refresh_token='Atzr|IwEBIIpVxgboyA6VhQqRnFSdocT4CgCzS85nr0KMt53T-moCph8akQbg-z9Ckrk3NNF4iyaRS8vIajYRiCSA1bTtTjaeGU9zdQaUVzIMHvEUtUIa6x-ZhvXc5KAhICp33vCo8dbTT_nVvOG1IS6RYFXMMpGeBHriVmIQne6Losv26DKYTzO54bRvxnE8X3NpzpB7H73qcgzM1_KslROGqUcF-qGJ_rsuNp4On5zskdml4LinKsGkWo3R9uK2QTqW6yGz8WP9jpJNq74t8xAHiNOqHqu8kTxFd1raLj9YzntZJls20ERz8GpFoGu8c8s0PfOwi_-MRV7XvSvWFT3oB1lBVtmi',
        lwa_app_id='amzn1.application-oa2-client.4566270efc6b46efa65dc239f81bafcf',
        lwa_client_secret='amzn1.oa2-cs.v1.ffbe2dc4ed59de070bca8474b942af9d2501cc2f1541bf1e92a86ba7b21b3cfe'
    )

    catalog_client = Catalog(credentials=credentials)
    res = catalog_client.get_item('B09SL1VL7L', MarketplaceId='A2EUQ1WTGCTBG2').payload
    return res['AttributeSets'][0]['Brand']
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
<|{captured_image}||width=300px|height=300px|image|>
|>
"""

if __name__ == "__main__":
    # Create dir where the pictures will be stored
    if not training_data_folder.exists():
        training_data_folder.mkdir()

    gui = Gui(webcam_md)
    gui.add_library(Webcam())
    gui.run(port=9090)
