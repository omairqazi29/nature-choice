# Installation

This demo requires Python 3.9 or 3.10. Python 3.11 is currently not supported by Taipy.

**Important Note**: To visualize images in Taipy, the package `python-magic` is required (and `python-magic-bin` on Windows). Please see the [python-magic](https://pypi.org/project/python-magic/) page for installation.


To install this demo:

```
git clone git@github.com:Avaiga/demo-demo-face-recognition.git
cd demo-face-recognition/src
```

To install the dependencies:
```
pip install -r requirements.txt
```

## Building the Webam component

- Clone the taipy-2-2 branch to build the front-end JavaScript,

```
pip install taipy==2.2
pip install opencv-python-headless==4.7.0.72
pip install opencv-contrib-python-headless==4.7.0.72
pip install pillow
```

- Run this command:

```
cd demo-face-recognition/webcam/webui
npm i
```

- Find the location of taipy-gui with the `find_taipy_gui_dir.py` script and run:

```
 npm i <path to taipy-gui>
```

- Change `webpack.config.js` with taipy-gui path and run:

```
npm run build
```


Finally, to run the demo:
```
python main.py
```
