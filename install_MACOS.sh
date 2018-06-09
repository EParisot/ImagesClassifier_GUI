#!/bin/bash

conda env create
source activate IC_GUI
conda install -c menpo opencv
conda install -c anaconda pillow
source deactivate
