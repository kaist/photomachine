from tkinter import *
from tkinter.ttk import *
from pathlib import Path
from tkinter import filedialog
import webbrowser


class Plugin:
    def __init__(self):
        self.category='output'
        self.name=_('To VK album')
        self.need_config=True


    def start_config(self,frame,plug):
        self.cur_path=Path(plug.path)

        Label(frame,text=_('In order to get a token, you need to log in to the VK. To do this, just click on the button.'),wraplength=400).grid(row=0,column=0,padx=5,pady=5,sticky=W,columnspan=2)
        self.f_image=PhotoImage(file=str(self.cur_path/'vk.png'))
        Button(frame,text=_('Authorize'),image=self.f_image,command=self.open_auth,compound='left').grid(row=1,column=0,columnspan=2,padx=5,pady=10)


        Label(frame,text=_('Token')).grid(row=2,column=0,padx=5,pady=5,sticky=W)
        self.key_var=StringVar()
        self.key_var.set(plug.settings.get('key',''))
        self.my=Entry(frame,width=40,textvariable=self.key_var)
        self.my.grid(row=2,column=1,padx=5,pady=5,sticky=E)

        
        Label(frame,text=_('Link to album')).grid(row=3,column=0,padx=5,pady=5,sticky=W)
        self.album_var=StringVar()
        self.album_var.set(plug.settings.get('album',''))
        Entry(frame,width=40,textvariable=self.album_var).grid(row=3,column=1,padx=5,pady=5,sticky=E)


        Label(frame,text=_('Caption')).grid(row=4,column=0,padx=5,pady=5,sticky=W)
        self.caption_var=StringVar()
        self.caption_var.set(plug.settings.get('caption',''))
        self.capt=Entry(frame,width=40,textvariable=self.caption_var).grid(row=4,column=1,padx=5,pady=5,sticky=E)   

 
    def open_auth(self):
        webbrowser.open('https://photo-machine.ru/vk_connect/')

    def save_config(self):
        d = {'key': self.key_var.get()}
        d['album']=self.album_var.get()
        d['caption']=self.caption_var.get()
        return d

    def select_folder(self):
        d=filedialog.askdirectory()
        self.path_var.set(d)
        self.sframe.focus_force()




