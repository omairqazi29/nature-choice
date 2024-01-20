from taipy.gui.extension import ElementLibrary, Element, ElementProperty, PropertyType


class Webcam(ElementLibrary):
    def get_name(self) -> str:
        return "webcam"

    def get_elements(self) -> dict:
        return {
            "Webcam": Element(
                "faces",
                {
                    "faces": ElementProperty(PropertyType.dynamic_list),
                    "id": ElementProperty(PropertyType.string),
                    "classname": ElementProperty(PropertyType.dynamic_string),
                    "on_data_receive": ElementProperty(PropertyType.string),
                    "sampling_rate": ElementProperty(PropertyType.number),
                },
                react_component="Webcam",
            )
        }

    def get_scripts(self) -> list[str]:
        return ["webui/dist/webcam.js"]
