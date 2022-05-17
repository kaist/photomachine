

class Plugin:

    def __init__(self):
        self.category='input'
        self.name=_('PhotoBooth')
        self.need_config=True


    def start_config(self,frame,plug):
        self.sframe=frame
        self.cur_path=Path(plug.path)
        self.full_var=BooleanVar()
        self.full_var.set(plug.settings.get('fullscreen',0))
        Checkbutton(frame, text=_("Fullscreen (press ESC to exit)"),variable=self.full_var).grid(row=0,column=0,columnspan=3,padx=5,pady=5,sticky=W)

        self.theme_var=IntVar()
        self.theme_var.set(plug.settings.get('external_theme',0))
        Radiobutton(frame, text=_("Use internal theme"),variable=self.theme_var,value=0).grid(row=1,column=0,columnspan=3,padx=5,pady=5,sticky=W)
        Radiobutton(frame, text=_("Use external theme"),variable=self.theme_var,value=1).grid(row=2,column=0,columnspan=3,padx=5,pady=5,sticky=W)

        Label(frame,text=_('Theme Folder')).grid(row=3,column=0,padx=5,pady=5,sticky=W)
        self.path_var=StringVar(value=plug.settings.get('theme_path',''))
        Entry(frame,state=DISABLED,textvariable=self.path_var,width=30).grid(row=3,column=1,padx=5,pady=5)
        self.f_image=PhotoImage(file=str(self.cur_path/'folder.png'))
        Button(frame,text=_('Select folder'),compound='left',image=self.f_image,command=self.select_folder).grid(row=3,column=2,padx=5,pady=5)

        Label(frame,text=_('Digicam server URL (see help)')).grid(row=4,column=0,padx=5,pady=5,sticky=W)
        self.url_var=StringVar(value=plug.settings.get('url','http://localhost:5513'))
        Entry(frame,textvariable=self.url_var,width=30).grid(row=4,columnspan=2,column=1,padx=5,pady=5,sticky=EW)

        Label(frame,text=_('Number of photos in the series')).grid(row=5,column=0,padx=5,pady=5,sticky=W)
        self.count_var=IntVar(value=plug.settings.get('count',1))
        Entry(frame,textvariable=self.count_var,width=10).grid(row=5,columnspan=2,column=1,padx=5,pady=5,sticky=W)

        Label(frame,text=_('Preview time (seconds)')).grid(row=6,column=0,padx=5,pady=5,sticky=W)
        self.timer_var=IntVar(value=plug.settings.get('timer',5))
        Entry(frame,textvariable=self.timer_var,width=10).grid(row=6,columnspan=2,column=1,padx=5,pady=5,sticky=W)


        self.confirm_var=BooleanVar(value=plug.settings.get('confirm',0))
        Checkbutton(frame, text=_("Enable confirmation from the user (dont forget about the photobooth confirmation plugin)"),variable=self.confirm_var,onvalue=1,offvalue=0).grid(row=7,column=0,columnspan=3,padx=5,pady=5,sticky=W)

    def save_config(self):
        return {
            'fullscreen': self.full_var.get(),
            'external_theme':self.theme_var.get(),
            'theme_path':self.path_var.get(),
            'url':self.url_var.get(),
            'count':self.count_var.get(),
            'timer':self.timer_var.get(),
            'confirm':self.confirm_var.get()
            
            
            }


    def select_folder(self):
        d=filedialog.askdirectory()
        self.path_var.set(d)
        self.sframe.focus_force()

            








