

class Plugin:

	def __init__(self):
		self.category='input'
		self.name=_('PhotoBooth')
		self.need_config=True
		self.default_config={'fullscreen':False}


	def start_config(self,frame,plug):
		self.full_var=BooleanVar()
		self.full_var.set(plug.settings.get('fullscreen',0))
		Checkbutton(frame, text=_("Fullscreen (press ESC to exit)"),variable=self.full_var).grid(row=0,column=0,padx=5,pady=5,sticky=W)	



	def save_config(self):
		return {'fullscreen': self.full_var.get()}

			








