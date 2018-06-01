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
import numpy as np
import pandas as pd

class FourthTab(object):

    def __init__(self, app, devMode):
        self.app = app
        self.devMode = devMode
        self.model = None
        self.model_filename = None
        self.input_shape = None
        self.dataset_dir = None
        self.images = None
        self.labels = None
        
        self.train_frame = Frame(app.fourth_tab)
        self.train_frame.grid(row=0, column=0, stick='nsew')
        self.train_frame.grid_columnconfigure(0, weight=1)
        self.train_frame.grid_rowconfigure(0, weight=1)

        command_frame = Frame(self.train_frame)
        command_frame.grid(row=0, column=0, sticky='nw')
        command_frame.grid_rowconfigure(0, weight=1)
        command_frame.grid_rowconfigure(1, weight=1)
        command_frame.grid_columnconfigure(0, weight=1)
        command_frame.grid_columnconfigure(1, weight=1)
        command_frame.grid_columnconfigure(2, weight=1)

        self.load_dataset_pic = ImageTk.PhotoImage(Image.open('assets/dir_open.png'))
        self.load_model_pic = ImageTk.PhotoImage(Image.open('assets/import.png'))
        self.labo_photos_pic = ImageTk.PhotoImage(Image.open('assets/edit_pic.png'))
        self.resize_pic = ImageTk.PhotoImage(Image.open('assets/resize.png'))
        self.crop_pic = ImageTk.PhotoImage(Image.open('assets/crop.png'))

        load_dataset_handler = lambda: self.load_dataset(self)
        
        self.load_dataset_but = Button(command_frame)
        self.load_dataset_but.config(image=self.load_dataset_pic, command=load_dataset_handler)
        self.load_dataset_but.grid(row=0, column=0, padx=10, pady=10)
        self.load_dataset_ttp = ttp.ToolTip(self.load_dataset_but, 'Select Dataset folder', msgFunc=None, delay=1, follow=True)

        labo_photos_handler = lambda: self.labo_photos(self.images)
        
        self.labo_photos_but = Button(command_frame)
        self.labo_photos_but.config(image=self.labo_photos_pic, command=labo_photos_handler, state="disabled")
        self.labo_photos_but.grid(row=0, column=1, padx=10, pady=10)
        self.labo_photos_ttp = ttp.ToolTip(self.labo_photos_but, 'Edit pictures', msgFunc=None, delay=1, follow=True)
        
        load_model_handler = lambda: self.load_model(self)
        
        self.load_model_but = Button(command_frame)
        self.load_model_but.config(image=self.load_model_pic, command=load_model_handler, state="disabled")
        self.load_model_but.grid(row=0, column=2, padx=10, pady=10)
        self.load_model_ttp = ttp.ToolTip(self.load_model_but, 'Import Model', msgFunc=None, delay=1, follow=True)
                

    def load_dataset(self, event):
        dataset_dir =  askdirectory(title = "Select Dataset folder")
        if dataset_dir:
            self.app.config(cursor="wait")
            self.app.update()
            self.dataset_dir = dataset_dir
            # Load images and labels
            self.images, self.labels = self.load_data(self.dataset_dir)
            nb_images = len(self.images)
            #normalise datas
            self.images = np.array(self.images)
            self.images /= 255
            
            #convert labels to dummy values
            self.labels = np.array(self.labels)
            self.labels = np.array(pd.get_dummies(self.labels))
            
            showinfo('Success', '%d Images and labels loaded' % nb_images)
            self.app.config(cursor="")
            self.labo_photos_but.config(state="normal")
            self.load_model_but.config(state="normal")

    def labo_photos(self, images):
        if self.dataset_dir and len(self.images) > 0:

            self.labo_photos_frame = tk.Toplevel()
            self.labo_photos_frame.geometry("%dx%d+%d+%d" % (SNAP_W + 100, SNAP_H + 200, self.app.winfo_x(), self.app.winfo_y()))
            self.labo_photos_frame.title("PhotoLab")
            self.labo_photos_frame.transient(self.app)
            self.labo_photos_frame.grab_set()

            first_pic = os.listdir(self.dataset_dir)[0]
            pic = Image.open(self.dataset_dir + '/' + first_pic)
            image = ImageTk.PhotoImage(pic)

            command_frame = Frame(self.labo_photos_frame)
            command_frame.grid(row=0, column=0, sticky='nw')
            command_frame.grid_rowconfigure(0, weight=1)
            command_frame.grid_rowconfigure(1, weight=1)
            command_frame.grid_columnconfigure(0, weight=1)
            command_frame.grid_columnconfigure(1, weight=1)
            command_frame.grid_columnconfigure(2, weight=1)

            self.pic_frame = Frame(command_frame)
            self.pic_frame.grid(row=0, column=1, sticky='nsew')
            self.pic_frame.grid_rowconfigure(0, weight=1)
            self.pic_frame.grid_rowconfigure(1, weight=1)
            self.pic_frame.grid_rowconfigure(2, weight=1)
            self.pic_frame.grid_columnconfigure(0, weight=1)
            self.pic_frame.grid_columnconfigure(1, weight=1)
            self.pic_frame.grid_columnconfigure(2, weight=1)

            self.pic_canvas = Canvas(self.pic_frame)
            self.pic_canvas.grid(row=1, column=1, sticky="nsew")
            canvas_image = self.pic_canvas.create_image(0, 0, image=image, anchor=NW)
            self.pic_canvas.image = image

            h1 = IntVar()
            h1.set(0)
            self.h1_id = None
            h2 = IntVar()
            h2.set(self.images.shape[1])
            self.h2_id = None
            w1 = IntVar()
            w1.set(0)
            self.w1_id = None
            w2 = IntVar()
            w2.set(self.images.shape[2])
            self.w2_id = None
            
            h1_handler = lambda _: self.draw_h1(h1.get(), pic.size[0])
            self.slide_height1 = Scale(self.pic_frame ,from_=0, to=pic.size[1], orient=VERTICAL, length=pic.size[1], variable=h1, command=h1_handler)
            self.slide_height1.grid(row=1, column=0, sticky="nse")

            h2_handler = lambda _: self.draw_h2(h2.get(), pic.size[0], pic.size[1])
            self.slide_height2 = Scale(self.pic_frame, from_=0, to=pic.size[1], orient=VERTICAL, length=pic.size[1], variable=h2, command=h2_handler)
            self.slide_height2.grid(row=1, column=2, sticky="nsw")

            w1_handler = lambda _: self.draw_w1(w1.get(), pic.size[1])
            self.slide_width1 = Scale(self.pic_frame ,from_=0, to=pic.size[0], orient=HORIZONTAL, length=pic.size[0], variable=w1, command=w1_handler)
            self.slide_width1.grid(row=0, column=1, sticky="sew")

            w2_handler = lambda _: self.draw_w2(w2.get(), pic.size[0], pic.size[1])
            self.slide_width2 = Scale(self.pic_frame, from_=0, to=pic.size[0], orient=HORIZONTAL, length=pic.size[0], variable=w2, command=w2_handler)
            self.slide_width2.grid(row=2, column=1, sticky="new")

            crop_handler = lambda : self.crop(h1.get(), h2.get(), w1.get(), w2.get())
            crop_but = Button(command_frame, image=self.crop_pic, command=crop_handler)
            crop_but.grid(row=1, column=1, pady=10, padx=10)

        else:
            showwarning("No images Error", "Load a dataset before cropping images");

    def draw_h1(self, h1, w):
        self.pic_canvas.delete(self.h1_id)
        self.h1_id = self.pic_canvas.create_rectangle(0, h1, w, 0, fill="")

    def draw_h2(self, h2, w, h):
        self.pic_canvas.delete(self.h2_id)
        self.h2_id = self.pic_canvas.create_rectangle(0, h2, w, h, fill="")

    def draw_w1(self, w1, h):
        self.pic_canvas.delete(self.w1_id)
        self.w1_id = self.pic_canvas.create_rectangle(w1, 0, 0, h, fill="")

    def draw_w2(self, w2, w, h):
        self.pic_canvas.delete(self.w2_id)
        self.w2_id = self.pic_canvas.create_rectangle(w2, 0, w, h, fill="")
        
    def crop(self, h1, h2, w1, w2):
        self.images = self.images[:, h1:h2, w1:w2, :]
        self.labo_photos_frame.destroy()
        showinfo("Cropped Images", "Images datas have been croped \n New size = %d x %d\n(your images are still complete on disk...)" % (self.images.shape[2], self.images.shape[1]));


    def load_data(self, directory):
        from keras.preprocessing.image import load_img
        from keras.preprocessing.image import img_to_array
        images = []
        labels = []
        for name in os.listdir(directory):
            filename = directory + '/' + name
            # load an image from file
            image = load_img(filename)
            # convert the image pixels to a numpy array
            image = img_to_array(image)
            # get image id + labels
            value = int(name.split('_')[0])
            labels.append(value)
            images.append(image)
        return images, labels

    def load_model(self, event):
        if self.dataset_dir:
            self.model_filename =  askopenfilename(title = "Select Model", filetypes = (("h5py files","*.h5py"),("all files","*.*")))
            if self.model_filename:
                import keras
                from keras.models import load_model
                self.model = load_model(self.model_filename)
                if self.devMode == True:
                    model_dict = json.loads(self.model.to_json())
                    self.input_shape = model_dict['config'][0]['config']['batch_input_shape']
        else:
            showwarning("Error", "Load a dataset before you import a model");
