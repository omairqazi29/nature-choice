# Demo Face Recognition

## What is Demo Face Recognition

This demo shows how to use Taipy with a custom GUI component to capture video from your webcam and do realtime face detection.

What this application demonstrates:
* How to build a complex custom UI component for Taipy.
* How to detect and recognize faces in the image in real time using OpenCV.

## Usage

A Webcam component is shown at the center of the application. It can detect faces and identify them. To be able to recognize your face, capture multiple photos of your face (click on the "Capture" button) and write your name when the dialog appears. At the end, click "Retrain" and the model should now recognize your face.

## Demo Type

- **Level**: Advanced
- **Topic**: Taipy-GUI, Computer Vision
- **Components/Controls**:
  - Taipy GUI: custom GUI component
- **Other**: OpenCV
## Installation
Want to install this demo? Check out our [`INSTALLATION.md`](docs/INSTALLATION.md) file.
## Getting Started

Check out our [`GETTING_STARTED.md`](docs/GETTING_STARTED.md) file.

## Directory Structure

- `src/`: Main folder for the application code
  - `main.py`: Main file containing the demo application code.
  - `demo/`: Contains additional demo source code.
    - `demo/faces.py`: Contains the code to do face detection and face recognition.
    - `src/image.py`: Contains shared facility functions.
  - `webcam/`: Contains custom component code. The directory contains the Python files to declare the custom component to Taipy.
    - `webcam/webui`: Contains the TypeScript source code for the custom React component.
  - `classifiers`: Contains the OpenCV classifiers used in the app for face detection.
  - `images`: Contains the files to train the face detection of the demo. This folder is created at first startup. All image captures will go into this directory.
- `docs/`: contains the images for the documentation
- `CODE_OF_CONDUCT.md`: Code of conduct for members and contributors of _demo-covid-dashboard_.
- `CONTRIBUTING.md`: Instructions to contribute to _demo-covid-dashboard_.
- `INSTALLATION.md`: Instructions to install _demo-covid-dashboard_.
- `LICENSE`: The Apache 2.0 License.
- `Pipfile`: File used by the Pipenv virtual environment to manage project dependencies.
- `README.md`: Current file.

## Contributing

Want to help build this demo? Check out our [`CONTRIBUTING.md`](docs/CONTRIBUTING.md) file.

## License

Licensed under the Apache License, Version 2.0. See [`LICENSE.md`](LICENSE.md).
