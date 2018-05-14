# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter.scrolledtext  import ScrolledText

import os
from PIL import Image, ImageTk
import configparser
from time import time, localtime, strftime, sleep

import imutils
from imutils.video import VideoStream
import cv2
import numpy as np
import threading

#################################################################################
'''
This is a graphic implementation of the famous "Patate42"
'''
#################################################################################

class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Patate for ids")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)


        self.lang_pic = ImageTk.PhotoImage(Image.open('Pictures\\lang.png'))
        self.dir_open_pic = ImageTk.PhotoImage(Image.open('Pictures\\dir_open.png'))
        
        self.cfg = configparser.ConfigParser()
        self.cfg.read('config.cfg')
        self.lang = self.cfg.get('general', 'language')
        self.snap_path = self.cfg.get('paths', 'snap_path')

        self.menu = Menu(self)
        self.menu.add_command(label="Options", command=self.Open_options)
        self.config(menu=self.menu)

        self.tabs = ttk.Notebook(self)
        self.tabs.grid(row=0, column=0, sticky='nsew')
        self.tabs.grid_columnconfigure(0, weight=1)
        self.tabs.grid_rowconfigure(0, weight=1)

        self.first_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.first_tab, text='Snap', compound=LEFT)
        self.first_tab.grid_columnconfigure(0, weight=1)
        self.first_tab.grid_rowconfigure(0, weight=1)
        self.first_tab.grid_rowconfigure(1, weight=10)
        self.first_tab.grid_rowconfigure(2, weight=1)

        self.second_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.second_tab, text='Labelize', compound=LEFT)
        self.second_tab.grid_columnconfigure(0, weight=1)
        self.second_tab.grid_rowconfigure(0, weight=1)
        self.second_tab.grid_rowconfigure(1, weight=100)

        self.third_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.third_tab, text='Train', compound=LEFT)
        self.third_tab.grid_columnconfigure(0, weight=1)
        self.third_tab.grid_rowconfigure(0, weight=1)
        self.third_tab.grid_rowconfigure(1, weight=100)

        
    def Open_options(self):
        self.options_frame = Toplevel()
        self.options_frame.geometry("900x600")
        self.options_frame.title("Options")

        self.options_frame.grid()
        self.options_frame.grid_columnconfigure(0, weight=1)
        self.options_frame.grid_rowconfigure(0, weight=1)
        self.options_frame.grid_rowconfigure(1, weight=1)
        self.options_frame.grid_rowconfigure(2, weight=1)
        self.options_frame.grid_rowconfigure(3, weight=1)
        self.options_frame.grid_rowconfigure(4, weight=1)
        self.options_frame.grid_rowconfigure(5, weight=1)
        self.options_frame.grid_rowconfigure(6, weight=1)

        general_label = Label(self.options_frame, text='General Options : ', font=("Helvetica", 16))
        general_label.grid(row=0, column=0, padx=10, sticky='w')

        option_frame = Frame(self.options_frame)
        option_frame.grid(row=1, column=0, sticky='n')
        option_frame.grid_columnconfigure(0, weight=1)
        option_frame.grid_columnconfigure(1, weight=1)
        option_frame.grid_columnconfigure(2, weight=1)
        option_frame.grid_columnconfigure(3, weight=1)
        option_frame.grid_rowconfigure(0, weight=1)
        option_frame.grid_rowconfigure(1, weight=1)

        option1_pic = Label(option_frame, image=self.lang_pic)
        option1_pic.grid(row=0, column=0, padx=10, pady=10)
        option1_label = Label(option_frame)
        option1_label.config(text='Language : ', font=("Helvetica", 16))
        option1_label.grid(row=0, column=1, sticky='w')
        option1_result = Frame(option_frame)
        option1_result.grid(row=0, column=2, sticky='w')
        option1_result.grid_columnconfigure(0, weight=1)
        option1_result.grid_columnconfigure(1, weight=1)
        option1_result.grid_rowconfigure(0, weight=1)

        lang_int = IntVar()
        option_en = Radiobutton(option1_result)
        option_en.config(text='En', font=("Helvetica", 16), variable=lang_int, value=1)
        option_en.grid(row=0, column=1)
        option_fr = Radiobutton(option1_result)
        option_fr.config(text='Fr', font=("Helvetica", 16), variable=lang_int, value=2)
        option_fr.grid(row=0, column=2)
        if self.cfg.get('general', 'language') == 'en-EN':
            option_en.select()
        elif self.cfg.get('general', 'language') == 'fr-FR':
            option_fr.select()


        paths_label = Label(self.options_frame, text='Default Folders : ', font=("Helvetica", 16))
        paths_label.grid(row=2, column=0, padx=10, sticky='w')

        paths_frame = Frame(self.options_frame)
        paths_frame.grid(row=3, column=0, sticky='n')
        paths_frame.grid_columnconfigure(0, weight=1)
        paths_frame.grid_columnconfigure(1, weight=1)
        paths_frame.grid_columnconfigure(2, weight=1)
        paths_frame.grid_columnconfigure(3, weight=1)
        paths_frame.grid_rowconfigure(0, weight=1)
        paths_frame.grid_rowconfigure(1, weight=1)

        path1_pic = Label(paths_frame, image=self.dir_open_pic)
        path1_pic.grid(row=0, column=0, padx=10, pady=10)
        path1_label = Label(paths_frame)
        path1_label.config(text='IN Folder : ', font=("Helvetica", 16))
        path1_label.grid(row=0, column=1, sticky='w')
        self.path1_result = Entry(paths_frame, width=35, font=("Helvetica", 12), justify=CENTER)
        self.path1_result.insert(END, self.cfg.get('paths', 'snap_path'))
        self.path1_result.grid(row=0, column=2, sticky='w')
        self.path1_result.grid_columnconfigure(0, weight=1)
        self.path1_result.grid_columnconfigure(1, weight=1)
        self.path1_result.grid_rowconfigure(0, weight=1)
        path1_button = Button(paths_frame)
        path1_button.config(text='Browse', font=("Helvetica", 14), command=self.Get_IN_Folder)
        path1_button.grid(row=0, column=3, padx=10)


        path2_pic = Label(paths_frame, image=self.dir_open_pic)
        path2_pic.grid(row=1, column=0, padx=10, pady=10)
        path2_label = Label(paths_frame)
        path2_label.config(text='OUT Folder : ', font=("Helvetica", 16))
        path2_label.grid(row=1, column=1, sticky='w')
        self.path2_result = Entry(paths_frame, width=35, font=("Helvetica", 12), justify=CENTER)
        self.path2_result.insert(END, self.cfg.get('paths', 'out_path'))
        self.path2_result.grid(row=1, column=2, sticky='w')
        self.path2_result.grid_columnconfigure(0, weight=1)
        self.path2_result.grid_columnconfigure(1, weight=1)
        self.path2_result.grid_rowconfigure(0, weight=1)
        path2_button = Button(paths_frame)
        path2_button.config(text='Browse', font=("Helvetica", 14), command=self.Get_OUT_Folder)
        path2_button.grid(row=1, column=3, padx=10)

        
        handler = lambda: self.Close_options(self.options_frame, lang_int)
        btn = Button(self.options_frame, text="Save / Close", font=("Helvetica", 16), command=handler)
        btn.grid(row=6, column=0)

    def Get_IN_Folder(self):
        IN_path = askdirectory()
        self.options_frame.focus_set()
        if len(IN_path) != 0:
            self.path1_result.delete(0, END)
            self.path1_result.insert(END, IN_path)

    def Get_OUT_Folder(self):
        OUT_path = askdirectory()
        self.options_frame.focus_set()
        if len(OUT_path) != 0:
            self.path2_result.delete(0, END)
            self.path2_result.insert(END, OUT_path)


    def Close_options(self,options_frame, lang_int):
        if lang_int.get() == 1:
            self.cfg.set('general', 'language', 'en-EN')
            self.lang = 'en-EN'
        if lang_int.get() == 2:
            self.cfg.set('general', 'language', 'fr-FR')
            self.lang = 'fr-FR'
        self.IN_path = self.path1_result.get()
        self.OUT_path = self.path2_result.get()
        self.cfg.set('paths', 'out_path', self.OUT_path)
        self.cfg.set('paths', 'snap_path', self.IN_path)

        with open('config.cfg', 'w') as f:
            self.cfg.write(f)

        if options_frame :
            options_frame.destroy()


