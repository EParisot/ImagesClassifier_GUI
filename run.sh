#!/bin/bash

if [ -d "patate_for_kids" ]
then
	cd patate_for_kids
	source bin/activate
	cd ..
	python3 Patate_for_kids.py $1
	deactivate
else
	source activate patate_for_kids
	python Patate_for_kids.py $1
	source deactivate
fi
