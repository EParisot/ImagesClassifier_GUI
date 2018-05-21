#!/bin/bash

sudo pip install virtualenv
virtualenv patate_for_kids
cd patate_for_kids
source bin/activate
#dependencies
sudo pip3 install pillow
sudo pip3 install pandas
sudo pip3 install numpy
sudo pip3 install tensorflow
sudo pip3 install keras
#quit venv
deactivate
