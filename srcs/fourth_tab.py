# -*- coding: utf-8 -*-

from srcs.const import *
import sys
#import threading

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

##import matplotlib
##matplotlib.use("TkAgg")
##from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
##from matplotlib.figure import Figure

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
        self.train_frame.grid_columnconfigure(1, weight=1)
        self.train_frame.grid_rowconfigure(0, weight=1)
        self.train_frame.grid_rowconfigure(1, weight=1)

        command_frame = Frame(self.train_frame)
        command_frame.grid(row=0, column=1, sticky='nw')
        command_frame.grid_rowconfigure(0, weight=1)
        command_frame.grid_rowconfigure(1, weight=1)
        command_frame.grid_rowconfigure(2, weight=1)
        command_frame.grid_columnconfigure(0, weight=1)
        command_frame.grid_columnconfigure(1, weight=1)
        command_frame.grid_columnconfigure(2, weight=1)
        command_frame.grid_columnconfigure(3, weight=1)
        command_frame.grid_columnconfigure(4, weight=1)
        command_frame.grid_columnconfigure(5, weight=1)
        command_frame.grid_columnconfigure(6, weight=1)

        self.load_dataset_pic = ImageTk.PhotoImage(Image.open('assets/dir_open.png'))
        self.load_model_pic = ImageTk.PhotoImage(Image.open('assets/import.png'))
        self.labo_photos_pic = ImageTk.PhotoImage(Image.open('assets/edit_pic.png'))
        self.resize_pic = ImageTk.PhotoImage(Image.open('assets/resize.png'))
        self.crop_pic = ImageTk.PhotoImage(Image.open('assets/crop.png'))
        self.train_model_pic = ImageTk.PhotoImage(Image.open('assets/brain.png'))
        self.accolade_pic = ImageTk.PhotoImage(Image.open('assets/accolade.png'))
        self.accolade_v1_pic = ImageTk.PhotoImage(Image.open('assets/accolade_v1.png'))
        self.accolade_v2_pic = ImageTk.PhotoImage(Image.open('assets/accolade_v2.png'))
        self.ok_pic = ImageTk.PhotoImage(Image.open('assets/ok.png'))
        self.nok_pic = ImageTk.PhotoImage(Image.open('assets/nok.png'))
        self.stop_pic = ImageTk.PhotoImage(Image.open('assets/pass.png'))

        load_dataset_handler = lambda: self.load_dataset(self)
        self.load_dataset_but = Button(command_frame)
        self.load_dataset_but.config(image=self.load_dataset_pic, command=load_dataset_handler)
        self.load_dataset_but.grid(row=0, column=0, padx=10, pady=5)
        self.load_dataset_ttp = ttp.ToolTip(self.load_dataset_but, 'Select Dataset folder', msgFunc=None, delay=1, follow=True)

        accolade_v1_label = Label(command_frame, image=self.accolade_v1_pic)
        accolade_v1_label.grid(row=0, column=1, sticky="nsew")

        checks_label = Label(command_frame)
        checks_label.grid(row=0, column=2, sticky='nwe', pady=10)
        checks_label.grid_rowconfigure(0, weight=1)
        checks_label.grid_rowconfigure(1, weight=1)
        checks_label.grid_rowconfigure(2, weight=1)
        checks_label.grid_rowconfigure(3, weight=1)
        checks_label.grid_columnconfigure(0, weight=1)
        checks_label.grid_columnconfigure(1, weight=1)
        checks_label.grid_columnconfigure(2, weight=1)

        w_label = Label(checks_label, text="W :", font=("Helvetica", 16))
        w_label.grid(row=0, column=0, sticky='nwe')
        h_label = Label(checks_label, text="H :", font=("Helvetica", 16))
        h_label.grid(row=1, column=0, sticky='nwe')
        pix_label = Label(checks_label, text="Colors :", font=("Helvetica", 16))
        pix_label.grid(row=2, column=0, sticky='nwe')
        out_label = Label(checks_label, text="Classes :", font=("Helvetica", 16))
        out_label.grid(row=3, column=0, sticky='nwe')

        self.w_in = StringVar()
        self.h_in = StringVar()
        self.pix_in = StringVar()
        self.out_dataset = StringVar()

        w_in = Label(checks_label, textvariable=self.w_in, font=("Helvetica", 16), borderwidth=2, relief="ridge", width=5)
        w_in.grid(row=0, column=1, sticky='nwe', padx=5)
        h_in = Label(checks_label, textvariable=self.h_in, font=("Helvetica", 16), borderwidth=2, relief="ridge", width=5)
        h_in.grid(row=1, column=1, sticky='nwe', padx=5)
        pix_in = Label(checks_label, textvariable=self.pix_in, font=("Helvetica", 16), borderwidth=2, relief="ridge", width=5)
        pix_in.grid(row=2, column=1, sticky='nwe', padx=5)
        out_dataset = Label(checks_label, textvariable=self.out_dataset, font=("Helvetica", 16), borderwidth=2, relief="ridge", width=5)
        out_dataset.grid(row=3, column=1, sticky='nwe', padx=5)

        self.w_out = StringVar()
        self.h_out = StringVar()
        self.pix_out = StringVar()
        self.out_model = StringVar()

        w_out = Label(checks_label, textvariable=self.w_out, font=("Helvetica", 16), borderwidth=2, relief="ridge", width=5)
        w_out.grid(row=0, column=2, sticky='nwe', padx=5)
        h_out = Label(checks_label, textvariable=self.h_out, font=("Helvetica", 16), borderwidth=2, relief="ridge", width=5)
        h_out.grid(row=1, column=2, sticky='nwe', padx=5)
        pix_out = Label(checks_label, textvariable=self.pix_out, font=("Helvetica", 16), borderwidth=2, relief="ridge", width=5)
        pix_out.grid(row=2, column=2, sticky='nwe', padx=5)
        out_model = Label(checks_label, textvariable=self.out_model, font=("Helvetica", 16), borderwidth=2, relief="ridge", width=5)
        out_model.grid(row=3, column=2, sticky='nwe', padx=5)

        accolade_v2_label = Label(command_frame, image=self.accolade_v2_pic)
        accolade_v2_label.grid(row=0, column=3, sticky="nsew")

        labo_photos_handler = lambda: self.labo_photos(self.images)
        self.labo_photos_but = Button(command_frame)
        self.labo_photos_but.config(image=self.labo_photos_pic, command=labo_photos_handler, state="disabled")
        self.labo_photos_but.grid(row=1, column=0, padx=10, pady=5, sticky="n")
        self.labo_photos_ttp = ttp.ToolTip(self.labo_photos_but, 'Crop pictures', msgFunc=None, delay=1, follow=True)
        
        self.check_label = Label(command_frame)
        self.check_label.grid(row=1, column=2, padx=10, pady=5, sticky="ne")

        self.check = BooleanVar()
        self.check.set(False)
        
        load_model_handler = lambda: self.load_model(self)
        self.load_model_but = Button(command_frame)
        self.load_model_but.config(image=self.load_model_pic, command=load_model_handler, state="disabled")
        self.load_model_but.grid(row=0, column=4, padx=10, pady=10)
        self.load_model_ttp = ttp.ToolTip(self.load_model_but, 'Import Model', msgFunc=None, delay=1, follow=True)

        train_label = Label(command_frame)
        train_label.grid(row=2, column=5, sticky="n")
        train_label.grid_rowconfigure(0, weight=1)
        train_label.grid_columnconfigure(0, weight=1)
        train_label.grid_columnconfigure(1, weight=1)
                
        train_handler = lambda: self.train_model(self)
        self.train_model_but = Button(train_label)
        self.train_model_but.config(image=self.train_model_pic, command=train_handler, state="disabled")
        self.train_model_but.grid(row=0, column=0, padx=10, pady=5, sticky="n")
        self.train_model_ttp = ttp.ToolTip(self.train_model_but, 'Train Model', msgFunc=None, delay=1, follow=True)  

        hyper_param_frame = Frame(command_frame, borderwidth=2, relief="sunken")
        hyper_param_frame.grid(row=0, column=5, sticky='nw', padx=5, pady=10)
        hyper_param_frame.grid_rowconfigure(0, weight=1)
        hyper_param_frame.grid_rowconfigure(1, weight=1)
        hyper_param_frame.grid_columnconfigure(0, weight=1)
        hyper_param_frame.grid_columnconfigure(1, weight=1)
        hyper_param_frame.grid_columnconfigure(2, weight=1)
        hyper_param_frame.grid_columnconfigure(3, weight=1)
        hyper_param_frame.grid_columnconfigure(4, weight=1)

        batch_label = Label(hyper_param_frame, text="Batch size :", font=("Helvetica", 16), borderwidth=2, relief="ridge")
        batch_label.grid(row=0, column=0, padx=5, pady=5)
        self.batch = StringVar()
        self.batch.set("1")
        batch_entry = Entry(hyper_param_frame, textvariable=self.batch, justify="center", width=10)
        batch_entry.grid(row=1, column=0, padx=5, pady=5)

        epochs_label = Label(hyper_param_frame, text="Epochs :", font=("Helvetica", 16), borderwidth=2, relief="ridge")
        epochs_label.grid(row=0, column=1, padx=5, pady=5)
        self.epochs = StringVar()
        self.epochs.set("1")
        epochs_entry = Entry(hyper_param_frame, textvariable=self.epochs, justify="center", width=10)
        epochs_entry.grid(row=1, column=1, padx=5, pady=5)

        split_label = Label(hyper_param_frame, text="Validation Split :", font=("Helvetica", 16), borderwidth=2, relief="ridge")
        split_label.grid(row=0, column=2, padx=5, pady=5)
        self.split = StringVar()
        self.split.set("0.1")
        split_entry = Entry(hyper_param_frame, textvariable=self.split, justify="center", width=10)
        split_entry.grid(row=1, column=2, padx=5, pady=5)

        stop_label = Label(hyper_param_frame, text="Early stop :", font=("Helvetica", 16), borderwidth=2, relief="ridge")
        stop_label.grid(row=0, column=3, padx=5, pady=5)
        self.stop_on = IntVar()
        self.stop_on.set(0)
        stop_check = Checkbutton(hyper_param_frame, variable=self.stop_on, command=self.grey_patience)
        stop_check.grid(row=1, column=3, padx=5, pady=5)

        patience_label = Label(hyper_param_frame, text="Patience :", font=("Helvetica", 16), borderwidth=2, relief="ridge")
        patience_label.grid(row=0, column=4, padx=5, pady=5)
        self.patience = StringVar()
        self.patience.set("1")
        self.patience_entry = Entry(hyper_param_frame, textvariable=self.patience, justify="center", width=10, state="disabled")
        self.patience_entry.grid(row=1, column=4, padx=5, pady=5)

        accolade_label = Label(command_frame, image=self.accolade_pic)
        accolade_label.grid(row=1, column=5, sticky="new")


    def grey_patience(self):
        if self.stop_on.get() == 1:
            self.stop_entry.config(state="normal")
        else:
            self.stop_entry.config(state="disabled")

    def load_dataset(self, event):
        dataset_dir =  askdirectory(title = "Select Dataset folder")
        if dataset_dir:
            self.app.config(cursor="wait")
            self.app.update()
            self.dataset_dir = dataset_dir
            # Load images and labels
            self.images, self.labels = self.load_data(self.dataset_dir)
            nb_images = len(self.images)
            if nb_images == 0:
                showwarning('Error', 'No Images found in %s' % dataset_dir)
                self.app.config(cursor="")
                return
            
            #normalise datas
            self.images = np.array(self.images)
            self.images /= 255
    
            #convert labels to dummy values
            self.labels = np.array(self.labels)
            self.labels = np.array(pd.get_dummies(self.labels))

            # show images and out dim
            self.w_in.set(str(self.images.shape[2]))
            self.h_in.set(str(self.images.shape[1]))
            self.pix_in.set(str(self.images.shape[3]))
            self.out_dataset.set(str(self.labels.shape[1]))
            self.check_model()
            
            showinfo('Success', '%d Images and labels loaded' % nb_images)
            self.app.config(cursor="")
            self.labo_photos_but.config(state="normal")
            self.load_model_but.config(state="normal")


    def load_data(self, directory):
        from keras.preprocessing.image import load_img
        from keras.preprocessing.image import img_to_array
        images = []
        labels = []
        for name in os.listdir(directory):
            if name.endswith(EXT_PHOTOS):
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

    def labo_photos(self, images):
        if self.dataset_dir and len(self.images) > 0:

            self.labo_photos_frame = tk.Toplevel()
            self.labo_photos_frame.geometry("%dx%d+%d+%d" % (SNAP_W + 100, SNAP_H + 200, self.app.winfo_x(), self.app.winfo_y()))
            self.labo_photos_frame.title("PhotoLab")
            self.labo_photos_frame.transient(self.app)
            self.labo_photos_frame.grab_set()

            first_pic = None
            i = 0
            while i + 1 < len(os.listdir(self.dataset_dir)) and not os.listdir(self.dataset_dir)[i].endswith(EXT_PHOTOS):
                i = i + 1
            first_pic = os.listdir(self.dataset_dir)[i]
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
            if self.app.second_tab.h1.get():
                h1.set(self.app.second_tab.h1.get())
                self.h1_id = self.pic_canvas.create_rectangle(0, h1.get(), pic.size[0], 0, fill="")
            else:
                h1.set(0)
            self.h1_id = None
            h2 = IntVar()
            if self.app.second_tab.h2.get():
                h2.set(self.app.second_tab.h2.get())
                self.h2_id = self.pic_canvas.create_rectangle(0, h2.get(), pic.size[0], pic.size[1], fill="")
            else:
                h2.set(self.images.shape[1])
            self.h2_id = None
            w1 = IntVar()
            if self.app.second_tab.w1.get():
                w1.set(self.app.second_tab.w1.get())
                self.w1_id = self.pic_canvas.create_rectangle(w1.get(), 0, 0, pic.size[1], fill="")
            else:
                w1.set(0)
            self.w1_id = None
            w2 = IntVar()
            if self.app.second_tab.w2.get():
                w2.set(self.app.second_tab.w2.get())
                self.w2_id = self.pic_canvas.create_rectangle(w2.get(), 0, pic.size[0], pic.size[1], fill="")
            else:
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
        if h1 < self.images.shape[1] and h1 < self.images.shape[1] and w1 < self.images.shape[2] and w2 < self.images.shape[2]:
            # crop images
            self.images = self.images[:, h1:h2, w1:w2, :]
            
            # update images dim
            self.w_in.set(str(self.images.shape[2]))
            self.h_in.set(str(self.images.shape[1]))
            self.pix_in.set(str(self.images.shape[3]))
            self.check_model()
            
            self.labo_photos_frame.destroy()
            self.labo_photos_but.config(state="disabled")
            showinfo("Cropped Images", "Images datas have been croped \n New size = %d x %d\n(your images are still complete on disk...)" % (self.images.shape[2], self.images.shape[1]));

    def load_model(self, event):
        if self.dataset_dir:
            self.model_filename =  askopenfilename(title = "Select Model", filetypes = (("h5py files","*.h5py"),("all files","*.*")))
            if self.model_filename:
                import keras
                from keras.models import load_model
                self.model = load_model(self.model_filename)
                self.train_model_but.config(state="normal")

                # show model input_dim
                model_dict = json.loads(self.model.to_json())
                self.input_shape = model_dict['config'][0]['config']['batch_input_shape']
                self.w_out.set(str(self.input_shape[2]))
                self.h_out.set(str(self.input_shape[1]))
                self.pix_out.set(str(self.input_shape[3]))
                self.out_model.set(str(self.model.layers[-1].get_output_at(0).get_shape().as_list()[1]))
                self.check_model()
                
                showinfo("Model Loaded", "Model '%s' loaded" % (self.model_filename.split('/')[-1]))
        else:
            showwarning("Error", "Load a dataset before you import a model");

    def check_model(self):
        try:
            if int(self.w_in.get()) != int(self.w_out.get()) or \
                            int(self.h_in.get()) != int(self.h_out.get()) or \
                            int(self.pix_in.get()) != int(self.pix_out.get()) or \
                            int(self.out_dataset.get()) != int(self.out_model.get()):
                self.check_label.config(image=self.nok_pic)
                self.check_label.image = self.nok_pic
                self.check.set(False)
            else:
                self.check_label.config(image=self.ok_pic)
                self.check_label.image = self.ok_pic
                self.check.set(True)
        except ValueError:
            pass

    def train_model(self, event):
        if self.check.get() is True:
            if self.devMode:
                verbose = 1
                self.model.summary()
            try:
                batch = int(self.batch.get())
                if batch <= 0 :
                    showwarning("Error", "Null or negative batch size value")
                    return
                epochs = int(self.epochs.get())
                if epochs <= 0 :
                    showwarning("Error", "Null or negative epochs value")
                    return
                split = round(float(self.split.get()), 2)
                if split <= 0 :
                    showwarning("Error", "Null or negative split value")
                    return
                patience = int(self.patience.get())
                if patience <= 0 :
                    showwarning("Error", "Null or negative patience value")
                    return
            except ValueError:
                showwarning("Error", "Wrong hyper-parameter value")
                return

            import keras
            import keras.backend as K
            
            #from srcs.keras_classes import CustomModelCheckPoint
            #checkpoint = CustomModelCheckPoint(graph=self.graph, canvas=self.graph_canvas)

            early_stop = None
            if self.stop_on.get() == 1:
                early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', min_delta=0, patience=patience, verbose=0, mode='auto', baseline=None)
                callbacks = [early_stop]
            else:
                callbacks = None
            
            history = self.model.fit(self.images, self.labels, batch_size=batch, epochs=epochs, validation_split=split, callbacks=callbacks, verbose=verbose)


        else:
            showwarning("Error", "Incompatible model / dataset")

