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

from PIL import Image, ImageTk

import srcs.Tk_Tooltips as ttp
import srcs.Tk_DragnDrop as dnd

class ThirdTab(object):

    def __init__(self, app):
        self.app = app
        self.model_frame = Frame(app.third_tab)
        self.model_frame.grid(row=0, column=0, stick='n')
        self.model_frame.grid_columnconfigure(0, weight=1)
        self.model_frame.grid_columnconfigure(1, weight=1)
        self.model_frame.grid_columnconfigure(2, weight=1)
        self.model_frame.grid_rowconfigure(0, weight=1)
        self.model_frame.grid_rowconfigure(1, weight=1)

        self.input_pic = ImageTk.PhotoImage(Image.open('assets/photo.png'))
        self.trash_pic = ImageTk.PhotoImage(Image.open('assets/trash.png'))
        self.in_layer_pic = ImageTk.PhotoImage(Image.open('assets/in_layer.png'))
        self.conv2d_layer_pic = ImageTk.PhotoImage(Image.open('assets/hidden_layer1.png'))
        self.dense_layer_pic = ImageTk.PhotoImage(Image.open('assets/hidden_layer2.png'))
        self.flatten_layer_pic = ImageTk.PhotoImage(Image.open('assets/hidden_layer3.png'))
        self.out_layer_pic = ImageTk.PhotoImage(Image.open('assets/out_layer3.png'))
        self.sig_activation_pic = ImageTk.PhotoImage(Image.open('assets/sig_activation.png'))
        self.relu_activation_pic = ImageTk.PhotoImage(Image.open('assets/relu_activation.png'))

        self.photo_label = Label(self.model_frame, image=self.input_pic)
        self.photo_label.grid(row=0, column=0, padx=20, pady=20, stick='e')

        self.model_canvas = Canvas(self.model_frame)
        self.model_canvas_dnd = dnd.DnD_Container(self.model_frame, self.model_canvas, tk)
        self.model_canvas.config(borderwidth=2, relief="sunken", height=400, width=800)
        self.model_canvas.grid(row=0, column=1, padx=20, pady=20, sticky="w")
        self.model_canvas.grid_propagate(0)

        self.layers_canvas = Canvas(self.model_frame)
        self.layers_canvas_dnd = dnd.DnD_Container(self.model_frame, self.layers_canvas, tk)
        self.layers_canvas.config(borderwidth=2, relief="sunken", height=300, width=600)
        self.layers_canvas.grid(row=1, column=1, padx=20, pady=20)
        self.layers_canvas.grid_propagate(0)

        self.trash_canvas = Canvas(self.model_frame)
        self.trash_canvas.config(borderwidth=2, relief="groove", height=200, width=200)
        self.trash_canvas.create_image(108, 105, image=self.trash_pic)
        self.trash_dnd = dnd.DnD_Container(self.model_frame, self.trash_canvas, tk)
        self.trash_canvas.grid(row=1, column=2, padx=20, pady=20, stick='w')
        self.trash_canvas.grid_propagate(0)

        self.in_layer = dnd.Icon(self.app, self.in_layer_pic, tk)
        self.in_layer.attach(self.layers_canvas)

        self.conv2d_layer = dnd.Icon(self.app, self.conv2d_layer_pic, tk)
        self.conv2d_layer.attach(self.layers_canvas, x=70)

        self.flatten_layer = dnd.Icon(self.app, self.flatten_layer_pic, tk)
        self.flatten_layer.attach(self.layers_canvas, x=130)

        self.dense_layer = dnd.Icon(self.app, self.dense_layer_pic, tk)
        self.dense_layer.attach(self.layers_canvas, x=190)

        self.out_layer = dnd.Icon(self.app, self.out_layer_pic, tk)
        self.out_layer.attach(self.layers_canvas, x=250)

        self.sig_activation = dnd.Icon(self.app, self.sig_activation_pic, tk)
        self.sig_activation.attach(self.layers_canvas, x=310)

        self.relu_activation = dnd.Icon(self.app, self.relu_activation_pic, tk)
        self.relu_activation.attach(self.layers_canvas, x=370)
