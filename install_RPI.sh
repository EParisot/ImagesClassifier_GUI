#!/bin/bash

sudo pip install virtualenv
virtualenv --python=python3.5 IC_GUI
cd IC_GUI
source bin/activate
#dependencies
sudo pip3 install pillow
sudo pip install pandas
sudo pip install numpy
sudo pip install tensorflow
sudo pip install keras
sudo pip install matplotlib
#quit venv
deactivate
