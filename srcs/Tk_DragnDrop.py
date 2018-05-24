# -*- coding: utf-8 -*-

import srcs.layers
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import *

from srcs.layers import layers_list

# The factory function

def dnd_start(source, event):
    h = DndHandler(source, event)
    if h.root:
        return h
    else:
        return None


# The class that does the work

class DndHandler:

    root = None

    def __init__(self, source, event):
        if event.num > 5:
            return
        root = event.widget._root()
        try:
            root.__dnd
            return # Don't start recursive dnd
        except AttributeError:
            root.__dnd = self
            self.root = root
        self.source = source
        self.target = None
        self.initial_button = button = event.num
        self.initial_widget = widget = event.widget
        self.release_pattern = "<B%d-ButtonRelease-%d>" % (button, button)
        self.save_cursor = widget['cursor'] or ""
        widget.bind(self.release_pattern, self.on_release)
        widget.bind("<Motion>", self.on_motion)
        widget['cursor'] = "hand2"

    def __del__(self):
        root = self.root
        self.root = None
        if root:
            try:
                del root.__dnd
            except AttributeError:
                pass

    def on_motion(self, event):
        x, y = event.x_root, event.y_root
        target_widget = self.initial_widget.winfo_containing(x, y)
        source = self.source
        new_target = None
        while target_widget:
            try:
                attr = target_widget.dnd_accept
            except AttributeError:
                pass
            else:
                new_target = attr(source, event)
                if new_target:
                    break
            target_widget = target_widget.master
        old_target = self.target
        if old_target is new_target:
            if old_target:
                old_target.dnd_motion(source, event)
        else:
            if old_target:
                self.target = None
                old_target.dnd_leave(source, event)
            if new_target:
                new_target.dnd_enter(source, event)
                self.target = new_target

    def on_release(self, event):
        self.finish(event, 1)

    def cancel(self, event=None):
        self.finish(event, 0)

    def finish(self, event, commit=0):
        target = self.target
        source = self.source
        widget = self.initial_widget
        root = self.root
        try:
            del root.__dnd
            self.initial_widget.unbind(self.release_pattern)
            self.initial_widget.unbind("<Motion>")
            widget['cursor'] = self.save_cursor
            self.target = self.source = self.initial_widget = self.root = None
            if target:
                if commit:
                    target.dnd_commit(source, event)
                else:
                    target.dnd_leave(source, event)
        finally:
            source.dnd_end(target, event)

class Icon:

    def __init__(self, app, img, tags):
        self.img = img
        self.tags = tags
        self.app = app
        self.canvas = self.label = self.id = None


    def attach(self, canvas, x=10, y=10):
        self.x = x
        self.y = y
        if canvas is self.canvas:
            self.canvas.coords(self.id, x, y)
            return
        if self.canvas:
            self.detach()
        if not canvas:
            return
        label = tk.Label(canvas, image=self.img, borderwidth=2, relief="raised")
        id = canvas.create_window(x, y, window=label, anchor="nw", tags=self.tags)
        self.canvas = canvas
        self.label = label
        self.id = id
        label.bind("<ButtonPress>", self.press)
        double_clic_handler = lambda event: DnD_Container.set_layer_params(self, self, self)
        label.bind("<Double-Button-1>", double_clic_handler)
        

    def detach(self):
        canvas = self.canvas
        if not canvas:
            return
        if self.canvas != self.app.third_tab.layers_canvas:
            id = self.id
            self.last_id = id
            label = self.label
            self.canvas = self.label = self.id = None
            canvas.delete(id)
            label.destroy()
        else:
            label = Icon(self.app, self.img, self.tags)
            label.attach(self.canvas, x=self.x_orig, y=self.y_orig)

    def press(self, event):
        if dnd_start(self, event):
            # where the pointer is relative to the label widget:
            self.x_off = event.x
            self.y_off = event.y
            # where the widget is relative to the canvas:
            self.x_orig, self.y_orig = self.canvas.coords(self.id)

    def move(self, event):
        x, y = self.where(self.canvas, event)
        self.canvas.coords(self.id, x, y)

    def putback(self):
        self.canvas.coords(self.id, self.x_orig, self.y_orig)

    def where(self, canvas, event):
        # where the corner of the canvas is relative to the screen:
        x_org = canvas.winfo_rootx()
        y_org = canvas.winfo_rooty()
        # where the pointer is relative to the canvas widget:
        x = event.x_root - x_org
        y = event.y_root - y_org
        # compensate for initial pointer offset
        return x - self.x_off, y - self.y_off

    def dnd_end(self, target, event):
        if target:
            if target.canvas == self.app.third_tab.trash_canvas:
                self.label.destroy()
                if self.last_id in layers_list:
                    layers_list.pop(self.last_id)
                
