# -*- coding: utf-8 -*-

from srcs.const import *

from srcs.__init__ import *
import sys

from srcs.first_tab import FirstTab
from srcs.second_tab import SecondTab
from srcs.third_tab import ThirdTab
from srcs.fourth_tab import FourthTab

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter.scrolledtext import ScrolledText

import os
import configparser
from time import time, localtime, strftime, sleep

import numpy as np
import threading

import Tk_Tooltips

from srcs.app import App

#################################################################################
'''
This is a graphic implementation of the famous "Patate42"
'''
#################################################################################

if __name__ == '__main__':

    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg in ('--usage', '--help'):
                print('Usage: python3 Patate_for_kids')
                exit(0)

    app = App()

    app.first_tab = FirstTab(app)
    app.second_tab = SecondTab(app)
    app.third_tab = ThirdTab(app)
    app.fourth_tab = FourthTab(app)

    app.wm_protocol("WM_DELETE_WINDOW", app.on_Quit)

    app.mainloop()
