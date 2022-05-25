from tkinter import *
from tkinter.ttk import *
from pathlib import Path
from tkinter import filedialog

from app.utils import *
class Plugin:
	def __init__(self):
		self.category='process'
		self.name=_('Copies')
		self.need_config=True
		
	def start_config(self,frame,plug):
		Label(frame,text=_('Number of copies')).grid(row=0,column=0,padx=5,pady=5)

		self.copyvar=IntVar(value=plug.settings.get('copies',2))

		Entry(frame,width=7,textvariable=self.copyvar).grid(row=0,column=1,padx=5,pady=5)




		

	def save_config(self):
		d = {'copies': int(self.copyvar.get())}
		return d





