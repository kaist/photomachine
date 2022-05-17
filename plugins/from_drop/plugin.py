

class Plugin:

    def __init__(self):
        self.category='input'
        self.name=_('Drop Window')
        self.need_config=True
        self.default_config={'matadata':False,'remember':False,'autoclean':True,'delete':False}


    def start_config(self,frame,plug):
        self.store=PluginStore(Path(plug.path).parts[-1])        
        self.cur_path=Path(plug.path)
        self.sframe=frame
        self.metadata_var=BooleanVar()
        self.metadata_var.set(plug.settings.get('metadata',0))      
        Checkbutton(frame, text=_("Dont load image (just metadata)"),variable=self.metadata_var,onvalue=1,offvalue=0).grid(row=2,column=0,columnspan=2,padx=5,pady=5,sticky=W)

        Label(frame,text=_('(If this is installed, dont forget to add the "Load Source Image" plugin before actions that modify or save the image.)'),wraplength=400).grid(row=3,column=0,columnspan=2,padx=5,pady=5,sticky=W)


        self.remember_var=IntVar()
        self.remember_var.set(plug.settings.get('remember',0))
        Checkbutton(frame, text=_("Do not open photos that have already been processed before."),variable=self.remember_var).grid(row=4,column=0,columnspan=2,padx=5,pady=5,sticky=W)

        self.auto_var=BooleanVar()
        self.auto_var.set(plug.settings.get('autoclean',1))
        Checkbutton(frame, text=_("Clear database at startup"),variable=self.auto_var,onvalue=1,offvalue=0).grid(row=5,column=0,columnspan=1,padx=5,pady=5,sticky=W)
        try:
            lst=len(self.store.image_list)
        except:
            self.store.image_list=[]
            lst=0
        self.clean_but=Button(frame,text=_('Clear now')+f' ({lst})',command=self.clean_db)
        self.clean_but.grid(row=5,column=1,columnspan=1,padx=5,pady=5,sticky=W)


        self.delete_var=BooleanVar()
        self.delete_var.set(plug.settings.get('delete',0))
        rc=Checkbutton(frame, text=_("Delete the original")+(' (!!!)'),variable=self.delete_var,onvalue=1,offvalue=0)
        rc.grid(row=8,column=0,columnspan=2,padx=5,pady=5,sticky=W)       


    def clean_db(self):
        self.store.image_list=[]
        self.clean_but['text']=_('Clear now')+' (0)'

    def save_config(self):
        d = {}
        d['metadata']=int(self.metadata_var.get())
        d['remember']=int(self.remember_var.get())
        d['autoclean']=int(self.auto_var.get())
        d['delete']=int(self.delete_var.get())
        return d

            








