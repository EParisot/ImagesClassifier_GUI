# -*- coding: utf-8 -*-

from srcs.const import *
import sys

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter.scrolledtext import ScrolledText

from PIL import Image, ImageTk

import os
import configparser
from time import time, localtime, strftime, sleep

import srcs.Tk_Tooltips as ttp

import json

class FourthTab(object):

    def __init__(self, app, devMode):
        self.app = app
        self.devMode = devMode
        self.model = None
        self.model_filename = None
        self.input_shape = None
        self.dataset_dir = None
        
        self.train_frame = Frame(app.fourth_tab)
        self.train_frame.grid(row=0, column=0, stick='n')
        self.train_frame.grid_columnconfigure(0, weight=1)
        self.train_frame.grid_rowconfigure(0, weight=1)

        command_frame = Frame(self.train_frame)
        command_frame.grid(row=0, column=0, sticky='nw')
        command_frame.grid_rowconfigure(0, weight=1)
        command_frame.grid_columnconfigure(0, weight=1)
        command_frame.grid_columnconfigure(1, weight=1)
        command_frame.grid_columnconfigure(2, weight=1)

        self.load_dataset_pic = ImageTk.PhotoImage(Image.open('assets/dir_open.png'))
        self.load_model_pic = ImageTk.PhotoImage(Image.open('assets/import.png'))


        load_dataset_handler = lambda: self.load_dataset(self)
        
        load_dataset_but = Button(command_frame)
        load_dataset_but.config(image=self.load_dataset_pic, command=load_dataset_handler)
        load_dataset_but.grid(row=0, column=0, padx=10, pady=10)
        load_dataset_ttp = ttp.ToolTip(load_dataset_but, 'Select Dataset folder', msgFunc=None, delay=1, follow=True)
        
        load_model_handler = lambda: self.load_model(self)
        
        load_model_but = Button(command_frame)
        load_model_but.config(image=self.load_model_pic, command=load_model_handler)
        load_model_but.grid(row=0, column=1, padx=10, pady=10)
        load_model_ttp = ttp.ToolTip(load_model_but, 'Import Model', msgFunc=None, delay=1, follow=True)
                

    def load_dataset(self, event):
        dataset_dir =  askdirectory(title = "Select Dataset folder")
        if dataset_dir:
            self.dataset_dir = dataset_dir
            # Load labels and normalise pictures

    def load_model(self, event):
        if self.dataset_dir:
            self.model_filename =  askopenfilename(title = "Select Model", filetypes = (("h5py files","*.h5py"),("all files","*.*")))
            if self.model_filename:
                from keras.models import load_model
                self.model = load_model(self.model_filename)
                if self.devMode == True:
                    model_dict = json.loads(self.model.to_json())
                    self.input_shape = model_dict['config'][0]['config']['batch_input_shape']
                    # Compile model
        else:
            showwarning("Error", "Load a dataset before you compile model.");
