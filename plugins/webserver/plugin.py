from tkinter import *
from tkinter.ttk import *
from pathlib import Path
from tkinter import filedialog
import time
from app.utils import *
import shutil
from netifaces import interfaces, ifaddresses, AF_INET




class Plugin:
    def __init__(self):
        self.category='output'
        self.name=_('Web server')
        self.need_config=True


    def start_config(self,frame,plug):
        self.ifaces=[]
        for ifaceName in interfaces():
            addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':None}] )]
            self.ifaces.extend(y for y in addresses if y)
        print(self.ifaces)


        self.store=PluginStore(Path(plug.path).parts[-1])
        self.cur_path=Path(plug.path)
        self.sframe=frame
        p=self.cur_path/Path('themes')
        self.int_themes=[]
        th=p.glob('*')
        self.int_themes.extend(x.parts[-1] for x in th)
        self.external_var=IntVar()
        self.external_var.set(plug.settings.get('external',0))
        Radiobutton(frame, text=_("Built-in themes"),variable=self.external_var,value=0).grid(row=0,column=0,columnspan=1,padx=5,pady=5,sticky=W)


        self.theme_var=StringVar()
        self.theme_var.set(plug.settings.get('theme',self.int_themes[0]))
        self.theme_combo=Combobox(frame,textvariable=self.theme_var,state="readonly",width=30)
        self.theme_combo.grid(row=0,column=1,columnspan=2,padx=5,pady=5,sticky=W)
        self.theme_combo['values']=self.int_themes


        Radiobutton(frame, text=_("Other theme (see help)"),variable=self.external_var,value=1).grid(row=1,column=0,columnspan=1,padx=5,pady=5,sticky=W)

        self.path_var=StringVar()
        self.path_entry=Entry(frame,state=DISABLED,textvariable=self.path_var,width=40)
        self.path_var.set(plug.settings.get('path',''))
        self.path_entry.grid(row=1,column=1,padx=5,pady=5)
        self.f_image=PhotoImage(file=str(self.cur_path/'folder.png'))
        Button(frame,text=_('Select folder'),compound='left',image=self.f_image,command=self.select_folder).grid(row=1,column=2,padx=5,pady=5)






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


        Label(frame,text=_('Server Port')).grid(row=4,column=0,padx=5,pady=5,sticky=E)

        self.port_var=IntVar(name='port')
        Entry(frame,textvariable=self.port_var,width=6).grid(row=4,column=1,columnspan=2,padx=5,pady=5,sticky=W)
        self.port_var.set(plug.settings.get('port',8080))
        self.port_var.trace('w',self.force_int)


        self.info_var=StringVar()
        self.info_var.set('...')
        Label(frame,textvariable=self.info_var).grid(row=5,column=0,columnspan=3,padx=5,pady=5,sticky=EW)


        Label(frame,text=_('Text at top')).grid(row=6,column=0,padx=5,pady=5,sticky=E)
        self.text_var=StringVar(value=plug.settings.get('text',''))
        Entry(frame,textvariable=self.text_var,width=60).grid(row=6,column=1,columnspan=2,padx=5,pady=5,sticky=W)

        Label(frame,text=_('Logo')).grid(row=7,column=0,padx=5,pady=5,sticky=E)
        self.logo_var=StringVar()
        self.logo_entry=Entry(frame,state=DISABLED,textvariable=self.logo_var,width=40)
        self.logo_var.set(plug.settings.get('logo',''))
        self.logo_entry.grid(row=7,column=1,padx=5,pady=5)
        Button(frame,text=_('Select image'),compound='left',image=self.f_image,command=self.select_logo).grid(row=7,column=2,padx=5,pady=5)


        Label(frame,text=_('or a link to site')+'\n'+_('(a qr code will be generated)')).grid(row=8,column=0,padx=5,pady=5,sticky=E)
        self.link_var=StringVar(value=plug.settings.get('link',''))
        Entry(frame,textvariable=self.link_var,width=50).grid(row=8,column=1,columnspan=2,padx=5,pady=5,sticky=W)

        Label(frame,text=_('Background')).grid(row=9,column=0,padx=5,pady=5,sticky=E)
        self.bg_var=StringVar()
        self.bg_entry=Entry(frame,state=DISABLED,textvariable=self.bg_var,width=40)
        self.bg_var.set(plug.settings.get('bg',''))
        self.bg_entry.grid(row=9,column=1,padx=5,pady=5)
        Button(frame,text=_('Select image'),compound='left',image=self.f_image,command=self.select_bg).grid(row=9,column=2,padx=5,pady=5)

        self.upd_label()




    def force_int(self,varname,index,mode):
        var = getattr(self, f'{varname}_var')
        try:newval=int(var.get())
        except:
            newval=8080
        var.set(newval)
        self.upd_label()

    def upd_label(self):
        ips = [f'http://{x}:{self.port_var.get()}' for x in self.ifaces]
        self.info_var.set(_('After the start, the server will be available at addresses')+':\n\n'+'\n'.join(ips))


    def clean_db(self):
        self.store.image_list=[]
        try:
            shutil.rmtree(DATA_PATH/Path('webserver'))
        except:pass

        self.clean_but['text']=_('Clear now')+' (0)'

    def save_config(self):
        d = {'path': self.path_var.get()}
        d['autoclean']=int(self.auto_var.get())
        d['theme']=self.theme_var.get()
        d['external']=int(self.external_var.get())
        d['port']=int(self.port_var.get())
        d['text']=self.text_var.get()
        d['logo']=self.logo_var.get()
        d['link']=self.link_var.get()
        d['bg']=self.bg_var.get()
        return d

    def select_folder(self):
        d=filedialog.askdirectory()
        self.path_var.set(d)
        self.sframe.focus_force()


    def select_logo(self):
        d=filedialog.askopenfilename(filetypes=(('images','.jpg .png'),))
        self.logo_var.set(d)
        self.sframe.focus_force()

    def select_bg(self):
        d=filedialog.askopenfilename(filetypes=(('images','.jpg .png'),))
        self.bg_var.set(d)
        self.sframe.focus_force()