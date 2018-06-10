#!/bin/bash

sudo pip install virtualenv
virtualenv --python=python3.5 IC_GUI
cd IC_GUI
source bin/activate
#dependencies
sudo pip3 install picamera
sudo pip3 install pillow
sudo pip3 install pandas
sudo pip3 install numpy
sudo pip3 install tensorflow
sudo pip3 install keras
sudo pip3 install matplotlib
#quit venv
deactivate
