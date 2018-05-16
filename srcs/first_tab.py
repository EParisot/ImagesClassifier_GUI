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

import imutils
from PIL import Image, ImageTk
import configparser
from imutils.video import VideoStream
import cv2
import numpy as np
import threading

import Tk_Tooltips

class FirstTab():

    def __init__(self, app):
        self.app = app
        self.snap_frame = Frame(self.app.first_tab)
        self.snap_frame.grid(row=0, column=1)
        self.snap_frame.grid_columnconfigure(0, weight=1)
        self.snap_frame.grid_rowconfigure(0, weight=1)
        self.snap_frame.grid_rowconfigure(1, weight=1)

        self.frame = None
        self.vs = None
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.stopEvent = threading.Event()
        self.panel = None
        self.image = None

        self.none_pic = ImageTk.PhotoImage(Image.open('assets/prev.png'))
        self.cam_pic = ImageTk.PhotoImage(Image.open('assets/webcam.png'))
        self.stop_pic = ImageTk.PhotoImage(Image.open('assets/stop.png'))
        self.snap_pic = ImageTk.PhotoImage(Image.open('assets/snap.png'))
        self.del_pic = ImageTk.PhotoImage(Image.open('assets/pass.png'))

        self.video_frame = Frame(self.snap_frame)
        self.video_frame.config(borderwidth=2, relief="sunken", height=500, width=810)
        self.video_frame.grid(row=0, column=0)
        self.video_frame.grid_propagate(0)

        self.count = IntVar()
        self.count.set(0)

        command_frame = Frame(self.snap_frame)
        command_frame.grid(row=1, column=0, sticky='n')
        command_frame.grid_columnconfigure(0, weight=1)
        command_frame.grid_columnconfigure(1, weight=1)
        command_frame.grid_columnconfigure(2, weight=1)
        command_frame.grid_columnconfigure(3, weight=1)
        command_frame.grid_columnconfigure(4, weight=1)
        command_frame.grid_columnconfigure(5, weight=1)
        command_frame.grid_rowconfigure(0, weight=1)

        cam_handler = lambda: self.open_cam(self)
        stop_handler = lambda: self.stop(self)
        snap_handler = lambda: self.snap(self)
        del_handler = lambda: self.del_snap(self)

        play_but = Button(command_frame)
        play_but.config(image=self.cam_pic, command=cam_handler)
        play_but.grid(row=0, column=0, padx=10)
        play_ttp = Tk_Tooltips.ToolTip(play_but, 'Start Camera', msgFunc=None, delay=1, follow=True)

        stop_but = Button(command_frame)
        stop_but.config(image=self.stop_pic, command=stop_handler)
        stop_but.grid(row=0, column=1, padx=10)
        stop_ttp = Tk_Tooltips.ToolTip(stop_but, 'Stop Camera', msgFunc=None, delay=1, follow=True)

        snap_but = Button(command_frame)
        snap_but.config(image=self.snap_pic, command=snap_handler)
        snap_but.grid(row=0, column=2, padx=10)
        snap_ttp = Tk_Tooltips.ToolTip(snap_but, 'Snapshot', msgFunc=None, delay=1, follow=True)

        self.prev_frame = Label(command_frame, image=self.none_pic)
        self.prev_frame.config(borderwidth=2, relief="sunken", height=120, width=160)
        self.prev_frame.grid(row=0, column=3)

        del_but = Button(command_frame)
        del_but.config(image=self.del_pic, command=del_handler)
        del_but.grid(row=0, column=4, sticky="se")
        del_but = Tk_Tooltips.ToolTip(del_but, 'Remove last snapshot', msgFunc=None, delay=1, follow=True)
 
        count_frame = Frame(command_frame)
        count_frame.grid(row=0, column=5, sticky='w')
        count_frame.grid_columnconfigure(0, weight=1)
        count_frame.grid_rowconfigure(0, weight=1)
        count_frame.grid_rowconfigure(0, weight=1)

        snap_count_title = Label(count_frame)
        snap_count_title.config(text="Snapshots :", font=("Helvetica", 16))
        snap_count_title.grid(row=0, column=0, padx=10)

        snap_count = Label(count_frame)
        snap_count.config(font=("Helvetica", 16), textvariable=self.count)
        snap_count.grid(row=1, column=0, padx=10)

    def videoLoop(self):
        while not self.stopEvent.is_set():
            if self.stopEvent.is_set():
                break
            #####SYSTEM DEPENDENT
            ret, self.video = self.vs.read()
            if ret is True:
                self.video = imutils.resize(self.video, width=800)
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
                else:
                    self.panel.configure(image=image)
                    self.panel.image = image
            else:
                self.stop(self, self.path)
                break
        self.panel.image = None
        self.vs.release()
        self.frame = None

    def open_cam(event, self):
        if self.thread.is_alive():
            showwarning("Video already running", "Please stop the video before you start again")
        else:
            self.thread = threading.Thread(target=self.videoLoop, args=())
            self.stopEvent = threading.Event()
            self.vs = cv2.VideoCapture(0)
            sleep(0.2)
            self.thread.start()

    def stop(event, self):
        self.stopEvent.set()
        self.prev_frame.config(image=self.none_pic)
        self.count.set(0)

    def snap(event, self):
        if self.thread.is_alive():
            self.picname = self.app.snap_path + "/" + str(time()) + ".jpg"
            pic = self.video
            cv2.imwrite(self.picname, pic)
            pic = imutils.resize(pic, width=160)
            pic = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
            pic = Image.fromarray(pic)
            pic = ImageTk.PhotoImage(pic)
            self.prev_frame.config(image=pic)
            self.prev_frame.image = pic
            self.count.set(self.count.get() + 1)
        else:
            showwarning("No video running", "Please start the video before you take a snap")

    def del_snap(event, self):
        os.remove(self.picname)
        self.count.set(self.count.get() - 1)
        self.prev_frame.config(image=self.none_pic)

    def on_quit(self):
        if self.thread.is_alive():
            showwarning("Video running", "Please stop the video before you quit")
        else:
            self.app.quit()
