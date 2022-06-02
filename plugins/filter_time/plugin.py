

class Plugin:
    def __init__(self):
        self.category='process'
        self.name=_('Filter by Time')
        self.need_config=True


    def start_config(self,frame,plug):
        Label(frame,text=_('Approve if shoot')).grid(row=0,column=0,padx=5,pady=5,sticky=W)

        self.if_var=StringVar()
        ifs=[_('more that'),_('less that')]
        self.if_var.set(ifs[plug.settings.get('if',1)])
        self.if_combo=Combobox(frame,textvariable=self.if_var,state="readonly",width=15)
        self.if_combo.grid(row=0,column=1,columnspan=1,padx=5,pady=5,sticky=W)
        self.if_combo['values']=ifs


        self.time_var=IntVar(value=plug.settings.get('time',1))
        Entry(frame,textvariable=self.time_var,width=5).grid(row=0,column=2,padx=5,pady=5,sticky=W)

        self.units_var=StringVar()
        units=[_('days'),_('hours'),_('minutes')]
        self.units_var.set(units[plug.settings.get('units',1)])
        self.units_combo=Combobox(frame,textvariable=self.units_var,state="readonly",width=15)
        self.units_combo.grid(row=0,column=3,columnspan=1,padx=5,pady=5,sticky=W)
        self.units_combo['values']=units





        Label(frame,text=_('ago')).grid(row=0,column=4,padx=5,pady=5,sticky=W)       






    def save_config(self):
        d = {'units': self.units_combo.current()}
        d['if']=self.if_combo.current()
        d['time']=self.time_var.get()
        print(d)
        return d





