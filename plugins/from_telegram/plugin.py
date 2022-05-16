from tkinter import *
from tkinter.ttk import *
from pathlib import Path
from tkinter import filedialog

class Plugin:
	def __init__(self):
		self.category='input'
		self.name=_('From Telegram Group')
		self.need_config=True


	def start_config(self,frame,plug):
		Label(frame,text=_('Key')).grid(row=0,column=0,padx=5,pady=5,sticky=W)
		self.key_var=StringVar()
		self.key_var.set(plug.settings.get('key',''))
		self.my=Entry(frame,width=30,textvariable=self.key_var)
		self.my.grid(row=0,column=1,padx=5,pady=5,sticky=E)

	

	def save_config(self):
		return {'key': self.key_var.get()}

	def select_folder(self):
		d=filedialog.askdirectory()
		self.path_var.set(d)
		self.sframe.focus_force()




