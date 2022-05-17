from tkinter import *
from tkinter.ttk import *
from pathlib import Path
from tkinter import filedialog
import webbrowser

class Plugin:
    def __init__(self):
        self.category='input'
        self.name=_('From Telegram Group')
        self.need_config=True


    def start_config(self,frame,plug):
        self.cur_path=Path(plug.path)

        Label(frame,text=_('Ask the bot @photomachine_bot for the key'),wraplength=400).grid(row=0,column=0,padx=5,pady=5,sticky=W,columnspan=2)
        self.f_image=PhotoImage(file=str(self.cur_path/'tg.png'))
        Button(frame,text=_('Ask @photomachine_bot'),image=self.f_image,command=self.open_auth,compound='left').grid(row=1,column=0,columnspan=2,padx=5,pady=10)



        Label(frame,text=_('Key')).grid(row=2,column=0,padx=5,pady=5,sticky=W)
        self.key_var=StringVar()
        self.key_var.set(plug.settings.get('key',''))
        self.my=Entry(frame,width=30,textvariable=self.key_var)
        self.my.grid(row=2,column=1,padx=5,pady=5,sticky=E)

    
    def open_auth(self):
        webbrowser.open('https://t.me/photomachine_bot')

    def save_config(self):
        return {'key': self.key_var.get()}

    def select_folder(self):
        d=filedialog.askdirectory()
        self.path_var.set(d)
        self.sframe.focus_force()




