#!/bin/bash

sudo pip install virtualenv
virtualenv --python=python3.5 IC_GUI
cd IC_GUI
source bin/activate
#dependencies
apt-get install python3-tk
pip3 install picamera
pip3 install Pillow
pip3 install pandas
pip3 install numpy
pip3 install tensorflow
pip3 install keras
pip3 install matplotlib
#quit venv
deactivate
