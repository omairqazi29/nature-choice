import taipy as tp
from taipy import Config, Core, Gui
import taipy.gui.builder as tgb
import cv2

# Camera capture function
def capture_image(state):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        # Convert the image format from BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Save the image to a file
        image_path = "captured_image.jpg"
        cv2.imwrite(image_path, frame)
        # Update the state with the captured image path
        state.captured_image = image_path
    cap.release()

# Taipy configuration and GUI setup
input_name_data_node_cfg = Config.configure_data_node(id="input_name")
message_data_node_cfg = Config.configure_data_node(id="message")
build_msg_task_cfg = Config.configure_task("build_msg", build_message, input_name_data_node_cfg, message_data_node_cfg)
scenario_cfg = Config.configure_scenario("scenario", task_configs=[build_msg_task_cfg])

input_name = "Taipy"
message = None
captured_image = None  # Add a state variable for the captured image

def submit_scenario(state):
    state.scenario.input_name.write(state.input_name)
    state.scenario.submit()
    state.message = state.scenario.message.read()

with tgb.Page() as page:
    tgb.text("Name:")
    tgb.input("{input_name}")
    tgb.button("Submit", on_action=submit_scenario)
    tgb.text("Message {message}")

    # Add a button and image display for the camera module
    tgb.button("Capture Image", on_action=capture_image)
    tgb.image("{captured_image}")

if __name__ == "__main__":
    Core().run()
    scenario = tp.create_scenario(scenario_cfg)
    Gui(page).run()