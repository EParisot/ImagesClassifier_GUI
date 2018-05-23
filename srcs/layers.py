# -*- coding: utf-8 -*-

from srcs.const import *

import sys
import os
from time import time, localtime, strftime, sleep

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter.scrolledtext import ScrolledText

from PIL import Image, ImageTk

import srcs.Tk_Tooltips as ttp


global layers_list
layers_list = {}

# Mother Class:
class Layers(object):

    def __init__(self, root, id, tag):
        self.id = id
        self.root = root
        self.tag = tag

# Children Classes:
class In_layer(Layers):

    def __init__(self, width, heigth, pix_type):
        self.width = width
        self.heigth = heigth
        self.pix_type = pix_type

class Conv2D_layer(Layers):

    def __init__(self, filters, k_size_x, k_size_y):
        self.filters = filters
        self.k_size_x = k_size_x
        self.k_size_y = k_size_y
        
class Dense_layer(Layers):

    def __init__(self, neurons):
        self.neurons = neurons

class MaxPooling_layer(Layers):

    def __init__(self, p_size_x, p_size_y, stride_x, stride_y):
        self.p_size_x = p_size_x
        self.p_size_y = p_size_y
        self.stride_x = stride_x
        self.stride_y = stride_y

class Out_layer(Layers):

    def __init__(self, out_nb, out_type):
        self.out_nb = out_nb
        self.out_type = out_type

class Dropout_layer(Layers):

    def __init__(self, ratio):
        self.ratio = ratio
        
