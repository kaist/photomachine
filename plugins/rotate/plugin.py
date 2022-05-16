

class Plugin:
    def __init__(self):
        self.category='process'
        self.name=_('Rotate/Flip')
        self.need_config=True


    def start_config(self,frame,plug):
        self.need_rotate=BooleanVar()
        self.need_rotate.set(plug.settings.get('need_rotate',0))
        Checkbutton(frame,text=_('Rotate'),variable=self.need_rotate).grid(row=0,column=0,padx=5,pady=5,sticky=W)
        self.if_var=StringVar()
        ifs=[_('Any'),_('Vertical only'),_('Horizontal only')]
        self.if_var.set(ifs[plug.settings.get('if',0)])
        self.if_combo=Combobox(frame,textvariable=self.if_var,state="readonly",width=20)
        self.if_combo.grid(row=0,column=1,columnspan=1,padx=5,pady=5,sticky=W)
        self.if_combo['values']=ifs

        self.rotate_var=StringVar()
        rts=[_('90° (clockwise)'),_('-90° (counterclockwise)'),'180°']
        self.rotate_var.set(rts[plug.settings.get('rotate',0)])
        self.rat_combo=Combobox(frame,textvariable=self.rotate_var,state="readonly",width=25)
        self.rat_combo.grid(row=0,column=2,columnspan=1,padx=5,pady=5,sticky=W)
        self.rat_combo['values']=rts


        self.flip_h_var=BooleanVar()
        self.flip_h_var.set(plug.settings.get('flip_h',0))
        Checkbutton(frame,text=_('Flip horizontally'),variable=self.flip_h_var).grid(row=1,column=0,columnspan=3,padx=5,pady=5,sticky=W)



        self.flip_v_var=BooleanVar()
        self.flip_v_var.set(plug.settings.get('flip_v',0))
        Checkbutton(frame,text=_('Flip vertically'),variable=self.flip_v_var).grid(row=2,column=0,columnspan=3,padx=5,pady=5,sticky=W)





    def save_config(self):
        d = {'rotate': int(self.rat_combo.current())}
        d['need_rotate']=self.need_rotate.get()
        d['if']=int(self.if_combo.current())
        d['flip_h']=self.flip_h_var.get()
        d['flip_v']=self.flip_v_var.get()

        return d





