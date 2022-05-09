from tkinter import *
from tkinter.ttk import *
from pathlib import Path
from tkinter import filedialog

from app.utils import *
class Plugin:
	def __init__(self):
		self.category='process'
		self.name=_('LUT')
		self.need_config=True


	def force_int(self,varname,index,mode):
		var= getattr(self, varname+'_var')
		try:newval=int(var.get())
		except:
			newval=100
		var.set(newval)

	def start_config(self,frame,plug):
		self.cur_path=Path(plug.path)
		self.sframe=frame
		self.path_var=StringVar()
		self.path_entry=Entry(frame,state=DISABLED,textvariable=self.path_var,width=40)
		self.path_var.set(plug.settings.get('path',''))
		self.path_entry.grid(row=0,column=0,padx=5,pady=5)
		self.f_image=PhotoImage(file=str(self.cur_path/'folder.png'))
		Button(frame,text=_('LUT file (.cube)'),compound='left',image=self.f_image,command=self.select_lut).grid(row=0,column=1,padx=5,pady=5)

		f2=Frame(frame)
		f2.grid(row=1,column=0,columnspan=2,sticky=EW)

		Label(f2,text=_('Blending')).grid(row=0,column=0,padx=5,pady=5,sticky=W)
		self.blend_var=IntVar(name='blend')
		self.blend_var.set(plug.settings.get('blend',100))
		Scale(f2, orient=HORIZONTAL,variable=self.blend_var, length=300, from_=0, to=100).grid(row=0,column=1,padx=5,pady=5)
		Entry(f2,textvariable=self.blend_var,width=5).grid(row=0,column=2,padx=5,pady=5)
		self.blend_var.trace('w',self.force_int)


		

	def save_config(self):
		d={}
		d['path']=self.path_var.get()
		d['blend']=int(self.blend_var.get())

		return d

	def select_lut(self):
		d=filedialog.askopenfilename(defaultextension=".cube",filetypes=[(".cube files", ".cube")])
		self.path_var.set(d)
		self.sframe.focus_force()