class DnD_Container:

    def __init__(self, app, root, canvas):
        self.app = app
        self.root = root
        self.canvas = canvas
        self.canvas.dnd_accept = self.dnd_accept

    def dnd_accept(self, source, event):
        return self

    def dnd_enter(self, source, event):
        if self.canvas != self.app.third_tab.layers_canvas:
            self.canvas.focus_set() # Show highlight border
            x, y = source.where(self.canvas, event)
            x1, y1, x2, y2 = source.canvas.bbox(source.id)
            dx, dy = x2-x1, y2-y1
            self.dndid = self.canvas.create_rectangle(x, y, x+dx, y+dy)
            self.dnd_motion(source, event)

    def dnd_motion(self, source, event):
        if self.canvas != self.app.third_tab.layers_canvas:
            x, y = source.where(self.canvas, event)
            x1, y1, x2, y2 = self.canvas.bbox(self.dndid)
            self.canvas.move(self.dndid, x-x1, y-y1)

    def dnd_leave(self, source, event):
        if self.canvas != self.app.third_tab.layers_canvas:
            self.root.focus_set() # Hide highlight border
            self.canvas.delete(self.dndid)
            self.dndid = None

    def dnd_commit(self, source, event):
        if self.canvas != self.app.third_tab.layers_canvas:
            self.dnd_leave(source, event)
            x, y = source.where(self.canvas, event)
            if self.canvas == self.app.third_tab.model_canvas:
                x, y = self.check_n_offset(self.canvas, source, x, y)
                if source.canvas == self.app.third_tab.layers_canvas:
                    self.set_layer_params(event, source)
            source.attach(self.canvas, x, y)
        else:
            source.putback()

    def check_n_offset(self, canvas, source, x, y):
        source_bbox = source.canvas.bbox(source.id)
        source_w = source_bbox[2] - source_bbox[0]
        source_h = source_bbox[3] - source_bbox[1]
        if len([z for z in canvas.find_overlapping(x, y, x + source_w, y + source_h) if z != source.id]) > 0:
            items = [z for z in canvas.find_overlapping(x, y, x + source_w, y + source_h) if z != source.id]
            item_under = items[0]
            x_under, y_under = canvas.coords(item_under)
            item_bbox = canvas.bbox(item_under)
            item_w = item_bbox[2] - item_bbox[0]
            item_h = item_bbox[3] - item_bbox[1]
            if x >= x_under:
                x = x_bis = x + ((x_under + item_w) - x)
                while len([z for z in canvas.find_overlapping(x_bis, y, x_bis + source_w, y + source_h) if z != item_under]) > 0:
                    items = [z for z in canvas.find_overlapping(x_bis, y, x_bis + source_w, y + source_h) if z != item_under]
                    item_under = items[0]
                    x_under, y_under = canvas.coords(item_under)
                    item_bbox = canvas.bbox(item_under)
                    item_w = item_bbox[2] - item_bbox[0]
                    item_h = item_bbox[3] - item_bbox[1]
                    canvas.move(item_under, item_w, 0)
                    x_bis = x_under + item_w
            elif x < x_under:
                x = x_bis = x - ((x + item_w) - x_under)
                while len([z for z in canvas.find_overlapping(x_bis, y, x_bis + source_w, y + source_h) if z != item_under]) > 0:
                    items = [z for z in canvas.find_overlapping(x_bis, y, x_bis + source_w, y + source_h) if z != item_under]
                    item_under = items[0]
                    x_under, y_under = canvas.coords(item_under)
                    item_bbox = canvas.bbox(item_under)
                    item_w = item_bbox[2] - item_bbox[0]
                    item_h = item_bbox[3] - item_bbox[1]
                    canvas.move(item_under, -item_w, 0)
                    x_bis = x_under - item_w
        return (x, y)

    def set_layer_params(self, event, source):
        if type(self) == srcs.Tk_DragnDrop.DnD_Container:
            self.test_val = self.app.third_tab.model_canvas
        else:
            self.test_val = self.canvas
        if self.test_val == source.app.third_tab.model_canvas:
            if ("layer" in source.tags and "Flatten" not in source.tags) or "Dropout" in source.tags:
                x = self.app.winfo_x()
                y = self.app.winfo_y()
                if type(self) == srcs.Tk_DragnDrop.DnD_Container:
                    x_clic, y_clic = source.where(self.canvas, event)
                else:
                    x_clic = event.x
                    y_clic = event.y
                self.param_frame = tk.Toplevel()
                self.param_frame.geometry("%dx%d+%d+%d" % (250, 250, x + x_clic, y + y_clic))
                self.param_frame.title(source.tags[0] + " parameters")
                self.param_frame.transient(self.app)
                self.param_frame.grab_set()
                self.test_val.master.config(bg='lightgrey')
                for widget in self.test_val.master.winfo_children():
                    widget.config(bg='lightgrey')
                    for elem in widget.winfo_children():
                        elem.config(bg='lightgrey')
                if source.tags[0] == "In":
                    
                    labels = tk.Label(self.param_frame)
                    labels.grid(row=0, column=0, sticky='nsw')
                    labels.grid_rowconfigure(0, weight=1)
                    labels.grid_rowconfigure(1, weight=1)
                    labels.grid_rowconfigure(2, weight=1)
                    labels.grid_rowconfigure(3, weight=1)
                    labels.grid_rowconfigure(4, weight=1)
                    labels.grid_columnconfigure(0, weight=1)
                    labels.grid_columnconfigure(1, weight=1)
                    labels.grid_columnconfigure(2, weight=1)

                    label_0 = tk.Label(labels)
                    label_0.config(text='In Layer:', font=("Helvetica", 18))
                    label_0.grid(row=0, column=0, sticky='new', columnspan=3, padx=5, pady=10)
                    
                    label_1 = tk.Label(labels)
                    label_1.config(text='Dim 1:', font=("Helvetica", 14))
                    label_1.grid(row=1, column=0, sticky='nsw', padx=5, pady=10)
                    
                    self.dim1 = tk.StringVar()
                    
                    val_1 = tk.Entry(labels, width=10, textvariable=self.dim1)
                    val_1.grid(row=1, column=2, sticky='nsw', padx=5, pady=10)

                    label_2 = tk.Label(labels)
                    label_2.config(text='Dim 2:', font=("Helvetica", 14))
                    label_2.grid(row=2, column=0, sticky='nsw', padx=5, pady=10)
                    
                    self.dim2 = tk.StringVar()
                    
                    val_2 = tk.Entry(labels, width=10, textvariable=self.dim2)
                    val_2.grid(row=2, column=2, sticky='nsw', padx=5, pady=10)

                    label_3 = tk.Label(labels)
                    label_3.config(text='Dim 3:', font=("Helvetica", 14))
                    label_3.grid(row=3, column=0, sticky='nsw', padx=5, pady=10)
                    
                    self.dim3 = tk.StringVar()
                    
                    val_3 = tk.Entry(labels, width=10, textvariable=self.dim3)
                    val_3.grid(row=3, column=2, sticky='nsw', padx=5, pady=10)
    

                    save_in = lambda: DnD_Container.save_layer(self=self, id=source.id, tag=source.tags[0],
                                                         dim1=self.dim1, dim2=self.dim2, dim3=self.dim3)

                    save_but = tk.Button(labels)
                    save_but.config(text='Save', font=("Helvetica", 16), command=save_in)
                    save_but.grid(row=4, column=1, sticky='nsew', padx=5, pady=10)
                    
                elif source.tags[0] == "Conv2d":
                    
                    labels = tk.Label(self.param_frame)
                    labels.grid(row=0, column=0, sticky='nsw')
                    labels.grid_rowconfigure(0, weight=1)
                    labels.grid_rowconfigure(1, weight=1)
                    labels.grid_rowconfigure(2, weight=1)
                    labels.grid_rowconfigure(3, weight=1)
                    labels.grid_columnconfigure(0, weight=1)
                    labels.grid_columnconfigure(1, weight=1)
                    labels.grid_columnconfigure(2, weight=1)

                    label_0 = tk.Label(labels)
                    label_0.config(text='Conv2D Layer:', font=("Helvetica", 18))
                    label_0.grid(row=0, column=0, sticky='new', columnspan=3, padx=10, pady=10)

                    label_1 = tk.Label(labels)
                    label_1.config(text='Filters:', font=("Helvetica", 14))
                    label_1.grid(row=1, column=0, sticky='nsw', padx=5, pady=10)

                    self.filters = tk.StringVar()
                    
                    val_1 = tk.Entry(labels, width=10, textvariable=self.filters)
                    val_1.grid(row=1, column=2, sticky='nse', padx=5, pady=10)
                    
                    label_2 = tk.Label(labels)
                    label_2.config(text='Kernel size:', font=("Helvetica", 14))
                    label_2.grid(row=2, column=0, sticky='nsw', pady=10)
                    
                    self.kernel_size_x = tk.StringVar()
                    
                    val_2_x = tk.Entry(labels, width=10, textvariable=self.kernel_size_x)
                    val_2_x.grid(row=2, column=1, sticky='nsw', pady=10)

                    self.kernel_size_y = tk.StringVar()
                    
                    val_2_y = tk.Entry(labels, width=10, textvariable=self.kernel_size_y)
                    val_2_y.grid(row=2, column=2, sticky='nsw', padx=5, pady=10)


                    save_conv2d = lambda: DnD_Container.save_layer(self=self, id=source.id, tag=source.tags[0],
                                                         filters=self.filters, kernel_size_x=self.kernel_size_x, kernel_size_y=self.kernel_size_y)
                    
                    save_but = tk.Button(labels)
                    save_but.config(text='Save', font=("Helvetica", 16), command=save_conv2d)
                    save_but.grid(row=3, column=1, sticky='nsew', pady=10)
                
                elif source.tags[0] == "Dense":
                    
                    labels = tk.Label(self.param_frame)
                    labels.grid(row=0, column=0, sticky='nsw')
                    labels.grid_rowconfigure(0, weight=1)
                    labels.grid_rowconfigure(1, weight=1)
                    labels.grid_rowconfigure(2, weight=1)
                    labels.grid_columnconfigure(0, weight=1)
                    labels.grid_columnconfigure(1, weight=1)
                    labels.grid_columnconfigure(2, weight=1)

                    label_0 = tk.Label(labels)
                    label_0.config(text='Conv2D Layer:', font=("Helvetica", 18))
                    label_0.grid(row=0, column=0, sticky='new', columnspan=3, padx=10, pady=10)
                    
                    label_1 = tk.Label(labels)
                    label_1.config(text='Neurons:', font=("Helvetica", 14))
                    label_1.grid(row=1, column=0, sticky='nsw', padx=5, pady=10)

                    self.neurons = tk.StringVar()
                    
                    val_1 = tk.Entry(labels, width=10, textvariable=self.neurons)
                    val_1.grid(row=1, column=2, sticky='nse', padx=5, pady=10)


                    save_dense = lambda: DnD_Container.save_layer(self=self, id=source.id, tag=source.tags[0], neurons=self.neurons)
                    
                    save_but = tk.Button(labels)
                    save_but.config(text='Save', font=("Helvetica", 16), command=save_dense)
                    save_but.grid(row=2, column=1, sticky='nsew', padx=5, pady=10)
                    
                elif source.tags[0] == "Max_pooling":
                    
                    labels = tk.Label(self.param_frame)
                    labels.grid(row=0, column=0, sticky='nsw')
                    labels.grid_rowconfigure(0, weight=1)
                    labels.grid_rowconfigure(1, weight=1)
                    labels.grid_rowconfigure(2, weight=1)
                    labels.grid_rowconfigure(3, weight=1)
                    labels.grid_columnconfigure(0, weight=1)
                    labels.grid_columnconfigure(1, weight=1)
                    labels.grid_columnconfigure(2, weight=1)

                    label_0 = tk.Label(labels)
                    label_0.config(text='MaxPooling Layer:', font=("Helvetica", 18))
                    label_0.grid(row=0, column=0, sticky='new', columnspan=3, padx=10, pady=10)
                    
                    label_1 = tk.Label(labels)
                    label_1.config(text='Pool size:', font=("Helvetica", 14))
                    label_1.grid(row=1, column=0, sticky='nsw', padx=5, pady=10)
                    
                    self.pool_size_x = tk.StringVar()
                    
                    val_1_x = tk.Entry(labels, width=10, textvariable=self.pool_size_x)
                    val_1_x.grid(row=1, column=2, sticky='nsw', pady=10)

                    self.pool_size_y = tk.StringVar()
                    
                    val_1_y = tk.Entry(labels, width=10, textvariable=self.pool_size_y)
                    val_1_y.grid(row=1, column=1, sticky='nsw', padx=5, pady=10)

                    label_2 = tk.Label(labels)
                    label_2.config(text='Stride:', font=("Helvetica", 14))
                    label_2.grid(row=2, column=0, sticky='nsw', padx=5, pady=10)
                    
                    self.stride_x = tk.StringVar()
                    
                    val_2_x = tk.Entry(labels, width=10, textvariable=self.stride_x)
                    val_2_x.grid(row=2, column=1, sticky='nsw', padx=5, pady=10)

                    self.stride_y = tk.StringVar()
                    
                    val_2_y = tk.Entry(labels, width=10, textvariable=self.stride_y)
                    val_2_y.grid(row=2, column=2, sticky='nsw', pady=10)

                    save_max_p = lambda: DnD_Container.save_layer(self=self, id=source.id, tag=source.tags[0],
                                                         pool_size_x=self.pool_size_x, pool_size_y=self.pool_size_y,
                                                         stride_x=self.stride_x, stride_y=self.stride_y)

                    save_but = tk.Button(labels)
                    save_but.config(text='Save', font=("Helvetica", 16), command=save_max_p)
                    save_but.grid(row=3, column=1, sticky='nsew', padx=5, pady=10)
                
                elif source.tags[0] == "Out":
                    
                    labels = tk.Label(self.param_frame)
                    labels.grid(row=0, column=0, sticky='nsw')
                    labels.grid_rowconfigure(0, weight=1)
                    labels.grid_rowconfigure(1, weight=1)
                    labels.grid_rowconfigure(2, weight=1)
                    labels.grid_rowconfigure(3, weight=1)
                    labels.grid_rowconfigure(4, weight=1)
                    labels.grid_columnconfigure(0, weight=1)
                    labels.grid_columnconfigure(1, weight=1)

                    label_0 = tk.Label(labels)
                    label_0.config(text="Out Layer:", font=("Helvetica", 18))
                    label_0.grid(row=0, column=0, sticky='new', columnspan=2, padx=10, pady=10)
                    
                    label_1 = tk.Label(labels)
                    label_1.config(text="Output(s):", font=("Helvetica", 14))
                    label_1.grid(row=1, column=0, sticky='nsw', padx=5, pady=10)
                    
                    self.out_nb = tk.StringVar()
                    self.values = ("1", "2", "3", "4")
                    self.out_nb.set(self.values[0])
                    
                    val_1 = ttk.Combobox(labels, textvariable=self.out_nb, values=self.values, state="readonly", width=10)
                    val_1.grid(row=1, column=1, sticky='nsw', padx=5, pady=10)

                    label_1 = tk.Label(labels)
                    label_1.config(text='Type:', font=("Helvetica", 14))
                    label_1.grid(row=2, column=0, sticky='nsw', padx=5, pady=10)
                    
                    self.out_type = tk.IntVar()
                    self.out_type.set(1)
                    
                    val_1 = tk.Radiobutton(labels)
                    val_1.config(text="Categories", variable=self.out_type, value=1)
                    val_1.grid(row=2, column=1, sticky='nsw', padx=5, pady=10)
                    val_1bis = tk.Radiobutton(labels)
                    val_1bis.config(text="Values", variable=self.out_type, value=2)
                    val_1bis.grid(row=3, column=1, sticky='nsw', padx=5, pady=10)

                    save_out = lambda: DnD_Container.save_layer(self=self, id=source.id, tag=source.tags[0], out_type=self.out_type, out_nb=self.out_nb)

                    save_but = tk.Button(labels)
                    save_but.config(text='Save', font=("Helvetica", 16), command=save_out)
                    save_but.grid(row=4, column=0, columnspan=2, padx=5, pady=10)
              
                elif source.tags[0] == "Dropout":
                    
                    labels = tk.Label(self.param_frame)
                    labels.grid(row=0, column=0, sticky='nsw')
                    labels.grid_rowconfigure(0, weight=1)
                    labels.grid_rowconfigure(1, weight=1)
                    labels.grid_rowconfigure(2, weight=1)
                    labels.grid_columnconfigure(0, weight=1)
                    labels.grid_columnconfigure(1, weight=1)
                    labels.grid_columnconfigure(2, weight=1)

                    label_0 = tk.Label(labels)
                    label_0.config(text='Dropout Layer:', font=("Helvetica", 18))
                    label_0.grid(row=0, column=0, sticky='new', columnspan=3, padx=10, pady=10)
                    
                    label_1 = tk.Label(labels)
                    label_1.config(text='Ratio:', font=("Helvetica", 14))
                    label_1.grid(row=1, column=0, sticky='nsw', padx=5, pady=10)

                    self.ratio = tk.StringVar()
                    
                    val_1 = tk.Entry(labels, width=10, textvariable=self.ratio)
                    val_1.grid(row=1, column=2, sticky='nse', padx=5, pady=10)

                    save_dropout = lambda: DnD_Container.save_layer(self=self, id=source.id, tag=source.tags[0], ratio=self.ratio)

                    save_but = tk.Button(labels)
                    save_but.config(text='Save', font=("Helvetica", 16), command=save_dropout)
                    save_but.grid(row=2, column=1, sticky='nsew', padx=5, pady=10)

    def save_layer(self, id, tag, **kwargs):
        
        if id in layers_list:
            res = askquestion("Modify Layer", "Layer already exists and will be overwriten...", icon='warning')
            if res == "no":
                self.param_frame.destroy()
                test_val.config(bg='grey')
                return
        layers_list[id] = {} #TODO: Save the layer's datas
        if len(kwargs) > 0:
            self.param_frame.destroy()
        self.test_val.master.config(bg='SystemButtonFace')
        for widget in self.test_val.master.winfo_children():
            widget.config(bg='SystemButtonFace')
            for elem in widget.winfo_children():
                elem.config(bg='SystemButtonFace')
