from tkinter import *
from tkinter.ttk import *
from pathlib import Path
from tkinter import filedialog

from app.utils import *
class Plugin:
	def __init__(self):
		self.category='process'
		self.name=_('Thumbnail')
		self.need_config=True



	def start_config(self,frame,plug):
		Label(frame,text=_('Max width (px.)')).grid(row=0,column=0,padx=5,pady=5)
		self.mxvar=StringVar()
		self.myvar=StringVar()
		self.mx=Entry(frame,width=7,textvariable=self.mxvar)
		self.mx.grid(row=0,column=1,padx=5,pady=5)

		Label(frame,text=_('Max height (px.)')).grid(row=1,column=0,padx=5,pady=5)
		self.my=Entry(frame,width=7,textvariable=self.myvar)
		self.my.grid(row=1,column=1,padx=5,pady=5)

		self.mxvar.set(plug.settings.get('width',1920))
		self.myvar.set(plug.settings.get('height',1920))


		

	def save_config(self):
		d = {'width': int(self.mxvar.get())}
		d['height']=int(self.myvar.get())
		return d





