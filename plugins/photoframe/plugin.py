from tkinter import *
from tkinter.ttk import *
from pathlib import Path
from tkinter import filedialog
import time
from app.utils import *





class Plugin:
	def __init__(self):
		self.category='process'
		self.name=_('PhotoFrame')
		self.need_config=True


	def start_config(self,frame,plug):
		self.cur_path=Path(plug.path)
		self.sframe=frame
		self.hpath_var=StringVar()
		self.hpath_entry=Entry(frame,state=DISABLED,textvariable=self.hpath_var,width=40)
		self.hpath_var.set(plug.settings.get('hpath',''))
		self.hpath_entry.grid(row=0,column=0,padx=5,pady=5)
		self.f_image=PhotoImage(file=str(self.cur_path/'folder.png'))
		Button(frame,text=_('Horizontal frame'),compound='left',image=self.f_image,command=self.select_hfolder).grid(row=0,column=1,padx=5,pady=5,sticky=W)

		self.vpath_var=StringVar()
		self.vpath_entry=Entry(frame,state=DISABLED,textvariable=self.vpath_var,width=40)
		self.vpath_var.set(plug.settings.get('vpath',''))
		self.vpath_entry.grid(row=1,column=0,padx=5,pady=5)
		Button(frame,text=_('Vertical frame'),compound='left',image=self.f_image,command=self.select_vfolder).grid(row=1,column=1,padx=5,pady=5,sticky=W)


		Label(frame,wraplength=400,text=_('It is better to use separate frames for vertical or horizontal photos. But you can only use one photo frame for everyone.')).grid(row=2,column=0,columnspan=2,padx=5,pady=5,sticky=W)

		self.contain_var=IntVar()
		self.contain_var.set(plug.settings.get('contain',0))
		Radiobutton(frame, text=_("Fit the image into the frame size"),variable=self.contain_var,value=0).grid(row=3,column=0,columnspan=2,padx=5,pady=5,sticky=W)
		Radiobutton(frame, text=_("Fit a frame into an image"),variable=self.contain_var,value=1).grid(row=4,column=0,columnspan=2,padx=5,pady=5,sticky=W)

	def save_config(self):
		d = {'hpath': self.hpath_var.get()}
		d['vpath']=self.vpath_var.get()
		d['contain']=self.contain_var.get()
		return d

	def select_hfolder(self):
		d=filedialog.askopenfilename(defaultextension=".png",filetypes=[(".png images", ".png")])
		self.hpath_var.set(d)
		self.sframe.focus_force()

	def select_vfolder(self):
		d=filedialog.askopenfilename(defaultextension=".png",filetypes=[(".png images", ".png")])
		self.vpath_var.set(d)
		self.sframe.focus_force()



