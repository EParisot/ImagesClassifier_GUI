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

import json

class ThirdTab(object):

    def __init__(self, app):
        self.app = app

        self.saved = tk.BooleanVar()
        self.saved.set(False)
        
        self.model_frame = Frame(app.third_tab)
        self.model_frame.grid(row=0, column=0, stick='n')
        self.model_frame.grid_columnconfigure(0, weight=1)
        self.model_frame.grid_columnconfigure(1, weight=1)
        self.model_frame.grid_columnconfigure(2, weight=1)
        self.model_frame.grid_rowconfigure(0, weight=1)
        self.model_frame.grid_rowconfigure(1, weight=1)
        self.model_frame.grid_rowconfigure(2, weight=1)

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
        self.compile_pic = ImageTk.PhotoImage(Image.open('assets/stack.png'))
        self.logo_pic = ImageTk.PhotoImage(Image.open('assets/keras.jpeg'))
        self.clear_pic = ImageTk.PhotoImage(Image.open('assets/pass.png'))

        self.photo_label = Label(self.model_frame, image=self.input_pic)
        self.photo_label.grid(row=0, column=0, padx=20, pady=10, stick='e')

        self.model_canvas = Canvas(self.model_frame)
        self.model_canvas.bind("<ButtonPress>", self.modified)
        self.model_canvas_dnd = dnd.DnD_Container(self.app, self.model_frame, self.model_canvas)
        self.model_canvas.config(borderwidth=2, relief="sunken", height=MODEL_H, width=MODEL_W)
        self.model_canvas.grid(row=0, column=1, padx=20, pady=10, sticky="w")
        self.model_canvas.grid_propagate(0)

        command_frame = Frame(self.model_frame)
        command_frame.grid(row=0, column=2, sticky='nsw')
        command_frame.grid_rowconfigure(0, weight=1)
        command_frame.grid_rowconfigure(1, weight=1)
        command_frame.grid_rowconfigure(2, weight=1)
        command_frame.grid_rowconfigure(3, weight=1)
        command_frame.grid_columnconfigure(0, weight=1)
        command_frame.grid_columnconfigure(1, weight=1)
        command_frame.grid_columnconfigure(2, weight=1)

        load_handler = lambda: self.load(self)
        save_handler = lambda: self.save(self)
        clear_handler = lambda: self.clear(self)
        compile_handler = lambda: self.compile(self)

        load_but = Button(command_frame)
        load_but.config(image=self.load_pic, command=load_handler)
        load_but.grid(row=0, column=1, padx=10, pady=10)
        load_but = ttp.ToolTip(load_but, 'Load Model', msgFunc=None, delay=1, follow=True)

        save_but = Button(command_frame)
        save_but.config(image=self.save_pic, command=save_handler)
        save_but.grid(row=1, column=1, padx=10, pady=10)
        save_but = ttp.ToolTip(save_but, 'Save Model', msgFunc=None, delay=1, follow=True)

        compile_but = Button(command_frame)
        compile_but.config(image=self.compile_pic, command=compile_handler)
        compile_but.grid(row=1, column=2, padx=10, pady=10)
        compile_but = ttp.ToolTip(compile_but, 'Compile Model', msgFunc=None, delay=1, follow=True)

        powered_label = Label(command_frame, text="powered by:")
        powered_label.grid(row=2, column=2, sticky="sew")

        logo_label = Label(command_frame, image=self.logo_pic)
        logo_label.grid(row=3, column=2, sticky="ne")

        clear_but = Button(command_frame)
        clear_but.config(image=self.clear_pic, command=clear_handler)
        clear_but.grid(row=3, column=0, pady=10, sticky="sw")
        clear_but = ttp.ToolTip(clear_but, 'Clear Model', msgFunc=None, delay=1, follow=True)

        info = Label(self.model_frame, text="^ Drag layers ^").grid(row=1, column=1)

        self.layers_canvas = Canvas(self.model_frame)
        self.layers_canvas_dnd = dnd.DnD_Container(self.app, self.model_frame, self.layers_canvas)
        self.layers_canvas.config(borderwidth=2, relief="sunken", height=235, width=600)
        self.layers_canvas.grid(row=2, column=1, padx=20, pady=10)
        self.layers_canvas.grid_propagate(0)

        self.trash_canvas = Canvas(self.model_frame)
        self.trash_canvas.config(borderwidth=2, relief="groove", height=200, width=200)
        self.trash_canvas.create_image(108, 105, image=self.trash_pic)
        self.trash_dnd = dnd.DnD_Container(self.app, self.model_frame, self.trash_canvas)
        self.trash_canvas.grid(row=2, column=2, padx=20, pady=20, stick='w')
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
                self.app.layers_list = {}
        else:
            self.model_canvas.delete("all")

    def load(self, event):
        filename =  askopenfilename(title = "Select Model",filetypes = (("json files","*.json"),("all files","*.*")))
        if filename:
            with open(filename, 'r') as infile:
                if self.app.layers_list:
                    res = askquestion("Load Model", "This action will overwrite existing model \n Load anyway ?", icon='warning')
                    if res == 'no':
                        return
                data = json.load(infile)
                self.model_canvas.delete("all")
                self.app.layers_list = {}
                self.parse(data)
                self.saved.set(True)

    def parse(self, data):
        for item in data:

            if data[item]['tag'] == "In":
                self.new_in_layer = dnd.Icon(self.app, self.in_layer_pic, ("In", "layer"))
                self.new_in_layer.attach(self.model_canvas, data[item]['x'], data[item]['y'])
                self.app.layers_list[self.new_in_layer.id] = data[item]
                
            elif data[item]['tag'] == "Conv2d":
                self.new_conv2d_layer = dnd.Icon(self.app, self.conv2d_layer_pic, ("Conv2d", "layer"))
                self.new_conv2d_layer.attach(self.model_canvas, data[item]['x'], data[item]['y'])
                self.app.layers_list[self.new_conv2d_layer.id] = data[item]
                
            elif data[item]['tag'] == "Max_Pooling":
                self.new_max_p_layer = dnd.Icon(self.app, self.max_p_layer_pic, ("Max_pooling", "layer"))
                self.new_max_p_layer.attach(self.model_canvas, data[item]['x'], data[item]['y'])
                self.app.layers_list[self.new_max_p_layer.id] = data[item]

            elif data[item]['tag'] == "Flatten":
                self.new_flatten_layer = dnd.Icon(self.app, self.flatten_layer_pic, ("Flatten", "layer"))
                self.new_flatten_layer.attach(self.model_canvas, data[item]['x'], data[item]['y'])
                self.app.layers_list[self.new_flatten_layer.id] = data[item]
                
            elif data[item]['tag'] == "Dense":
                self.new_dense_layer = dnd.Icon(self.app, self.dense_layer_pic, ("Dense", "layer"))
                self.new_dense_layer.attach(self.model_canvas, data[item]['x'], data[item]['y'])
                self.app.layers_list[self.new_dense_layer.id] = data[item]

            elif data[item]['tag'] == "Out":  
                self.new_out_layer = dnd.Icon(self.app, self.out_layer_pic, ("Out", "layer"))
                self.new_out_layer.attach(self.model_canvas, data[item]['x'], data[item]['y'])
                self.app.layers_list[self.new_out_layer.id] = data[item]

            elif data[item]['tag'] == "Relu":
                self.new_relu_activation = dnd.Icon(self.app, self.relu_activation_pic, ("Relu", "activation"))
                self.new_relu_activation.attach(self.model_canvas, data[item]['x'], data[item]['y'])
                self.app.layers_list[self.new_relu_activation.id] = data[item]
                
            elif data[item]['tag'] == "Sigmoid":
                self.new_sig_activation = dnd.Icon(self.app, self.sig_activation_pic, ("Sigmoid", "activation"))
                self.new_sig_activation.attach(self.model_canvas, data[item]['x'], data[item]['y'])
                self.app.layers_list[self.new_sig_activation.id] = data[item]

            elif data[item]['tag'] == "Softmax":
                self.new_max_activation = dnd.Icon(self.app, self.max_activation_pic, ("Softmax", "activation"))
                self.new_max_activation.attach(self.model_canvas, data[item]['x'], data[item]['y'])
                self.app.layers_list[self.new_max_activation.id] = data[item]
                
            elif data[item]['tag'] == "Dropout":
                self.new_dropout = dnd.Icon(self.app, self.dropout_pic, ("Dropout", "activation"))
                self.new_dropout.attach(self.model_canvas, data[item]['x'], data[item]['y'])
                self.app.layers_list[self.new_dropout.id] = data[item]


    def write_coords(self):
        
        for item_id in self.model_canvas.find_all():
            if item_id in self.app.layers_list:
                self.app.layers_list[item_id]['x'] = self.model_canvas.coords(item_id)[0]
                self.app.layers_list[item_id]['y'] = self.model_canvas.coords(item_id)[1]
            else:
                self.app.layers_list[item_id] = {}
                self.app.layers_list[item_id]['tag'] = self.model_canvas.gettags(item_id)[0]
                self.app.layers_list[item_id]['x'] = self.model_canvas.coords(item_id)[0]
                self.app.layers_list[item_id]['y'] = self.model_canvas.coords(item_id)[1]

    
    def save(self, event):
        filename = asksaveasfilename(title = "Save Model", defaultextension=".json", filetypes = (("json files","*.json"),("all files","*.*")))
        if filename:
            self.saved.set(True)
            self.write_coords()
            if os.path.exists(filename):
                os.remove(filename)
            with open(filename, 'w') as outfile:
                items_sorted = sorted(self.app.layers_list, key=lambda x: self.app.layers_list[x]['x'])
                sorted_data = {}
                for item in items_sorted:
                    sorted_data[item] = self.app.layers_list[item]
                json.dump(sorted_data, outfile, indent=4, separators=(',', ': '))

    def modified(self, event):
        self.saved.set(False)

    def compile(self, event):
        self.app.config(cursor="wait")
        self.app.update()
        
        from  keras.models import Model, Sequential
        from keras.layers import Input, Conv2D, Dense, Flatten, Dropout, Activation, MaxPooling2D
        import keras.backend as K

        items_sorted = sorted(self.app.layers_list, key=lambda x: self.app.layers_list[x]['x'])
        for items in items_sorted:
            print(self.app.layers_list[items])
        
        # Build Model
        #
        #
        #

        self.app.config(cursor="")
