from tkinter import *
from tkinter.ttk import *
from app.utils import *

import json

class Plugin:
    def __init__(self):
        self.category='process'
        self.name=_('Photoshop actions')
        self.need_config=True

    def start_config(self,frame,plug):
        self.plug=plug
        self.cur_path=Path(plug.path)
        self.all_actions=[]
        Label(frame,text=_('Sets')).grid(row=0,column=0,padx=5,pady=5)
        self.sets_var=StringVar()
        self.sets_var.set(_('waiting photoshop'))
        self.sets_combo=Combobox(frame,textvariable=self.sets_var)
        self.sets_combo.grid(row=0,column=1,padx=5,pady=5)
        self.sets_combo.bind("<<ComboboxSelected>>", self.select_1_level)

        self.action_var=StringVar()
        self.action_var.set(_('waiting photoshop'))
        Label(frame,text=_('Action')).grid(row=1,column=0,padx=5,pady=5)
        self.action_combo=Combobox(frame,textvariable=self.action_var)
        self.action_combo.grid(row=1,column=1,padx=5,pady=5)

        frame.after(200,self.get_actions)

    def select_1_level(self,event):
        for x in self.all_actions:
            if self.sets_combo.get()==x['name']:
                self.action_combo['values']=x['actions']
                self.action_var.set(x['actions'][0])


    def get_actions(self,event=None):
        import photoshop.api as ps
        from photoshop import Session
        app = ps.Application()
        self.all_actions=json.loads(app.doJavaScript(open(self.cur_path/'get_actions.js').read()))
        first_level=[]
        for x in self.all_actions:
            first_level.append(x['name'])
        self.sets_combo['values']=first_level
        self.sets_var.set(first_level[0])
        self.select_1_level(event=None)

        if self.plug.settings:
            self.sets_var.set(self.plug.settings['sets'])
            self.action_var.set(self.plug.settings['action'])
        del app          

    def save_config(self):
        d={}
        d['sets']=self.sets_var.get()
        d['action']=self.action_var.get()
        return d

