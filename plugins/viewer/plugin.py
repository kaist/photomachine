

class Plugin:

	def __init__(self):
		self.category='output'
		self.name=_('Viewer')
		self.need_config=True
		self.default_config={'fullscreen':False,'split':False,'left':1}


	def start_config(self,frame,plug):
		self.full_var=BooleanVar()
		self.full_var.set(plug.settings.get('fullscreen',0))
		Checkbutton(frame, text=_("Fullscreen (press ESC to exit)"),variable=self.full_var).grid(row=0,column=0,padx=5,pady=5,sticky=W)	

		self.split_var=BooleanVar()
		self.split_var.set(plug.settings.get('split',0))
		Checkbutton(frame, text=_("Before and after split view"),variable=self.split_var).grid(row=1,column=0,padx=5,pady=5,sticky=W)
		Label(frame,text=_("WARNING! Don't use rename actions before this feature works.")).grid(row=2,column=0,padx=5,pady=5,sticky=W)
		bb=Frame(frame)
		bb.grid(row=3,column=0)
		self.left_var=IntVar()
		self.left_var.set(plug.settings.get('left',1))
		Radiobutton(bb, text=_("Left/Right view"),variable=self.left_var,value=1).pack(side=LEFT,padx=5,pady=5)
		Radiobutton(bb, text=_("Top/Bottom"),variable=self.left_var,value=0).pack(side=LEFT,padx=5,pady=5)	

	def save_config(self):
		d={}
		d['fullscreen']=self.full_var.get()
		d['split']=self.split_var.get()
		d['left']=self.left_var.get()
		return d

			








