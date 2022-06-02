

class Plugin:
    def __init__(self):
        self.category='process'
        self.name=_('Filter by Camera/Lens')
        self.need_config=True


    def start_config(self,frame,plug):
        Label(frame,text=_('Approve if contain')).grid(row=0,column=0,padx=5,pady=5,sticky=W)

        self.contain_var=StringVar(value=plug.settings.get('contain','Canon'))
        Entry(frame,textvariable=self.contain_var,width=25).grid(row=0,column=1,padx=5,pady=5,sticky=W)

        Label(frame,text=_('See the help for the plugin for information.')).grid(row=1,column=0,columnspan=2,padx=5,pady=5,sticky=W)       






    def save_config(self):
        d = {'contain': self.contain_var.get()}
        return d





