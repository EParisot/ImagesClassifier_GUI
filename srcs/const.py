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

##### snap
SNAP_W = 810
SNAP_H = 600
SNAP_FPS = 60
#####

##### label
EXT_PHOTOS = ('.png', '.jpg', '.PNG', '.JPG', '.jpeg', '.JPEG')
WIDTH_IMG = 810
HEIGHT_IMG = 600
HEIGHT_IMG_INFO = 35
#####

##### model
MODEL_W = 900
MODEL_H = 400
LAYER_INFO_W = 250
LAYER_INFO_H = 300
#####

##### shortcut
KEY_OPTION = 'comma' # open option menu
KEY_QUIT = 'Escape' # quit windows
KEY_CTRL_L = 'Control_L'
KEY_NEXT_TAB = 'bracketright' # ctrl + tab
KEY_PREV_TAB = 'bracketleft' # ctrl + tab
    ##### label shortcut
KEY_NEXT_PHOTO = 'Up'
KEY_LAST_PHOTO = 'Down'
KEY_DEL_PHOTO = 'BackSpace'
KEY_LABEL_CHARS = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
    #####
#####
