#!/bin/bash

conda env create
source activate IC_GUI
conda install -c menpo opencv
source deactivate
