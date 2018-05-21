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

from PIL import ImageTk, Image

import srcs.Tk_Tooltips as ttp

"""
labelisation
"""

class SecondTab(object):

    def __init__(self, app):
        self.app = app
        self.label_frame = Frame(app.second_tab)
        self.label_frame.grid(row=0, column=0, stick='n')
        self.label_frame.grid_columnconfigure(0, weight=1)
        self.label_frame.grid_rowconfigure(0, weight=1)

        self.fen = {
            'fen' : None,
            'lab_photo' : None,
            'photo' : None,
            'lab_info' : None
        }
        self.fen['fen'] = Frame(self.label_frame,
                width=WIDTH_IMG, height=HEIGHT_IMG)
        self.fen['fen'].grid(row=0, column=0, sticky='n')


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

        self.dir_srcs = None  # directory with photos
        self.dir_dest = None  # directory with labelised photos
        self.photos = None    # list with all photos

        self.load()
        self.print_win()


    def load(self, event=None):
        self.dir_srcs = self.app.cfg.get('paths', 'snap_path')
        self.dir_dest = self.app.cfg.get('paths', 'out_path')
        self.photos = os.listdir(self.dir_srcs)
        self.photo_act = 0
        if len(self.photos) == 0:
            print(RED + 'ERROR: ' + EOC + 'first tab -> no photos')
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
                self.photos[i] = self.dir_srcs + '/' + self.photos[i]



    def print_win(self):
        if self.fen['lab_photo'] != None:
            self.fen['lab_photo'].destroy()
        if self.fen['lab_info'] != None:
            self.fen['lab_info'].destroy()
        image = Image.open(self.photos[self.photo_act])
        image = image.resize((WIDTH_IMG, HEIGHT_IMG - 50), Image.ANTIALIAS)
        self.fen['photo'] = ImageTk.PhotoImage(image)
        self.fen['lab_photo'] = Label(self.fen['fen'], image=self.fen['photo'])
        self.fen['lab_photo'].pack(side=TOP)
        self.fen['lab_info'] = Label(self.fen['fen'], width=32, height=2, font=("Courier", 40))
        self.fen['lab_info']['text'] = "self.get_label()" + '\t\t' + str(self.photo_act) + '/' + str(len(self.photos))
        self.fen['lab_info'].pack(side=BOTTOM)


    def last_photo(self):
        self.photo_act -= 1
        if self.photo_act < 0:
            self.photo_act = len(self.photos) - 1
        self.print_win()

    def next_photo(self):
        self.photo_act += 1
        if self.photo_act >= len(self.photos):
            self.photo_act = 0
        self.print_win()



#    def __init__(self, photos, auto_next=True, width=800, height=600):
#        self.photos_dir = photos
#        self.photo_act = 0
#        self.fen = {
#            'fen' : None,
#            'lab_photo' : None,
#            'photo' : None,
#            'lab_info' : None
#        }
#        self.width = width
#        self.height = height
#        self.width_img = self.width
#        self.height_img = self.height - 50
#        self.auto_next = auto_next
#
#
#    def init_key(self):
#        self.fen['fen'].bind("<Escape>", self.quit_win)
#        self.fen['fen'].bind("<Right>", self.next_photo)
#        self.fen['fen'].bind("<Left>", self.last_photo)
#        self.fen['fen'].bind("<Up>", self.del_photo)
#        self.fen['fen'].bind("<KeyPress>", self.event_win)
#
#
#    def init_win(self, width=0, height=0):
#        self.width = width if width != 0 else self.width
#        self.width_img = width if width != 0 else self.width_img
#        self.height_img = height - 50 if height != 0 else self.height_img
#        self.fen['fen'] = Tk()
#        self.fen['fen'].title('lab_photo')
#        self.print_win()
#        self.init_key()
#        self.fen['fen'].mainloop()
#
#    def init_key(self):
#        self.fen['fen'].bind("<Escape>", self.quit_win)
#        self.fen['fen'].bind("<Right>", self.next_photo)
#        self.fen['fen'].bind("<Left>", self.last_photo)
#        self.fen['fen'].bind("<Up>", self.del_photo)
#        self.fen['fen'].bind("<KeyPress>", self.event_win)
#
#    def quit_win(self, event):
#        self.fen['fen'].destroy()
#        self.fen['fen'].quit()
#
#    def event_win(self, event):
#        if event.char in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
#            self.set_label(event.char)
#            if self.auto_next == True:
#                self.next_photo(None)
#            else:
#                self.print_win()
#
#    def del_photo(self, event):
#        print(c.RED + 'REMOVE: ' + c.EOC + self.photos[self.photo_act])
#        os.remove(self.photos_dir + self.photos[self.photo_act])
#        self.photos.pop(self.photo_act)
#        if len(self.photos) == 0:
#            print(c.MAGENTA + 'THE END' + c.EOC)
#            self.quit_win(None)
#            exit(0)
#        if self.photo_act >= len(self.photos):
#            self.photo_act = 0
#        self.print_win()
#
#
#    def print_win(self):
#        if self.fen['lab_photo'] != None:
#            self.fen['lab_photo'].destroy()
#        if self.fen['lab_info'] != None:
#            self.fen['lab_info'].destroy()
#        image = Image.open(self.photos_dir + self.photos[self.photo_act])
#        image = image.resize((self.width_img, self.height_img), Image.ANTIALIAS)
#        self.fen['photo'] = ImageTk.PhotoImage(image)
#        self.fen['lab_photo'] = Label(self.fen['fen'], image=self.fen['photo'])
#        self.fen['lab_photo'].pack(side=TOP)
#        self.fen['lab_info'] = Label(self.fen['fen'], width=32, height=2, font=("Courier", 40))
#        self.fen['lab_info']['text'] = self.get_label() + '\t\t' + str(self.photo_act) + '/' + str(len(self.photos))
#        self.fen['lab_info'].pack(side=BOTTOM)
#
#
#    def get_label(self):
#        try:
#            char = self.photos[self.photo_act].split('_')[0]
#            if len(char) == 1 and char.isdigit():
#                return char
#        except:
#            pass
#        return ''
#
#    def set_label(self, label):
#        new = ''
#        if self.get_label() == '':
#            if self.photos[self.photo_act][0] == '_':
#                new = label + self.photos[self.photo_act]
#            else:
#                new = label + '_' + self.photos[self.photo_act]
#        else:
#            new =  label + '_' + self.photos[self.photo_act].split('_')[1:][0]
#        print(c.GREEN + 'RENAME: ' + c.EOC + new)
#        os.rename(self.photos_dir + self.photos[self.photo_act], self.photos_dir + new)
#        self.photos[self.photo_act] = new
