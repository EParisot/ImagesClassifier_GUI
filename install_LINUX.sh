#!/bin/bash

apt-get install python-setuptools python-dev build-essential
easy_install pip
pip install virtualenv
virtualenv -p python3.5 IC_GUI
cd IC_GUI
source bin/activate
#dependencies
apt-get install python3-tk
pip install opencv-python
pip install imutils
pip install Pillow
pip install pandas
pip install numpy
pip install tensorflow
pip install keras
pip install matplotlib
#quit venv
deactivate
