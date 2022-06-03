from tkinter import *
from tkinter.ttk import *
from pathlib import Path
from tkinter import filedialog

class Plugin:
    def __init__(self):
        self.category='output'
        self.name=_('Save original')
        self.need_config=True


    def start_config(self,frame,plug):
        self.cur_path=Path(plug.path)
        self.sframe=frame
        self.path_var=StringVar()
        self.path_entry=Entry(frame,state=DISABLED,textvariable=self.path_var,width=40)
        self.path_var.set(plug.settings.get('path',''))
        self.path_entry.grid(row=0,column=0,padx=5,pady=5,sticky=W)
        self.f_image=PhotoImage(file=str(self.cur_path/'folder.png'))
        Button(frame,text=_('Select folder'),compound='left',image=self.f_image,command=self.select_folder).grid(row=0,column=1,padx=5,pady=5,sticky=W)

        self.delete_var=IntVar(value=plug.settings.get('delete',0))
        Checkbutton(frame, text=_("Delete original after saving (!!!)"),variable=self.delete_var).grid(row=1,column=0,columnspan=2,padx=5,pady=5,sticky=W)



    def save_config(self):
        d = {'path': self.path_var.get()}
        d['delete']=self.delete_var.get()
        return d

    def select_folder(self):
        d=filedialog.askdirectory()
        self.path_var.set(d)
        self.sframe.focus_force()




