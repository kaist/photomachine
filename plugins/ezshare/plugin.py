from tkinter import *
from tkinter.ttk import *
from pathlib import Path
from tkinter import filedialog
import time
from app.utils import *
import subprocess
import locale
import sys
import ctypes

class Plugin:
    def __init__(self):
        self.category='input'
        self.name=_('EzShare WiFi')
        self.need_config=True


    def start_config(self,frame,plug):
        self.plug=plug
        self.frame=frame
        self.store=PluginStore(Path(plug.path).parts[-1]) 
        enc=locale.getpreferredencoding()
        data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode(enc).split('\n')
        aps=[]
        for x in data:
            if ' : ' in x:
                aps.append(x.split(' : ')[1].replace('\n','').replace('\r',''))

        self.connect_var=BooleanVar()
        self.connect_var.set(plug.settings.get('connect',0))      
        Checkbutton(frame, text=_("Auto connect to ezShare WiFi"),variable=self.connect_var,onvalue=1,offvalue=0).grid(row=0,column=0,columnspan=1,padx=5,pady=5,sticky=W)

        self.ap_var=StringVar()
        self.ap_var.set(plug.settings.get('ap',aps[0]))
        self.ap_combo=Combobox(frame,textvariable=self.ap_var,state="readonly",width=30)
        self.ap_combo.grid(row=0,column=1,padx=5,pady=5,sticky=W)
        self.ap_combo['values']=aps

 

        self.disconnect_var=BooleanVar()
        self.disconnect_var.set(plug.settings.get('disconnect',0))      
        Checkbutton(frame, text=_("After downloading, connect to another WiFi"),variable=self.disconnect_var,onvalue=1,offvalue=0).grid(row=1,column=0,columnspan=1,padx=5,pady=5,sticky=W)

        self.dis_var=StringVar()
        self.dis_var.set(plug.settings.get('dis_ap',aps[0]))
        self.dis_combo=Combobox(frame,textvariable=self.dis_var,state="readonly",width=30)
        self.dis_combo.grid(row=1,column=1,padx=5,pady=5,sticky=W)
        self.dis_combo['values']=aps


        Label(frame,text=_('Pause between connections (seconds)')).grid(row=2,column=0,padx=5,pady=5,sticky=W)

        self.pause_var=StringVar()
        self.pause_var.set(plug.settings.get('pause',60))
        Entry(frame,width=10,textvariable=self.pause_var).grid(row=2,column=1,padx=5,pady=5,sticky=W)


        self.auto_var=BooleanVar()
        self.auto_var.set(plug.settings.get('autoclean',0))
        Checkbutton(frame, text=_("Clear database at startup"),variable=self.auto_var,onvalue=1,offvalue=0).grid(row=3,column=0,columnspan=1,padx=5,pady=5,sticky=W)
        try:
            lst=len(self.store.image_list)
        except:
            self.store.image_list=[]
            lst=0
        self.clean_but=Button(frame,text=_('Clear now')+f' ({lst})',command=self.clean_db)
        self.clean_but.grid(row=3,column=1,columnspan=1,padx=5,pady=5,sticky=W)


        Label(frame,wraplength=500,text=_("When connected to the ezShare Wi-Fi card, the browser opens a page with a gallery. Its annoying! You can temporarily disable this feature, but do not forget to turn it back on later so that there are no problems connecting to some WiFi networks")).grid(row=4,column=0,columnspan=2,padx=5,pady=5,sticky=W)
        Button(frame,text=_('Switch off'),command=self.run_adm).grid(row=5,column=0,padx=5,pady=20,sticky=E)

        Button(frame,text=_('Turn it back on'),command=self.run_adm_on).grid(row=5,column=1,padx=5,pady=20,sticky=W)

    def run_adm(self):
        p=Path(self.plug.path)/Path('off.bat')
        ctypes.windll.shell32.ShellExecuteW(None, "runas",str(p), " ", None, 1)
        self.frame.after(1000,self.focus)

    def run_adm_on(self):
        p=Path(self.plug.path)/Path('on.bat')
        ctypes.windll.shell32.ShellExecuteW(None, "runas",str(p), " ", None, 1)
        self.frame.after(1000,self.focus)

    def focus(self,event=None):
        self.frame.focus_force()


    def clean_db(self):
        self.store.image_list=[]
        self.clean_but['text']=_('Clear now')+' (0)'


    def save_config(self):
        d={}
        d['connect']=int(self.connect_var.get())
        d['ap']=self.ap_var.get()
        d['disconnect']=int(self.disconnect_var.get())
        d['dis_ap']=self.dis_var.get()
        d['pause']=int(self.pause_var.get())
        d['autoclean']=int(self.auto_var.get())
        return d






