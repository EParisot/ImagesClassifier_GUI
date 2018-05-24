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

from srcs.layers import layers_list

class ThirdTab(object):

    def __init__(self, app):
        self.app = app

        self.saved = False
        
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
        self.max_p_layer_pic = ImageTk.PhotoImage(Image.open('assets/hidden_layer4.png'))
        self.out_layer_pic = ImageTk.PhotoImage(Image.open('assets/out_layer3.png'))
        self.sig_activation_pic = ImageTk.PhotoImage(Image.open('assets/sig_activation.png'))
        self.relu_activation_pic = ImageTk.PhotoImage(Image.open('assets/relu_activation.png'))
        self.max_activation_pic = ImageTk.PhotoImage(Image.open('assets/softmax_activation.png'))
        self.dropout_pic = ImageTk.PhotoImage(Image.open('assets/dropout.png'))
        self.load_pic = ImageTk.PhotoImage(Image.open('assets/dir_open.png'))
        self.save_pic = ImageTk.PhotoImage(Image.open('assets/save.png'))
        self.clear_pic = ImageTk.PhotoImage(Image.open('assets/pass.png'))

        self.photo_label = Label(self.model_frame, image=self.input_pic)
        self.photo_label.grid(row=0, column=0, padx=20, pady=10, stick='e')

        self.model_canvas = Canvas(self.model_frame)
        self.model_canvas.bind("<Enter>", self.modified)
        self.model_canvas_dnd = dnd.DnD_Container(self.app, self.model_frame, self.model_canvas)
        self.model_canvas.config(borderwidth=2, relief="sunken", height=400, width=900)
        self.model_canvas.grid(row=0, column=1, padx=20, pady=10, sticky="w")
        self.model_canvas.grid_propagate(0)

        command_frame = Frame(self.model_frame)
        command_frame.grid(row=0, column=2, sticky='nsw')
        command_frame.grid_rowconfigure(0, weight=1)
        command_frame.grid_rowconfigure(1, weight=1)
        command_frame.grid_rowconfigure(2, weight=1)
        command_frame.grid_columnconfigure(0, weight=1)
        command_frame.grid_columnconfigure(1, weight=1)

        load_handler = lambda: self.load(self)
        save_handler = lambda: self.save(self)
        clear_handler = lambda: self.clear(self)

        load_but = Button(command_frame)
        load_but.config(image=self.load_pic, command=load_handler)
        load_but.grid(row=0, column=1, padx=10, pady=10)
        load_but = ttp.ToolTip(load_but, 'Load Model', msgFunc=None, delay=1, follow=True)

        save_but = Button(command_frame)
        save_but.config(image=self.save_pic, command=save_handler)
        save_but.grid(row=1, column=1, padx=10, pady=10)
        save_but = ttp.ToolTip(save_but, 'Save Model', msgFunc=None, delay=1, follow=True)

        clear_but = Button(command_frame)
        clear_but.config(image=self.clear_pic, command=clear_handler)
        clear_but.grid(row=2, column=0, pady=10, sticky="sw")
        clear_but = ttp.ToolTip(clear_but, 'Clear Model', msgFunc=None, delay=1, follow=True)

        self.layers_canvas = Canvas(self.model_frame)
        self.layers_canvas_dnd = dnd.DnD_Container(self.app, self.model_frame, self.layers_canvas)
        self.layers_canvas.config(borderwidth=2, relief="sunken", height=235, width=600)
        self.layers_canvas.grid(row=1, column=1, padx=20, pady=10)
        self.layers_canvas.grid_propagate(0)

        self.trash_canvas = Canvas(self.model_frame)
        self.trash_canvas.config(borderwidth=2, relief="groove", height=200, width=200)
        self.trash_canvas.create_image(108, 105, image=self.trash_pic)
        self.trash_dnd = dnd.DnD_Container(self.app, self.model_frame, self.trash_canvas)
        self.trash_canvas.grid(row=1, column=2, padx=20, pady=20, stick='w')
        self.trash_canvas.grid_propagate(0)

        self.in_layer = dnd.Icon(self.app, self.in_layer_pic, ("In", "layer"))
        self.in_layer.attach(self.layers_canvas)

        self.conv2d_layer = dnd.Icon(self.app, self.conv2d_layer_pic, ("Conv2d", "layer"))
        self.conv2d_layer.attach(self.layers_canvas, x=70)

        self.max_p_layer = dnd.Icon(self.app, self.max_p_layer_pic, ("Max_pooling", "layer"))
        self.max_p_layer.attach(self.layers_canvas, x=130)

        self.flatten_layer = dnd.Icon(self.app, self.flatten_layer_pic, ("Flatten", "layer"))
        self.flatten_layer.attach(self.layers_canvas, x=190)

        self.dense_layer = dnd.Icon(self.app, self.dense_layer_pic, ("Dense", "layer"))
        self.dense_layer.attach(self.layers_canvas, x=250)

        self.out_layer = dnd.Icon(self.app, self.out_layer_pic, ("Out", "layer"))
        self.out_layer.attach(self.layers_canvas, x=310)

        self.relu_activation = dnd.Icon(self.app, self.relu_activation_pic, ("Relu", "activation"))
        self.relu_activation.attach(self.layers_canvas, x=370)

        self.sig_activation = dnd.Icon(self.app, self.sig_activation_pic, ("Sigmoid", "activation"))
        self.sig_activation.attach(self.layers_canvas, x=430)

        self.max_activation = dnd.Icon(self.app, self.max_activation_pic, ("Softmax", "activation"))
        self.max_activation.attach(self.layers_canvas, x=490)

        self.dropout = dnd.Icon(self.app, self.dropout_pic, ("Dropout", "activation"))
        self.dropout.attach(self.layers_canvas, x=550)

    def clear(self, event):
        if self.saved == False:
            res = askquestion("Clear Model", "Modifications not saved, \nare you sure ?", icon='warning')
            if res == 'yes':
                self.model_canvas.delete("all")
                layers_list = {}
        else:
            self.model_canvas.delete("all")

    def parse(self, filename):
        pass

    def load(self, event):
        filename =  askopenfilename(title = "Select Model",filetypes = (("json files","*.json"),("all files","*.*")))
        if filename is not None:
            self.parse(filename)

    def write(self, filename):
        pass
    
    def save(self, event):
        filename = asksaveasfilename(title = "Save Model",filetypes = (("json files","*.json"),("all files","*.*")))
        if filename is not None:
            self.saved = True
            self.write(filename)

    def modified(self, event):
        self.saved = False
