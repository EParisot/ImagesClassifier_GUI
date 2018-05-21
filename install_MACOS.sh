#!/bin/bash

conda env create
source activate patate_for_kids
conda install -c menpo opencv
conda install -c anaconda pillow
source deactivate
