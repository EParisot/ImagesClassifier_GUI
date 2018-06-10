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
import configparser
from pathlib import Path

if SYSTEM != 'Rpi':
    import imutils
    from imutils.video import VideoStream
    import cv2
else:
    from picamera import PiCamera
    from picamera.array import PiRGBArray

import numpy as np
import threading

import srcs.Tk_Tooltips as ttp

class FirstTab():

    def __init__(self, app, devMode):
        self.app = app
        self.devMode = devMode
        
        self.snap_frame = Frame(self.app.first_tab)
        self.snap_frame.grid(row=0, column=0, sticky="nsew")
        self.snap_frame.grid_columnconfigure(0, weight=1)
        self.snap_frame.grid_columnconfigure(1, weight=1)
        self.snap_frame.grid_columnconfigure(2, weight=1)
        self.snap_frame.grid_rowconfigure(0, weight=1)

        self.frame = None
        self.vs = None
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.stopEvent = threading.Event()
        self.panel = None
        self.image = None

        self.snap_w = IntVar()
        self.snap_w.set(SNAP_W)
        self.snap_h = IntVar()
        self.snap_h.set(SNAP_H)

        self.none_pic = ImageTk.PhotoImage(Image.open('assets/prev.png'))
        self.cam_pic = ImageTk.PhotoImage(Image.open('assets/webcam.png'))
        self.stop_pic = ImageTk.PhotoImage(Image.open('assets/stop.png'))
        self.snap_pic = ImageTk.PhotoImage(Image.open('assets/snap.png'))
        self.del_pic = ImageTk.PhotoImage(Image.open('assets/pass.png'))
        self.settings_pic = ImageTk.PhotoImage(Image.open('assets/settings.png'))

        if SYSTEM == 'Rpi':
            self.camera = PiCamera()
            self.camera.resolution = (self.snap_w.get(), self.snap_h.get())
            self.camera.framerate = SNAP_FPS
            self.camera.hflip = True
            self.camera.vflip = True
            self.rawCapture = PiRGBArray(self.camera, size=(self.snap_w.get(), self.snap_h.get()))
        
        self.video_frame = Frame(self.snap_frame)
        self.video_frame.config(borderwidth=2, relief="sunken", height=SNAP_H, width=SNAP_W)
        self.video_frame.grid(row=0, column=1)
        self.video_frame.grid_propagate(0)

        self.count = IntVar()
        self.count.set(0)

        command_frame = Frame(self.snap_frame)
        command_frame.grid(row=0, column=0)
        command_frame.grid_rowconfigure(0, weight=1)
        command_frame.grid_rowconfigure(1, weight=1)
        command_frame.grid_rowconfigure(2, weight=1)
        command_frame.grid_rowconfigure(3, weight=1)
        command_frame.grid_rowconfigure(4, weight=1)
        command_frame.grid_rowconfigure(5, weight=1)
        command_frame.grid_rowconfigure(6, weight=1)
        command_frame.grid_columnconfigure(0, weight=1)

        cam_handler = lambda: self.open_cam(self)
        stop_handler = lambda: self.stop(self)
        snap_handler = lambda: self.snap(self)
        del_handler = lambda: self.del_snap(self)
        settings_handler = lambda: self.set_video_param(self)

        settings_but = Button(command_frame)
        settings_but.config(image=self.settings_pic, command=settings_handler)
        settings_but.grid(row=0, column=0, padx=10, pady=5)
        settings_ttp = ttp.ToolTip(settings_but, 'Setup Camera', msgFunc=None, delay=1, follow=True)     

        play_but = Button(command_frame)
        play_but.config(image=self.cam_pic, command=cam_handler)
        play_but.grid(row=1, column=0, padx=10, pady=5)
        play_ttp = ttp.ToolTip(play_but, 'Start Camera', msgFunc=None, delay=1, follow=True)

        stop_but = Button(command_frame)
        stop_but.config(image=self.stop_pic, command=stop_handler)
        stop_but.grid(row=2, column=0, padx=10, pady=5)
        stop_ttp = ttp.ToolTip(stop_but, 'Stop Camera', msgFunc=None, delay=1, follow=True)

        snap_but = Button(command_frame)
        snap_but.config(image=self.snap_pic, command=snap_handler)
        snap_but.grid(row=3, column=0, padx=10, pady=5)
        snap_ttp = ttp.ToolTip(snap_but, 'Snapshot', msgFunc=None, delay=1, follow=True)

        self.prev_frame = Label(command_frame, image=self.none_pic)
        self.prev_frame.config(borderwidth=2, relief="sunken", height=120, width=160)
        self.prev_frame.grid(row=4, column=0, pady=5)

        del_but = Button(command_frame)
        del_but.config(image=self.del_pic, command=del_handler)
        del_but.grid(row=5, column=0, sticky="se", pady=5)
        del_but = ttp.ToolTip(del_but, 'Remove last Snap', msgFunc=None, delay=1, follow=True)
 
        count_frame = Frame(self.snap_frame, borderwidth=2, relief="sunken")
        count_frame.grid(row=0, column=2, sticky='e', padx=20)
        count_frame.grid_columnconfigure(0, weight=1)
        count_frame.grid_rowconfigure(0, weight=1)
        count_frame.grid_rowconfigure(1, weight=1)

        snap_count_title = Label(count_frame)
        snap_count_title.config(text="Photos :", font=("Courier", 20))
        snap_count_title.grid(row=0, column=0, padx=10)

        snap_count = Label(count_frame)
        snap_count.config(font=("Courier", 20), textvariable=self.count)
        snap_count.grid(row=1, column=0, padx=10)

    def videoLoop(self):
        if SYSTEM != 'Rpi':
            while not self.stopEvent.is_set():
                if self.stopEvent.is_set():
                    break
                ret, self.video = self.vs.read()
                if ret is True:
                    self.video = imutils.resize(self.video, width=self.snap_w.get())
                    image = cv2.cvtColor(self.video, cv2.COLOR_BGR2RGB)
                    image = Image.fromarray(image)
                    try:
                        image = ImageTk.PhotoImage(image)
                    except RuntimeError:
                        break
                    if self.panel is None:
                        self.panel = Label(self.video_frame, image=image)
                        self.panel.image = image
                        self.panel.grid()
                        self.panel.place(x=SNAP_W/2, y=SNAP_H/2, anchor="center")
                    else:
                        self.panel.configure(image=image)
                        self.panel.image = image
                        self.panel.place(x=SNAP_W/2, y=SNAP_H/2, anchor="center")
                else:
                    self.stop(self, self.path)
                    break
            self.panel.image = None
            self.vs.release()
            self.frame = None
            
        else:
            for frame in self.camera.capture_continuous(self.rawCapture, format="rgb", use_video_port=True):
                if self.stopEvent.is_set():
                    self.rawCapture.truncate(0)
                    break
                self.image = frame.array
                image = Image.fromarray(self.image)
                try:
                    image = ImageTk.PhotoImage(image)
                except RuntimeError:
                    break
                if self.panel is None:
                    self.panel = Label(self.video_frame, image=image)
                    self.panel.image = image
                    self.panel.grid()
                    self.panel.place(x=SNAP_W/2, y=SNAP_H/2, anchor="center")
                else:
                    self.panel.configure(image=image)
                    self.panel.image = image
                    self.panel.place(x=SNAP_W/2, y=SNAP_H/2, anchor="center")
                self.rawCapture.truncate(0)
            self.panel.image = None
            self.frame = None

    def set_video_param(self, event):
        self.video_param_frame = tk.Toplevel()
        self.video_param_frame.geometry("%dx%d+%d+%d" % (LAYER_INFO_W, LAYER_INFO_H, 200, 200))
        self.video_param_frame.title("Set Video Size")
        self.video_param_frame.transient(self.app)
        self.video_param_frame.grab_set()

        labels = tk.Label(self.video_param_frame)
        labels.grid(row=0, column=0, sticky='nsw')
        labels.grid_rowconfigure(0, weight=1)
        labels.grid_rowconfigure(1, weight=1)
        labels.grid_rowconfigure(2, weight=1)
        labels.grid_rowconfigure(3, weight=1)
        labels.grid_columnconfigure(0, weight=1)
        labels.grid_columnconfigure(1, weight=1)
        labels.grid_columnconfigure(2, weight=1)

        label_0 = tk.Label(labels)
        label_0.config(text='Video Settings:', font=("Helvetica", 18))
        label_0.grid(row=0, column=0, sticky='new', columnspan=3, padx=10, pady=10)
        
        label_1 = tk.Label(labels)
        label_1.config(text='Width:', font=("Helvetica", 14))
        label_1.grid(row=1, column=0, sticky='nsw', padx=5, pady=10)

        self.width = tk.StringVar()
        self.width.set(str(self.snap_w.get()))
        
        val_1 = tk.Entry(labels, width=10, textvariable=self.width)
        val_1.grid(row=1, column=2, sticky='nse', padx=5, pady=10)

        self.heigth = tk.StringVar()
        self.heigth.set(str(self.snap_h.get()))

        if SYSTEM == 'Rpi':
            label_2 = tk.Label(labels)
            label_2.config(text='Heigth:', font=("Helvetica", 14))
            label_2.grid(row=2, column=0, sticky='nsw', padx=5, pady=10)

            val_2 = tk.Entry(labels, width=10, textvariable=self.heigth)
            val_2.grid(row=2, column=2, sticky='nse', padx=5, pady=10)
        else:
            self.heigth.set(str(round((3/4) * int(self.width.get()))))
            
        save_dense = lambda _: self.save_video_param(self.width, self.heigth)
        
        save_but = tk.Button(labels)
        save_but.config(text='Save', font=("Helvetica", 16))
        save_but.bind("<ButtonPress-1>", save_dense)
        save_but.bind("<Return>", save_dense)
        save_but.grid(row=3, column=1, sticky='nsew', padx=5, pady=10)

        val_1.focus_set()

    def save_video_param(self, width, heigth):
        try:
            if int(width.get()) <= SNAP_W and int(heigth.get()) <= SNAP_H:
                self.snap_w.set(int(width.get()))
                self.snap_h.set(int(heigth.get()))
                self.video_param_frame.destroy()
            else:
                showwarning("Error", "Too large value(s)")
        except ValueError:
            showwarning("Error", "Wrong value(s)")

    def open_cam(event, self):
        if self.thread.is_alive():
            showwarning("Video already running", "Please stop the video before you start again")
        else:
            self.thread = threading.Thread(target=self.videoLoop, args=())
            self.stopEvent = threading.Event()
            if SYSTEM != 'Rpi':
                self.vs = cv2.VideoCapture(0)
            sleep(0.2)
            self.thread.start()

    def stop(event, self):
        self.stopEvent.set()
        self.prev_frame.config(image=self.none_pic)
        self.count.set(0)

    def snap(event, self):
        if self.thread.is_alive():
            p = Path(self.app.snap_path.get())
            if p.exists():
                self.picname = self.app.snap_path.get() + "/" + str(time()) + ".jpg"
                if SYSTEM != 'Rpi':
                    pic = self.video
                    cv2.imwrite(self.picname, pic)
                    pic = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
                else:
                    pic = self.image
                    self.camera.capture(self.picname)
                pic = imutils.resize(pic, width=160)
                pic = Image.fromarray(pic)
                pic = ImageTk.PhotoImage(pic)
                self.prev_frame.config(image=pic)
                self.prev_frame.image = pic
                self.count.set(self.count.get() + 1)
            else:
                showwarning("No destination", "Please select a destination folder in Options")
        else:
            showwarning("No video running", "Please Start the video before you take a snap")

    def del_snap(event, self):
        try:
            dir_list = os.listdir(self.app.snap_path.get())
            if len(dir_list) > 0 and dir_list[-1].endswith(EXT_PHOTOS):
                os.remove(self.app.snap_path.get() + '/' + dir_list[-1])
                dir_list = os.listdir(self.app.snap_path.get())
                if len(dir_list) > 0 and dir_list[-1].endswith(EXT_PHOTOS):
                    image = ImageTk.PhotoImage(Image.open(self.app.snap_path.get() + '/' + dir_list[-1]).resize((160, 120), Image.ANTIALIAS))
                else:
                    image = self.none_pic
                    showwarning("File not found", "No file to remove")
                self.count.set(self.count.get() - 1)
                self.prev_frame.config(image=image)
                self.prev_frame.image = image
            else:
                image = self.none_pic
                showwarning("File not found", "No file to remove")
        except FileNotFoundError:
            showwarning("File not found", "No file to remove")

    def on_quit(self):
        if self.thread.is_alive():
            showwarning("Video running", "Please stop the video before you quit")
            return 0
        else:
            return 1
