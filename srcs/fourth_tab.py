# -*- coding: utf-8 -*-

from srcs.const import *
import sys

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter.scrolledtext import ScrolledText

import os
import configparser
from time import time, localtime, strftime, sleep

import srcs.Tk_Tooltips as ttp

class FourthTab(object):

    def __init__(self, app):
        self.train_frame = Frame(app.fourth_tab)
        self.train_frame.grid(row=0, column=0, stick='n')
        self.train_frame.grid_columnconfigure(0, weight=1)
        self.train_frame.grid_rowconfigure(0, weight=1)
