#!/bin/bash

conda env create -p python3.5
source activate IC_GUI
conda install -c menpo opencv
source deactivate
