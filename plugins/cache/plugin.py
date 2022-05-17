from app.utils import DATA_PATH
import shutil 

class Plugin:
    def __init__(self):
        self.category='process'
        self.name=_('Cache')
        self.need_config=True
        self.default_config={'autoclean':False}


    def start_config(self,frame,plug):
        self.store=PluginStore(Path(plug.path).parts[-1])
        self.auto_var=BooleanVar()
        self.auto_var.set(plug.settings.get('autoclean',0))
        Checkbutton(frame, text=_("Clear cache at startup"),variable=self.auto_var,onvalue=1,offvalue=0).grid(row=0,column=0,columnspan=1,padx=5,pady=5,sticky=W)
        try:
            lst=len(self.store.cache)
        except:
            self.store.cache=[]
            lst=0
        self.clean_but=Button(frame,text=_('Clear now')+f' ({lst})',command=self.clean_db)
        self.clean_but.grid(row=0,column=1,columnspan=1,padx=5,pady=5,sticky=W)

    def clean_db(self):
        path=DATA_PATH/Path('cache')
        try:
            shutil.rmtree(path)
        except:pass
        self.store.cache=[]


        self.clean_but['text']=_('Clear now')+' (0)'

    def save_config(self):
        return {'autoclean': self.auto_var.get()}





