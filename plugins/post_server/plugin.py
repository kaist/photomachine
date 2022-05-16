from tkinter import *
from tkinter.ttk import *
from pathlib import Path
from tkinter import filedialog
import webbrowser


class Plugin:
    def __init__(self):
        self.category='output'
        self.name=_('HTTP POST')
        self.need_config=True


    def start_config(self,frame,plug):
        self.cur_path=Path(plug.path)
        Label(frame,text=_('POST url')).grid(row=0,column=0,padx=5,pady=5,sticky=W)
        self.url_var=StringVar()
        self.url_var.set(plug.settings.get('url','https://'))
        Entry(frame,width=40,textvariable=self.url_var).grid(row=0,column=1,padx=5,pady=5,sticky=E)



    def save_config(self):
        return {'url': self.url_var.get()}






