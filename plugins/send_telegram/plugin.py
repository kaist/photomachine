from tkinter import *
from tkinter.ttk import *
from pathlib import Path
from tkinter import filedialog

class Plugin:
	def __init__(self):
		self.category='output'
		self.name=_('To Telegram Group')
		self.need_config=True


	def start_config(self,frame,plug):
		Label(frame,text=_('Key')).grid(row=0,column=0,padx=5,pady=5,sticky=W)
		self.key_var=StringVar()
		self.key_var.set(plug.settings.get('key',''))
		self.my=Entry(frame,width=30,textvariable=self.key_var)
		self.my.grid(row=0,column=1,padx=5,pady=5,sticky=E)

		Label(frame,text=_('Caption')).grid(row=1,column=0,padx=5,pady=5,sticky=W)
		self.caption_var=StringVar()
		self.caption_var.set(plug.settings.get('caption',''))
		self.capt=Entry(frame,width=30,textvariable=self.caption_var)
		self.capt.grid(row=1,column=1,padx=5,pady=5,sticky=E)	

		self.asdoc_var=BooleanVar()
		self.asdoc_var.set(plug.settings.get('asdoc',0))		
		Checkbutton(frame, text=_("Send as document"),variable=self.asdoc_var,onvalue=1,offvalue=0).grid(row=2,column=0,columnspan=2,padx=5,pady=5,sticky=W)	

	def save_config(self):
		d={}
		d['key']=self.key_var.get()
		d['caption']=self.caption_var.get()
		d['asdoc']=self.asdoc_var.get()
		return d

	def select_folder(self):
		d=filedialog.askdirectory()
		self.path_var.set(d)
		self.sframe.focus_force()




