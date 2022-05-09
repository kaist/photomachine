from tkinter import *
from tkinter.ttk import *
from pathlib import Path
from tkinter import filedialog
from app.utils import *

class Plugin:
    def __init__(self):
        self.category='process'
        self.name=_('Rename')
        self.need_config=True


    def start_config(self,frame,plug):
        self.store=PluginStore(Path(plug.path).parts[-1])    
        Label(frame,text=_('Name Template')).grid(row=0,column=0,padx=5,pady=5,sticky=W)


        self.templ_var=StringVar()
        self.templ_var.set(plug.settings.get('templ','IMG_[COUNT]'))
        self.mx=Entry(frame,width=50,textvariable=self.templ_var)
        self.mx.grid(row=0,column=1,padx=5,columnspan=2,pady=5,sticky=W)


        Label(frame,text=_('Example')).grid(row=1,column=0,padx=5,pady=5,sticky=W)

        self.ex_var=StringVar()
        self.ex=Entry(frame,width=50,textvariable=self.ex_var,state=DISABLED)
        self.ex.grid(row=1,column=1,padx=5,columnspan=2,pady=5,sticky=W)


        self.digits_var=StringVar()
        self.digits_var.set(plug.settings.get('digits',4))
        Label(frame,text=_('Digits count')).grid(row=2,column=0,padx=5,pady=5,sticky=W)
        self.my=Entry(frame,width=7,textvariable=self.digits_var)
        self.my.grid(row=2,column=1,padx=5,pady=5,sticky=W)




        self.auto_var=BooleanVar()
        self.auto_var.set(plug.settings.get('autoclean',1))
        Checkbutton(frame, text=_("Set counter to zero at start"),variable=self.auto_var,onvalue=1,offvalue=0).grid(row=3,column=0,columnspan=2,padx=5,pady=5,sticky=W)
        try:
            counter=len(self.store.counter)
        except:
            self.store.counter=0
            counter=0
        self.clean_but=Button(frame,text=_('Set now')+f' ({counter})',command=self.clean_db)
        self.clean_but.grid(row=3,column=2,columnspan=1,padx=5,pady=5,sticky=W)


        self.time_var=IntVar()
        self.time_var.set(plug.settings.get('time',0))
        Radiobutton(frame, text=_("Date/Time from EXIF"),variable=self.time_var,value=0).grid(row=4,column=0,columnspan=3,padx=5,pady=5,sticky=W)
        Radiobutton(frame, text=_("Date/Time now"),variable=self.time_var,value=1).grid(row=5,column=0,columnspan=3,padx=5,pady=5,sticky=W) 


        Label(frame,text=_('Patterns:\n[COUNT] - counter\n[YEAR],[MONTH],[DAY] - date\n[HOUR],[MINUTE],[SECOND] - time')).grid(row=6,column=0,columnspan=3,padx=5,pady=5,sticky=W)
        self.templ_var.trace('w',self.upd_example)
        self.digits_var.trace('w',self.upd_example)
        self.upd_example()

    def upd_example(self,*args):
        patt=self.templ_var.get()
        digs=int(self.digits_var.get())
        c=str(self.store.counter).zfill(digs)
        patt=patt.replace('[COUNT]',c)
        patt=patt.replace('[YEAR]','2022')
        patt=patt.replace('[MONTH]','11')
        patt=patt.replace('[DAY]','05')    
        patt=patt.replace('[HOUR]','16')
        patt=patt.replace('[MINUTE]','47')
        patt=patt.replace('[SECOND]','01')             
        self.ex_var.set(patt)
        


    def clean_db(self):
        self.store.counter=0
        self.clean_but['text']=_('Set now')+' (0)'

        

    def save_config(self):
        d={}
        d['templ']=self.templ_var.get()
        d['digits']=int(self.digits_var.get())
        d['time']=int(self.time_var.get())
        d['autoclean']=int(self.auto_var.get())
        return d





