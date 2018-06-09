#!/bin/bash

if [ -d "IC_GUI" ]
then
	cd IC_GUI
	source bin/activate
	cd ..
	python3 main.py $1
	deactivate
else
	source activate IC_GUI
	python main.py $1
	source deactivate
fi
