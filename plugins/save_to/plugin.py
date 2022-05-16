from tkinter import *
from tkinter.ttk import *
from pathlib import Path
from tkinter import filedialog

class Plugin:
    def __init__(self):
        self.category='output'
        self.name=_('Save to disk')
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

        Label(frame,text=_('Format')).grid(row=1,column=0,padx=5,pady=5,sticky=E)
        self.format_var=StringVar()
        formats=['jpg','png','tiff','bmp','gif','pdf']
        self.format_var.set(plug.settings.get('format','jpg'))
        self.format_combo=Combobox(frame,textvariable=self.format_var,state="readonly",width=10)
        self.format_combo.grid(row=1,column=1,columnspan=1,padx=5,pady=5,sticky=W)
        self.format_combo['values']=formats 

    def save_config(self):
        d = {'path': self.path_var.get()}
        d['format']=self.format_var.get()
        return d

    def select_folder(self):
        d=filedialog.askdirectory()
        self.path_var.set(d)
        self.sframe.focus_force()




