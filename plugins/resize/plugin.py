from tkinter import *
from tkinter.ttk import *
from pathlib import Path
from app.utils import *

class Plugin:
    def __init__(self):
        self.category='process'
        self.name=_('Thumbnail')
        self.need_config=True

    def start_config(self,frame,plug):
        self.mxvar=IntVar(value=plug.settings.get('width',1920))
        self.myvar=IntVar(value=plug.settings.get('height',1920))

        Label(frame,text=_('Max width (px.)')).grid(row=0,column=0,padx=5,pady=5)
        Entry(frame,width=7,textvariable=self.mxvar).grid(row=0,column=1,padx=5,pady=5)

        Label(frame,text=_('Max height (px.)')).grid(row=1,column=0,padx=5,pady=5)
        Entry(frame,width=7,textvariable=self.myvar).grid(row=1,column=1,padx=5,pady=5)

    def save_config(self):
        d = {'width': int(self.mxvar.get())}
        d['height']=int(self.myvar.get())
        return d





