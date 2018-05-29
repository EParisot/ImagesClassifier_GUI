# -*- coding: utf-8 -*-

from srcs.const import *
import sys

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter.scrolledtext import ScrolledText
from tkinter.font import Font

import os
import configparser
from time import time, localtime, strftime, sleep

from PIL import ImageTk, Image

import srcs.Tk_Tooltips as ttp

"""
labelisation
"""

class SecondTab(object):

    def __init__(self, app, devMode):
        self.app = app
        self.devMode = devMode
        self.label_frame = Frame(app.second_tab)
        self.label_frame.grid(row=0, column=0, stick='n')
        self.label_frame.grid_columnconfigure(0, weight=1)
        self.label_frame.grid_rowconfigure(0, weight=1)

        self.fen = {
            'fen' : None,
            'lab_photo' : None,
            'slide_height1' : None,
            'slide_height2' : None,
            'photo' : None,
            'lab_info' : None
        }
        self.fen['fen'] = Frame(self.label_frame,
                width=WIDTH_IMG, height=HEIGHT_IMG,
                borderwidth=2, relief="sunken")
        self.fen['fen'].grid(row=0, column=0, sticky='n')
        self.fen['fen'].grid_propagate(0)


        self.command_frame = Frame(self.label_frame)
        self.command_frame.grid(row=1, column=0, sticky='n')
        self.command_frame.grid_columnconfigure(0, weight=1)
        self.command_frame.grid_columnconfigure(1, weight=1)
        self.command_frame.grid_columnconfigure(2, weight=1)
        self.command_frame.grid_columnconfigure(3, weight=1)
        self.command_frame.grid_columnconfigure(4, weight=1)
        self.command_frame.grid_columnconfigure(5, weight=1)
        self.command_frame.grid_rowconfigure(0, weight=1)

        load_handler = lambda: self.load(self)
        self.reload_pic = ImageTk.PhotoImage(Image.open('assets/reload.png'))
        self.reload_but = Button(self.command_frame)
        self.reload_but.config(image=self.reload_pic, command=load_handler)
        self.reload_but.grid(row=0, column=0, padx=10)
        reload_ttp = ttp.ToolTip(self.reload_but, 'Reload labelisation',
                msgFunc=None, delay=1, follow=True)

        prev_handler = lambda: self.last_photo()
        self.prev_pic = ImageTk.PhotoImage(Image.open('assets/arrow_left.png'))
        self.prev_but = Button(self.command_frame)
        self.prev_but.config(image=self.prev_pic, command=prev_handler)
        self.prev_but.grid(row=0, column=1, padx=10)
        next_ttp = ttp.ToolTip(self.prev_but, 'Go to previous photo',
                msgFunc=None, delay=1, follow=True)

        next_handler = lambda: self.next_photo()
        self.next_pic = ImageTk.PhotoImage(Image.open('assets/arrow_right.png'))
        self.next_but = Button(self.command_frame)
        self.next_but.config(image=self.next_pic, command=next_handler)
        self.next_but.grid(row=0, column=2, padx=10)
        next_ttp = ttp.ToolTip(self.next_but, 'Go to next photo',
                msgFunc=None, delay=1, follow=True)

        rm_handler = lambda: self.del_photo()
        self.rm_pic = ImageTk.PhotoImage(Image.open('assets/trash64.png'))
        self.rm_but = Button(self.command_frame)
        self.rm_but.config(image=self.rm_pic, command=rm_handler)
        self.rm_but.grid(row=0, column=3, padx=10)
        rm_ttp = ttp.ToolTip(self.rm_but, 'Remove photo',
                msgFunc=None, delay=1, follow=True)

        self.button_frame = Frame(self.command_frame)
        self.button_frame.grid(row=0, column=4, sticky='n')
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)
        self.button_frame.grid_columnconfigure(2, weight=1)
        self.button_frame.grid_columnconfigure(3, weight=1)
        self.button_frame.grid_columnconfigure(4, weight=1)
        self.button_frame.grid_rowconfigure(0, weight=1)
        self.button_frame.grid_rowconfigure(1, weight=1)

        font = Font(family='Helvetica', size=20, weight='bold')

        label_handler0 = lambda: self.set_label(KEY_LABEL_CHARS[0])
        self.label_but0 = Button(self.button_frame)
        self.label_but0.config(height=1, width=2)
        self.label_but0['font'] = font
        self.label_but0.config(text=KEY_LABEL_CHARS[0], command=label_handler0)
        self.label_but0.grid(row=0, column=0, padx=10, pady=5)
        label_ttp0 = ttp.ToolTip(self.label_but0, 'Set label ' +
                KEY_LABEL_CHARS[0] + ' to this photo', msgFunc=None, delay=1,
                follow=True)

        label_handler1 = lambda: self.set_label(KEY_LABEL_CHARS[1])
        self.label_but1 = Button(self.button_frame)
        self.label_but1.config(height=1, width=2)
        self.label_but1['font'] = font
        self.label_but1.config(text=KEY_LABEL_CHARS[1], command=label_handler1)
        self.label_but1.grid(row=0, column=1, padx=10, pady=5)
        label_ttp1 = ttp.ToolTip(self.label_but1, 'Set label ' +
                KEY_LABEL_CHARS[1] + ' to this photo', msgFunc=None, delay=1,
                follow=True)

        label_handler2 = lambda: self.set_label(KEY_LABEL_CHARS[2])
        self.label_but2 = Button(self.button_frame)
        self.label_but2.config(height=1, width=2)
        self.label_but2['font'] = font
        self.label_but2.config(text=KEY_LABEL_CHARS[2], command=label_handler2)
        self.label_but2.grid(row=0, column=2, padx=10, pady=5)
        label_ttp2 = ttp.ToolTip(self.label_but2, 'Set label ' +
                KEY_LABEL_CHARS[2] + ' to this photo', msgFunc=None, delay=1,
                follow=True)

        label_handler3 = lambda: self.set_label(KEY_LABEL_CHARS[3])
        self.label_but3 = Button(self.button_frame)
        self.label_but3.config(height=1, width=2)
        self.label_but3['font'] = font
        self.label_but3.config(text=KEY_LABEL_CHARS[3], command=label_handler3)
        self.label_but3.grid(row=0, column=3, padx=10, pady=5)
        label_ttp3 = ttp.ToolTip(self.label_but3, 'Set label ' +
                KEY_LABEL_CHARS[3] + ' to this photo', msgFunc=None, delay=1,
                follow=True)

        label_handler4 = lambda: self.set_label(KEY_LABEL_CHARS[4])
        self.label_but4 = Button(self.button_frame)
        self.label_but4.config(height=1, width=2)
        self.label_but4['font'] = font
        self.label_but4.config(text=KEY_LABEL_CHARS[4], command=label_handler4)
        self.label_but4.grid(row=0, column=4, padx=10, pady=5)
        label_ttp4 = ttp.ToolTip(self.label_but4, 'Set label ' +
                KEY_LABEL_CHARS[4] + ' to this photo', msgFunc=None, delay=1,
                follow=True)

        label_handler5 = lambda: self.set_label(KEY_LABEL_CHARS[5])
        self.label_but5 = Button(self.button_frame)
        self.label_but5.config(height=1, width=2)
        self.label_but5['font'] = font
        self.label_but5.config(text=KEY_LABEL_CHARS[5], command=label_handler5)
        self.label_but5.grid(row=1, column=0, padx=10, pady=5)
        label_ttp5 = ttp.ToolTip(self.label_but5, 'Set label ' +
                KEY_LABEL_CHARS[5] + ' to this photo', msgFunc=None, delay=1,
                follow=True)

        label_handler6 = lambda: self.set_label(KEY_LABEL_CHARS[6])
        self.label_but6 = Button(self.button_frame)
        self.label_but6.config(height=1, width=2)
        self.label_but6['font'] = font
        self.label_but6.config(text=KEY_LABEL_CHARS[6], command=label_handler6)
        self.label_but6.grid(row=1, column=1, padx=10, pady=5)
        label_ttp6 = ttp.ToolTip(self.label_but6, 'Set label ' +
                KEY_LABEL_CHARS[6] + ' to this photo', msgFunc=None, delay=1,
                follow=True)

        label_handler7 = lambda: self.set_label(KEY_LABEL_CHARS[7])
        self.label_but7 = Button(self.button_frame)
        self.label_but7.config(height=1, width=2)
        self.label_but7['font'] = font
        self.label_but7.config(text=KEY_LABEL_CHARS[7], command=label_handler7)
        self.label_but7.grid(row=1, column=2, padx=10, pady=5)
        label_ttp7 = ttp.ToolTip(self.label_but7, 'Set label ' +
                KEY_LABEL_CHARS[7] + ' to this photo', msgFunc=None, delay=1,
                follow=True)

        label_handler8 = lambda: self.set_label(KEY_LABEL_CHARS[8])
        self.label_but8 = Button(self.button_frame)
        self.label_but8.config(height=1, width=2)
        self.label_but8['font'] = font
        self.label_but8.config(text=KEY_LABEL_CHARS[8], command=label_handler8)
        self.label_but8.grid(row=1, column=3, padx=10, pady=5)
        label_ttp8 = ttp.ToolTip(self.label_but8, 'Set label ' +
                KEY_LABEL_CHARS[8] + ' to this photo', msgFunc=None, delay=1,
                follow=True)

        label_handler9 = lambda: self.set_label(KEY_LABEL_CHARS[9])
        self.label_but9 = Button(self.button_frame)
        self.label_but9.config(height=1, width=2)
        self.label_but9['font'] = font
        self.label_but9.config(text=KEY_LABEL_CHARS[9], command=label_handler9)
        self.label_but9.grid(row=1, column=4, padx=10, pady=5)
        label_ttp9 = ttp.ToolTip(self.label_but9, 'Set label ' +
                KEY_LABEL_CHARS[9] + ' to this photo', msgFunc=None, delay=1,
                follow=True)

        self.dir_srcs = None  # directory with photos
        self.dir_dest = None  # directory with labelised photos
        self.photos = None    # list with all photos
        self.auto_next = True # go automatically to next photo

        self.load()

    def load(self, event=None):
        self.dir_srcs = self.app.cfg.get('paths', 'snap_path')
        if self.dir_srcs != '' and self.dir_srcs[-1] != '/':
            self.dir_srcs += '/'
        self.dir_dest = self.app.cfg.get('paths', 'out_path')
        if self.dir_dest != '' and self.dir_dest[-1] != '/':
            self.dir_dest += '/'
        try:
            self.photos = os.listdir(self.dir_srcs)
        except FileNotFoundError:
            self.photos = []
        self.photo_act = 0
        if len(self.photos) == 0:
            return

        for i in range(len(self.photos) - 1, -1, -1):
            remove = 1
            for ext in EXT_PHOTOS:
                if len(self.photos[i]) > len(ext) and self.photos[i][-len(ext):] == ext:
                    remove = 0
                    break
            if remove == 1:
                self.photos.pop(i)
            else:
                self.photos[i] = self.dir_srcs + self.photos[i]
        self.print_win()



    def print_win(self):
        if len(self.photos) == 0:
            return
        if self.fen['lab_photo'] != None:
            self.fen['lab_photo'].destroy()
        if self.fen['lab_info'] != None:
            self.fen['lab_info'].destroy()
        image = Image.open(self.photos[self.photo_act])
        image = image.resize((WIDTH_IMG, HEIGHT_IMG - 50), Image.ANTIALIAS)
        self.fen['photo'] = ImageTk.PhotoImage(image)
        if self.fen['slide_height1'] == None:
            self.fen['slide_height1'] = Scale(self.fen['fen'],from_=image.size[1],
                    to=0, orient=VERTICAL, length=HEIGHT_IMG - 50)
            self.fen['slide_height1'].grid(row=0, column=1)
        self.fen['lab_photo'] = Label(self.fen['fen'], image=self.fen['photo'])
        self.fen['lab_photo'].grid(row=0, column=0)
        if self.fen['slide_height2'] == None:
            self.fen['slide_height2'] = Scale(self.fen['fen'], from_=image.size[1],
                    to=0, orient=VERTICAL, length=HEIGHT_IMG - 50)
            self.fen['slide_height2'].grid(row=0, column=2)
        self.fen['lab_info'] = Label(self.fen['fen'], width=32, height=2, font=("Courier", 40))
        self.fen['lab_info']['text'] = 'label: ' + self.get_label() + '\t\t' + str(self.photo_act) + '/' + str(len(self.photos))
        self.fen['lab_info'].grid(row=1, column=0)


    def last_photo(self):
        if len(self.photos) == 0:
            return
        self.photo_act -= 1
        if self.photo_act < 0:
            self.photo_act = len(self.photos) - 1
        self.print_win()

    def next_photo(self):
        if len(self.photos) == 0:
            return
        self.photo_act += 1
        if self.photo_act >= len(self.photos):
            self.photo_act = 0
        self.print_win()


    def event_win(self, event):
        if len(self.photos) == 0:
            return
        self.set_label(event.char)


    def set_label(self, label):
        if len(self.photos) == 0:
            return
        new = self.dir_dest
        if self.get_label() == '':
            if self.photos[self.photo_act].split('/')[-1][0] == '_':
                new += label + self.photos[self.photo_act].split('/')[-1]
            else:
                new += label + '_' + self.photos[self.photo_act].split('/')[-1]
        else:
            new += label + '_' + self.photos[self.photo_act].split('/')[-1].split('_')[1:][0]
        if self.devMode:
            print(GREEN + 'RENAME: ' + EOC + new)
        try:
            os.rename(self.photos[self.photo_act], new)
        except FileExistsError:
            pass
        self.photos[self.photo_act] = new
        if self.auto_next == True:
            self.next_photo()
        else:
            self.print_win()


    def get_label(self):
        if len(self.photos) == 0:
            return
        try:
            char = self.photos[self.photo_act].split('/')[-1].split('_')[0]
            if len(char) == 1 and char in KEY_LABEL_CHARS:
                return char
        except:
            pass
        return ''


    def del_photo(self):
        if len(self.photos) == 0:
            return
        if self.devMode:
            print(RED + 'REMOVE: ' + EOC + self.photos[self.photo_act])
        os.remove(self.photos[self.photo_act])
        self.photos.pop(self.photo_act)
        if self.photo_act >= len(self.photos):
            self.photo_act = 0
        self.print_win()