################################################################################

class FirstTab():
    
    def __init__(self):
        self.snap_frame = Frame(app.first_tab)
        self.snap_frame.grid(row=0, column=0, sticky='n')
        self.snap_frame.grid_columnconfigure(0, weight=1)
        self.snap_frame.grid_rowconfigure(0, weight=1)
        self.snap_frame.grid_rowconfigure(1, weight=1)

        self.frame = None
        self.vs = None
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.stopEvent = threading.Event()
        app.wm_protocol("WM_DELETE_WINDOW", self.onQuit)
        self.panel = None
        self.image = None

        self.video_frame = Frame(self.snap_frame)
        self.video_frame.config(borderwidth=2, relief="sunken", height=640, width=810)
        self.video_frame.grid(row=0, column=0)

        command_frame = Frame(self.snap_frame)
        command_frame.grid(row=1, column=0, sticky='n')
        command_frame.grid_columnconfigure(0, weight=1)
        command_frame.grid_columnconfigure(1, weight=1)
        command_frame.grid_columnconfigure(2, weight=1)
        command_frame.grid_rowconfigure(0, weight=1)

        cam_handler = lambda: self.open_cam(self)
        stop_handler = lambda: self.stop(self)
        snap_handler = lambda: self.snap(self)

        play_but = Button(command_frame)
        play_but.config(text='Play', font=("Helvetica", 14), command=cam_handler)
        play_but.grid(row=1, column=0, padx=10)

        stop_but = Button(command_frame)
        stop_but.config(text='Stop', font=("Helvetica", 14), command=stop_handler)
        stop_but.grid(row=1, column=1, padx=10) 

        snap_but = Button(command_frame)
        snap_but.config(text='Snap', font=("Helvetica", 14), command=snap_handler)
        snap_but.grid(row=1, column=2, padx=10)

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
                    self.panel = tk.Label(self.video_frame, image=image)
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

    def snap(event, self):
        picname = app.snap_path + "/" + str(time()) + ".jpg"
        cv2.imwrite(picname, self.video)

    def onQuit(self):
        if self.thread.is_alive():
            showwarning("Video running", "Please stop the video before you quit")
        else:
            app.quit()
            
################################################################################

class SecondTab():

    def __init__(self):
        self.labelize_frame = Frame(app.second_tab)
        self.labelize_frame.grid(row=0, column=0, stick='n')
        self.labelize_frame.grid_columnconfigure(0, weight=1)
        self.labelize_frame.grid_rowconfigure(0, weight=1)

################################################################################

class ThirdTab():
    
    def __init__(self):
        top_panel = Frame(app.third_tab)
        top_panel.grid(row=0, column=0, stick='n')
        top_panel.grid_columnconfigure(0, weight=1)
        top_panel.grid_rowconfigure(0, weight=1)


################################################################################

app = App()

app.first_tab = FirstTab()
app.second_tab = SecondTab()
app.third_tab = ThirdTab()

app.mainloop()

################################################################################
