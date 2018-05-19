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
import numpy as np
import threading

import Tk_Tooltips

class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.bind("<KeyPress>", self.onKeyPress)
        self.bind("<KeyRelease>", self.onKeyRelease)

        self.l_ctrl_pressed = False;

        self.title("Patate for Kids")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1000)

        style = ttk.Style()
        current_theme = style.theme_use()

        self.lang_pic = ImageTk.PhotoImage(Image.open('assets/lang.png'))
        self.dir_open_pic = ImageTk.PhotoImage(Image.open('assets/dir_open.png'))

        self.cfg = configparser.ConfigParser()
        self.cfg.read(FILE_CONFIG)
        self.lang = self.cfg.get('general', 'language')
        self.snap_path = self.cfg.get('paths', 'snap_path')

        self.options_but = Button(self, text="Options", font=("Helvetica", 16), command=self.open_options)
        self.options_but.grid(row=0, column=0, sticky="nw")

        self.tabs = ttk.Notebook(self)
        self.tabs.grid(row=1, column=0, sticky='nsew')
        self.tabs.grid_columnconfigure(0, weight=1)
        self.tabs.grid_rowconfigure(0, weight=1)
        style.theme_settings(current_theme, {"TNotebook.Tab": {"configure": {"padding": [20, 5]}}})

        self.first_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.first_tab, text=SNAP_NAME, compound=LEFT)
        self.first_tab.grid_columnconfigure(0, weight=1)
        self.first_tab.grid_rowconfigure(0, weight=1)
        self.second_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.second_tab, text=LABEL_NAME, compound=LEFT)
        self.second_tab.grid_columnconfigure(0, weight=1)
        self.second_tab.grid_rowconfigure(0, weight=1)
        self.third_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.third_tab, text=MODEL_NAME, compound=LEFT)
        self.third_tab.grid_columnconfigure(0, weight=1)
        self.third_tab.grid_rowconfigure(0, weight=1)
        self.fourth_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.fourth_tab, text=TRAIN_NAME, compound=LEFT)
        self.fourth_tab.grid_columnconfigure(0, weight=1)
        self.fourth_tab.grid_rowconfigure(0, weight=1)


    def onKeyPress(self, event):
        """
        define action with keyboard shortcut
        """
        if event.keysym == KEY_OPTION:
            self.open_options()
        elif event.keysym == KEY_QUIT:
            self.on_Quit()
        elif event.keysym == KEY_CTRL_L:
            self.l_ctrl_pressed = True;
            print(YELLOW + "key press: " + EOC + "Control_L")
        else:
            print(YELLOW + 'key press: ' + EOC + event.keysym)

        # if we are in label
        if self.tabs.tab(self.tabs.select(), "text") == LABEL_NAME:
            if event.keysym == NEXT_PHOTO:
                self.second_tab.next_photo()
            elif event.keysym == LAST_PHOTO:
                self.second_tab.last_photo()
            
    def onKeyRelease(self, event):
        if event.keysym == KEY_CTRL_L:
            self.l_ctrl_pressed = False;
            print(YELLOW + "key release: " + EOC + "Control_L")


    def open_options(self):
        self.options_frame = Toplevel()
        self.options_frame.geometry("800x600")
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
        path1_button.config(text='Browse', font=("Helvetica", 14), command=self.get_IN_Folder)
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
        path2_button.config(text='Browse', font=("Helvetica", 14), command=self.get_OUT_Folder)
        path2_button.grid(row=1, column=3, padx=10)

        handler = lambda: self.close_options(self.options_frame, lang_int)
        btn = Button(self.options_frame, text="Save / Close", font=("Helvetica", 16), command=handler)
        btn.grid(row=6, column=0)

    def get_IN_Folder(self):
        IN_path = askdirectory()
        self.options_frame.focus_set()
        if len(IN_path) != 0:
            self.path1_result.delete(0, END)
            self.path1_result.insert(END, IN_path)

    def get_OUT_Folder(self):
        OUT_path = askdirectory()
        self.options_frame.focus_set()
        if len(OUT_path) != 0:
            self.path2_result.delete(0, END)
            self.path2_result.insert(END, OUT_path)


    def close_options(self, options_frame, lang_int):
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

        with open(FILE_CONFIG, 'w') as f:
            self.cfg.write(f)

        if options_frame:
            options_frame.destroy()

    def on_Quit(self):
        self.first_tab.on_quit()
