

class Plugin:
    def __init__(self):
        self.category='process'
        self.name=_('Filter by Stars')
        self.need_config=True


    def start_config(self,frame,plug):
        Label(frame,text=_('Approve if')).grid(row=0,column=0,padx=5,pady=5,sticky=W)
        self.if_var=StringVar()
        ifs=[_('Rating more than'),_('Rating is'),_('Rating less than')]
        self.if_var.set(ifs[plug.settings.get('if',1)])
        self.if_combo=Combobox(frame,textvariable=self.if_var,state="readonly",width=20)
        self.if_combo.grid(row=0,column=1,columnspan=1,padx=5,pady=5,sticky=W)
        self.if_combo['values']=ifs

        self.rating_var=StringVar()
        rts=[_('Not set'),'★','★★','★★★','★★★★','★★★★★']
        self.rating_var.set(rts[plug.settings.get('rating',1)])
        self.rat_combo=Combobox(frame,textvariable=self.rating_var,state="readonly",width=15)
        self.rat_combo.grid(row=0,column=2,columnspan=1,padx=5,pady=5,sticky=W)
        self.rat_combo['values']=rts






    def save_config(self):
        d={}
        d['rating']=self.rat_combo.current()
        d['if']=self.if_combo.current()
        return d





