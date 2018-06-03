# -*- coding: utf-8 -*-

from srcs.const import *
import sys

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import *
from tkinter.filedialog import *

import os
import configparser
from time import time, localtime, strftime, sleep

from PIL import Image, ImageTk

import srcs.Tk_Tooltips as ttp
import srcs.Tk_DragnDrop as dnd

import json

class ThirdTab(object):

    def __init__(self, app, devMode):
        self.app = app
        self.devMode = devMode

        self.saved = tk.BooleanVar()
        self.saved.set(False)
        
        self.model_frame = Frame(app.third_tab)
        self.model_frame.grid(row=0, column=0, stick='nsew')
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
        self.sig_activation_pic = ImageTk.PhotoImage(Image.open('assets/sig_activation.png'))
        self.relu_activation_pic = ImageTk.PhotoImage(Image.open('assets/relu_activation.png'))
        self.max_activation_pic = ImageTk.PhotoImage(Image.open('assets/softmax_activation.png'))
        self.dropout_pic = ImageTk.PhotoImage(Image.open('assets/dropout.png'))
        self.load_pic = ImageTk.PhotoImage(Image.open('assets/dir_open.png'))
        self.save_pic = ImageTk.PhotoImage(Image.open('assets/save.png'))
        self.export_pic = ImageTk.PhotoImage(Image.open('assets/export.png'))
        self.logo_pic = ImageTk.PhotoImage(Image.open('assets/keras.jpeg'))
        self.clear_pic = ImageTk.PhotoImage(Image.open('assets/pass.png'))

        self.model_canvas = Canvas(self.model_frame)
        self.model_canvas.bind("<ButtonPress>", self.modified)
        self.model_canvas_dnd = dnd.DnD_Container(self.app, self.model_frame, self.model_canvas)
        self.model_canvas.config(borderwidth=2, relief="sunken", height=MODEL_H, width=MODEL_W)
        self.model_canvas.grid(row=0, column=1, padx=20, pady=10, sticky="w")
        self.model_canvas.grid_propagate(0)
        model_ttp = ttp.ToolTip(self.model_canvas, 'Drop a to add it to the model \n \
                                        Double clic on a layer to edit it', msgFunc=None, delay=1, follow=True)

        self.param_frame = Frame(self.model_frame)
        self.param_frame.grid(row=0, column=0, padx=20, pady=10, stick='e')
        self.param_frame.grid_columnconfigure(0, weight=1)
        self.param_frame.grid_rowconfigure(0, weight=1)
        self.param_frame.grid_rowconfigure(1, weight=1)
        self.param_frame.grid_rowconfigure(2, weight=1)
        self.param_frame.grid_rowconfigure(3, weight=1)

        output_label = Label(self.param_frame, text="Output type :", font=("Helvetica", 16), borderwidth=2, relief="ridge")
        output_label.grid(row=0, column=0, padx=5, pady=5, sticky="n")
        output = ["Binary", "Categorical", "MSE"]
        self.out_type = StringVar()
        output_box = ttk.Combobox(self.param_frame, textvariable=self.out_type, values=output, justify="center", width=10)
        output_box.grid(row=1, column=0, padx=5, pady=5, sticky="n")

        opti_label = Label(self.param_frame, text="Optimizer :", font=("Helvetica", 16), borderwidth=2, relief="ridge")
        opti_label.grid(row=2, column=0, padx=5, pady=5, sticky="s")
        self.optimizers = ["adadelta", "adam", "nadam", "rmsprop", "sgd"]
        self.opti = StringVar()
        opti_box = ttk.Combobox(self.param_frame, textvariable=self.opti, values=self.optimizers, justify="center", width=10)
        opti_box.grid(row=3, column=0, padx=5, pady=5, sticky="s")

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
        export_handler = lambda: self.export(self)

        load_but = Button(command_frame)
        load_but.config(image=self.load_pic, command=load_handler)
        load_but.grid(row=0, column=1, padx=10, pady=10)
        load_but_ttp = ttp.ToolTip(load_but, 'Load Model', msgFunc=None, delay=1, follow=True)

        save_but = Button(command_frame)
        save_but.config(image=self.save_pic, command=save_handler)
        save_but.grid(row=0, column=2, padx=10, pady=10)
        save_but_ttp = ttp.ToolTip(save_but, 'Save Model', msgFunc=None, delay=1, follow=True)

        self.export_but = Button(command_frame)
        self.export_but.config(image=self.export_pic, command=export_handler, state="disabled")
        self.export_but.grid(row=1, column=1, columnspan=2, padx=10, pady=10)
        export_but_ttp = ttp.ToolTip(self.export_but, 'Export Model', msgFunc=None, delay=1, follow=True)

        powered_label = Label(command_frame, text="powered by:")
        powered_label.grid(row=2, column=1, columnspan=2, sticky="nsew")

        logo_label = Label(command_frame, image=self.logo_pic)
        logo_label.grid(row=3, column=1, columnspan=2, sticky="new")

        clear_but = Button(command_frame)
        clear_but.config(image=self.clear_pic, command=clear_handler)
        clear_but.grid(row=3, column=0, pady=10, sticky="sw")
        clear_but_ttp = ttp.ToolTip(clear_but, 'Clear Model', msgFunc=None, delay=1, follow=True)

        info = Label(self.model_frame, text="^ Drag layers ^").grid(row=1, column=1)

        self.layers_canvas = Canvas(self.model_frame)
        self.layers_canvas_dnd = dnd.DnD_Container(self.app, self.model_frame, self.layers_canvas)
        self.layers_canvas.config(borderwidth=2, relief="sunken", height=235, width=600)
        self.layers_canvas.grid(row=2, column=1, padx=20, pady=10)
        self.layers_canvas.grid_propagate(0)
        layers_ttp = ttp.ToolTip(self.layers_canvas, 'Drag a layer to upper area to add it to the model', msgFunc=None, delay=1, follow=True)

        self.trash_canvas = Canvas(self.model_frame)
        self.trash_canvas.config(borderwidth=2, relief="groove", height=200, width=200)
        self.trash_canvas.create_image(108, 105, image=self.trash_pic)
        self.trash_dnd = dnd.DnD_Container(self.app, self.model_frame, self.trash_canvas)
        self.trash_canvas.grid(row=2, column=2, padx=20, pady=20, stick='w')
        self.trash_canvas.grid_propagate(0)
        trash_ttp = ttp.ToolTip(self.trash_canvas, 'Drop a layer to remove it', msgFunc=None, delay=1, follow=True)

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
        self.filename =  askopenfilename(title = "Select Model",filetypes = (("json files","*.json"),("all files","*.*")))
        if self.filename:
            with open(self.filename, 'r') as infile:
                if self.app.layers_list:
                    res = askquestion("Load Model", "This action will overwrite existing model \nLoad anyway ?", icon='warning')
                    if res == 'no':
                        return
                data = json.load(infile)
                self.model_canvas.delete("all")
                self.app.layers_list = {}
                if 'output_type' in data:
                    self.out_type.set(data['output_type'])
                if 'optimizer' in data:
                    self.opti.set(data['optimizer'])
                self.parse(data)
                self.saved.set(True)
                self.export_but.config(state="normal")

    def parse(self, data):
        for item in data:
            if item != "optimizer" and item != "output_type":
                if data[item]['tag'] == "In":
                    self.new_in_layer = dnd.Icon(self.app, self.in_layer_pic, ("In", "layer"))
                    self.new_in_layer.attach(self.model_canvas, data[item]['x'], data[item]['y'])
                    self.app.layers_list[self.new_in_layer.id] = data[item]
                    
                elif data[item]['tag'] == "Conv2d":
                    self.new_conv2d_layer = dnd.Icon(self.app, self.conv2d_layer_pic, ("Conv2d", "layer"))
                    self.new_conv2d_layer.attach(self.model_canvas, data[item]['x'], data[item]['y'])
                    self.app.layers_list[self.new_conv2d_layer.id] = data[item]
                    
                elif data[item]['tag'] == "Max_pooling":
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
        self.filename = asksaveasfilename(title = "Save Model", defaultextension=".json", filetypes = (("json files","*.json"),("all files","*.*")))
        if self.filename:
            self.saved.set(True)
            self.write_coords()
            if os.path.exists(self.filename):
                os.remove(self.filename)
            with open(self.filename, 'w') as outfile:
                items_sorted = sorted(self.app.layers_list, key=lambda x: self.app.layers_list[x]['x'])
                sorted_data = {}
                sorted_data['output_type'] = self.out_type.get()
                sorted_data['optimizer'] = self.opti.get()
                for item in items_sorted:
                    sorted_data[item] = self.app.layers_list[item]
                json.dump(sorted_data, outfile, indent=4, separators=(',', ': '))
                self.export_but.config(state="normal")

    def modified(self, event):
        self.saved.set(False)
        self.export_but.config(state="disabled")

    def export(self, event):
        if self.saved.get() == False:
            showwarning("Error", "Save model before you export it.");
            return
        self.app.config(cursor="wait")
        self.app.update()

        # Order Datas
        items_sorted = sorted(self.app.layers_list, key=lambda x: self.app.layers_list[x]['x'])
        sorted_data = {}
        for item in items_sorted:
            sorted_data[item] = self.app.layers_list[item]
        items_list = list(sorted_data.keys())
        
        # Check and Get In Layer
        try:
            in_id = items_list[0]
            if sorted_data[in_id]['tag'] == 'In':
                try:
                    if int(sorted_data[in_id]['dim_1']) > 0:
                        dim_1 = int(sorted_data[in_id]['dim_1'])
                    else:
                        showwarning("Error", "Negative or null 'dim_1' value in {} layer".format(sorted_data[in_id]['tag']));
                        self.app.config(cursor="")
                        return

                    if int(sorted_data[in_id]['dim_2']) > 0:
                        dim_2 = int(sorted_data[in_id]['dim_2'])
                    else:
                        showwarning("Error", "Negative or null 'dim_2' value in {} layer".format(sorted_data[in_id]['tag']));
                        self.app.config(cursor="")
                        return

                    if int(sorted_data[in_id]['dim_3']) > 0:
                        dim_3 = int(sorted_data[in_id]['dim_3'])
                    else:
                        showwarning("Error", "Negative or null 'dim_3' value in {} layer".format(sorted_data[in_id]['tag']));
                        self.app.config(cursor="")
                        return
                    
                    # Set Input Shape with Keras Sequential API
                    input_shape = (dim_1, dim_2, dim_3)
                    
                except ValueError:
                    showwarning("Error", "Incorrect or empty value(s) in In Layer");
                    self.app.config(cursor="")
                    return
            else:
                showwarning("Error", "No Input Layer");
                self.app.config(cursor="")
                return 
        except(IndexError):
            showwarning("Error", "No layers");
            self.app.config(cursor="")
            return

        # Import Keras ######
        from  keras.models import Sequential, Model
        from keras.layers import Input, Conv2D, Dense, Flatten, Dropout, Activation, MaxPooling2D
        import keras.backend as K
        K.clear_session()

        # Buid Model
        model = Sequential()
        
        # Check and Get first layer
        try:
            first_layer_id = items_list[1]

            # If First Layer is Dense
            if sorted_data[first_layer_id]['tag'] == 'Dense':
                try:
                    if int(sorted_data[first_layer_id]['neurons']) > 0:
                        neurons = int(sorted_data[first_layer_id]['neurons'])
                        
                        # Build Dense Layer with Keras Sequential API
                        model.add(Dense(units=neurons, input_shape=input_shape))

                    else:
                        showwarning("Error", "Negative or null 'neurons' value in {} layer".format(sorted_data[first_layer_id]['tag']));
                        self.app.config(cursor="")
                        return
                    
                except ValueError:
                    showwarning("Error", "Incorrect or empty value(s) in {}".format(sorted_data[first_layer_id]['tag']));
                    self.app.config(cursor="")
                    return
                
            # If First Layer is Conv2D
            elif sorted_data[first_layer_id]['tag'] == 'Conv2d':
                try:  
                    if int(sorted_data[first_layer_id]['filters']) > 0:
                        filters = int(sorted_data[first_layer_id]['filters'])
                    else:
                        showwarning("Error", "Negative or null 'filters' value in {} layer".format(sorted_data[first_layer_id]['tag']));
                        self.app.config(cursor="")
                        return
                    
                    if int(sorted_data[first_layer_id]['kernel_size_x']) > 0:
                        kernel_size_x = int(sorted_data[first_layer_id]['kernel_size_x'])
                    else:
                        showwarning("Error", "Negative or null 'kernel_size_x' value in {} layer".format(sorted_data[first_layer_id]['tag']));
                        self.app.config(cursor="")
                        return
                    
                    if int(sorted_data[first_layer_id]['kernel_size_y']) > 0:
                        kernel_size_y = int(sorted_data[first_layer_id]['kernel_size_y'])
                    else:
                        showwarning("Error", "Negative or null 'kernel_size_y' value in {} layer".format(sorted_data[first_layer_id]['tag']));
                        self.app.config(cursor="")
                        return

                    if int(sorted_data[first_layer_id]['stride_x']) > 0:
                        stride_x = int(sorted_data[first_layer_id]['stride_x'])
                    else:
                        showwarning("Error", "Negative or null 'stride_x' value in {} layer".format(sorted_data[first_layer_id]['tag']));
                        self.app.config(cursor="")
                        return
                    
                    if int(sorted_data[first_layer_id]['stride_y']) > 0:
                        stride_y = int(sorted_data[first_layer_id]['stride_y'])
                    else:
                        showwarning("Error", "Negative or null 'stride_y' value in {} layer".format(sorted_data[first_layer_id]['tag']));
                        self.app.config(cursor="")
                        return

                    if int(sorted_data[first_layer_id]['padding']) == 2:
                        padding = 'same'
                    else:
                        padding = 'valid'

                    # Build Conv2D Layer with Keras Sequential API
                    model.add(Conv2D(filters=filters, input_shape=input_shape, kernel_size=(kernel_size_y, kernel_size_x), strides=(stride_y, stride_x), padding=padding))
                        
                except ValueError:
                    showwarning("Error", "Incorrect or empty value(s) in {}".format(sorted_data[first_layer_id]['tag']));
                    self.app.config(cursor="")
                    return
 
            else:
                showwarning("Error", "Incorrect first layer, \nUse Conv or Dense as first layer (after In)");
                self.app.config(cursor="")
                return
            
        except IndexError:
            showwarning("Error", "Not enough layers");
            self.app.config(cursor="")
            return

        # TODO : Loop over next layers...
        i = 2
        while i < len(items_list):
            item = items_list[i]

            # If Layer is Dense
            if sorted_data[item]['tag'] == 'Dense':
                try:
                    if int(sorted_data[item]['neurons']) > 0:
                        neurons = int(sorted_data[item]['neurons'])
                    else:
                        showwarning("Error", "Negative or null 'neurons' value in {} layer".format(sorted_data[item]['tag']));
                        self.app.config(cursor="")
                        return

                    # Build Dense Layer with Keras Sequential API
                    model.add(Dense(units=neurons))
                    
                except ValueError:
                    showwarning("Error", "Incorrect or empty value(s) in {}".format(sorted_data[item]['tag']));
                    self.app.config(cursor="")
                    return
                
            # If Layer is Conv2D
            elif sorted_data[item]['tag'] == 'Conv2d':
                try:
                    if int(sorted_data[item]['filters']) > 0:
                        filters = int(sorted_data[item]['filters'])
                    else:
                        showwarning("Error", "Negative or null 'filters' value in {} layer".format(sorted_data[item]['tag']));
                        self.app.config(cursor="")
                        return
                    
                    if int(sorted_data[item]['kernel_size_x']) > 0:
                        kernel_size_x = int(sorted_data[item]['kernel_size_x'])
                    else:
                        showwarning("Error", "Negative or null 'kernel_size_x' value in {} layer".format(sorted_data[item]['tag']));
                        self.app.config(cursor="")
                        return
                    
                    if int(sorted_data[item]['kernel_size_y']) > 0:
                        kernel_size_y = int(sorted_data[item]['kernel_size_y'])
                    else:
                        showwarning("Error", "Negative or null 'kernel_size_y' value in {} layer".format(sorted_data[item]['tag']));
                        self.app.config(cursor="")
                        return

                    if int(sorted_data[item]['stride_x']) > 0:
                        stride_x = int(sorted_data[item]['stride_x'])
                    else:
                        showwarning("Error", "Negative or null 'stride_x' value in {} layer".format(sorted_data[item]['tag']));
                        self.app.config(cursor="")
                        return
                    
                    if int(sorted_data[item]['stride_y']) > 0:
                        stride_y = int(sorted_data[item]['stride_y'])
                    else:
                        showwarning("Error", "Negative or null 'stride_y' value in {} layer".format(sorted_data[item]['tag']));
                        self.app.config(cursor="")
                        return

                    if int(sorted_data[item]['padding']) == 1:
                        padding = 'same'
                    else:
                        padding = 'valid'

                    # Build Conv2D Layer with Keras Sequential API
                    model.add(Conv2D(filters=filters, kernel_size=(kernel_size_y, kernel_size_x), input_shape=input_shape, strides=(stride_y, stride_x), padding=padding))

                except ValueError:
                    showwarning("Error", "Incorrect or empty value(s) in {}".format(sorted_data[item]['tag']));
                    self.app.config(cursor="")
                    return

            # If Layer is Max Pooling
            elif sorted_data[item]['tag'] == 'Max_pooling':
                try:
                    if int(sorted_data[item]['pool_size_x']) > 0:
                        pool_size_x = int(sorted_data[item]['pool_size_x'])
                    else:
                        showwarning("Error", "Negative or null 'pool_size_x' value in {} layer".format(sorted_data[item]['tag']));
                        self.app.config(cursor="")
                        return
                    
                    if int(sorted_data[item]['pool_size_y']) > 0:
                        pool_size_y = int(sorted_data[item]['pool_size_y'])
                    else:
                        showwarning("Error", "Negative or null 'pool_size_y' value in {} layer".format(sorted_data[item]['tag']));
                        self.app.config(cursor="")
                        return

                    if int(sorted_data[item]['stride_x']) >= 0:
                        stride_x = int(sorted_data[item]['stride_x'])
                    else:
                        showwarning("Error", "Negative 'stride_x' value in {} layer".format(sorted_data[item]['tag']));
                        self.app.config(cursor="")
                        return
                    
                    if int(sorted_data[item]['stride_y']) >= 0:
                        stride_y = int(sorted_data[item]['stride_y'])
                    else:
                        showwarning("Error", "Negative 'stride_y' value in {} layer".format(sorted_data[item]['tag']));
                        self.app.config(cursor="")
                        return

                    if int(sorted_data[item]['padding']) == 1:
                        padding = 'same'
                    else:
                        padding = 'valid'

                    # Build Max Pooling Layer with Keras Sequential API
                    if stride_x > 0 and stride_y > 0:
                        strides = (stride_y, stride_x)
                    else:
                        strides = None
                    model.add(MaxPooling2D(pool_size=(pool_size_x, pool_size_y), strides=strides, padding=padding))

                except ValueError:
                    showwarning("Error", "Incorrect or empty value(s) in {}".format(sorted_data[item]['tag']));
                    self.app.config(cursor="")
                    return

            # If Layer is Flatten
            elif sorted_data[item]['tag'] == 'Flatten':
                # Build Flatten Layer with Keras Sequential API
                model.add(Flatten())

            # If Layer is Relu
            elif sorted_data[item]['tag'] == 'Relu':
                if sorted_data[item - 1]['tag'] == 'Dense' or sorted_data[item - 1]['tag'] == 'Conv2d' or sorted_data[item - 1]['tag'] == 'Max_pooling':
                    # Build Relu Layer with Keras Sequential API
                    model.add(Activation('relu'))
                else:
                    showwarning("Error", "Activation layer {} is invalid after {} layer".format(sorted_data[item]['tag'], sorted_data[item - 1]['tag']));
                    self.app.config(cursor="")
                    return
                
            # If Layer is Sigmoid
            elif sorted_data[item]['tag'] == 'Sigmoid':
                if sorted_data[item - 1]['tag'] == 'Dense' or sorted_data[item - 1]['tag'] == 'Conv2d' or sorted_data[item - 1]['tag'] == 'Max_pooling':
                    # Build Sigmoid Layer with Keras Sequential API
                    model.add(Activation('sigmoid'))
                else:
                    showwarning("Error", "Activation layer {} is invalid after {} layer".format(sorted_data[item]['tag'], sorted_data[item - 1]['tag']));
                    self.app.config(cursor="")
                    return

            # If Layer is Softmax
            elif sorted_data[item]['tag'] == 'Softmax':
                if sorted_data[item - 1]['tag'] == 'Dense' or sorted_data[item - 1]['tag'] == 'Conv2d' or sorted_data[item - 1]['tag'] == 'Max_pooling':
                    # Build Softmax Layer with Keras Sequential API
                    model.add(Activation('softmax'))
                else:
                    showwarning("Error", "Activation layer {} is invalid after {} layer".format(sorted_data[item]['tag'], sorted_data[item - 1]['tag']));
                    self.app.config(cursor="")
                    return

            # If Layer is Dropout
            elif sorted_data[item]['tag'] == 'Dropout':
                if sorted_data[item - 1]['tag'] == 'Dense' or sorted_data[item - 1]['tag'] == 'Conv2d' or sorted_data[item - 1]['tag'] == 'Max_pooling':
                    try:
                        if int(sorted_data[item]['ratio']) > 0:
                            ratio = int(sorted_data[item]['ratio'])
                        else:
                            showwarning("Error", "Negative or null 'ratio' value in {} layer".format(sorted_data[item]['tag']));
                            self.app.config(cursor="")
                            return
                        # Build Dropout Layer with Keras Sequential API
                        model.add(Activation('dropout', ratio))
                    
                    except ValueError:
                        showwarning("Error", "Incorrect or empty value(s) in {}".format(sorted_data[item]['tag']));
                        self.app.config(cursor="")
                        return
                else:
                    showwarning("Error", "Activation layer {} is invalid after {} layer".format(sorted_data[item]['tag'], sorted_data[item - 1]['tag']));
                    self.app.config(cursor="")
                    return
            
            i = i + 1

        output = self.out_type.get()
        if output == "Binary":
            loss = 'binary_crossentropy'
        elif output == "Categorical":
            loss = 'categorical_crossentropy'
        elif output == "MSE":
            loss = 'mse'
        else:
            showwarning("Error", "Wrong output type value")
            self.app.config(cursor="")
            return
        opti = self.opti.get()
        if opti not in self.optimizers:
            showwarning("Error", "Wrong optimizer value")
            self.app.config(cursor="")
            return

        model.compile(optimizer=opti, loss=loss, metrics=['accuracy'])

        model.save(self.filename.split('.')[0] + ".h5");

        if self.devMode:
            model.summary()

        showinfo("Success", "Model Exported with 'h5py' format");


        self.app.config(cursor="")

    def on_quit(self):
        if self.app.layers_list and self.saved.get() == False:
            res = askquestion("Quit", "This action may destroy unsaved model... \n Quit anyway ?", icon='warning')
            if res == 'no':
                return 0
            else:
                return 1
        else:
            return 1
