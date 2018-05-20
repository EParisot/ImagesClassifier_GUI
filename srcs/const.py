# -*- coding: utf-8 -*-

from srcs.color import *
import platform
import os

"""
This file contains all constant
"""

if platform.system() == 'Windows':
    SYSTEM = 'Win'
elif platform.system() == 'Linux':
    if os.uname()[1] == 'raspberrypi':
        SYSTEM = 'Rpi'
    else:
        SYSTEM = 'Linux'
elif platform.system() == 'Darwin':
    SYSTEM = 'MAC'
FILE_CONFIG = 'config.cfg'

SUCCESS = 0
ERROR = 1

##### tab names
SNAP_NAME = 'Snap'
LABEL_NAME = 'Labelize'
MODEL_NAME = 'Model'
TRAIN_NAME = 'Train'
#####

##### label
EXT_PHOTOS = ('.png', '.jpg', '.PNG', '.JPG', '.jpeg', '.JPEG')
WIDTH_IMG = 800
HEIGHT_IMG = 500
HEIGHT_IMG_INFO = 35
#####

##### shortcut
KEY_OPTION = 'comma' # open option menu
KEY_QUIT = 'Escape' # quit windows
KEY_CTRL_L = 'Control_L'
    ##### label shortcut
NEXT_PHOTO = 'd'
LAST_PHOTO = 'a'
    #####
#####
