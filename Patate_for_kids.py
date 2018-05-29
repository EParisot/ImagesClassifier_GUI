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

from srcs.app import App

#################################################################################
'''
This is a graphic implementation of the famous "Patate42"
'''
#################################################################################

if __name__ == '__main__':

    devMode = False
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg in ('--usage', '--help'):
                print('Usage: python3 Patate_for_kids [--usage] [--develop]\n' + \
                        '\t--usage: print usage\n' + \
                        '\t--develop: print develloper information')
                exit(0)
            elif arg == '--develop':
                print(GREEN + '[+] ' + EOC + BOLD + 'develop mode activate' + EOC)
                devMode = True

    app = App()
    app.setDevMode(devMode)

    app.first_tab = FirstTab(app, devMode)
    app.second_tab = SecondTab(app, devMode)
    app.third_tab = ThirdTab(app, devMode)
    app.fourth_tab = FourthTab(app, devMode)

    app.wm_protocol("WM_DELETE_WINDOW", app.on_Quit)

    app.mainloop()
