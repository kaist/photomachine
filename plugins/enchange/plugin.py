from tkinter import *
from tkinter.ttk import *
from pathlib import Path
from tkinter import filedialog

from app.utils import *
class Plugin:
	def __init__(self):
		self.category='process'
		self.name=_('Image Settings')
		self.need_config=True



	def force_int(self,varname,index,mode):
		var = getattr(self, f'{varname}_var')
		try:newval=int(var.get())
		except:
			newval=100
		var.set(newval)

	def force_float(self,varname,index,mode):
		var = getattr(self, f'{varname}_var')
		try:newval=round(float(var.get()),1)
		except:
			newval=1
		var.set(newval)


	def start_config(self,frame,plug):
		self.frame=frame
		Label(frame,text=_('Saturation')).grid(row=0,column=0,padx=5,pady=5,sticky=W)
		self.color_var=IntVar(name='color')
		self.color_var.set(plug.settings.get('color',0))
		self.color_scale=Scale(frame, orient=HORIZONTAL,variable=self.color_var, length=300, from_=-100, to=100,value=1).grid(row=0,column=1,padx=5,pady=5)
		Entry(frame,textvariable=self.color_var,width=5).grid(row=0,column=2,padx=5,pady=5)
		self.color_var.trace('w',self.force_int)


		Label(frame,text=_('Contrast')).grid(row=1,column=0,padx=5,pady=5,sticky=W)
		self.contrast_var=IntVar(name='contrast')
		self.contrast_var.set(plug.settings.get('contrast',0))
		Scale(frame, orient=HORIZONTAL,variable=self.contrast_var, length=300, from_=-100, to=100,value=1).grid(row=1,column=1,padx=5,pady=5)
		Entry(frame,textvariable=self.contrast_var,width=5).grid(row=1,column=2,padx=5,pady=5)
		self.contrast_var.trace('w',self.force_int)


		Label(frame,text=_('Brightness')).grid(row=2,column=0,padx=5,pady=5,sticky=W)
		self.brightness_var=IntVar(name='brightness')
		self.brightness_var.set(plug.settings.get('brightness',0))
		Scale(frame, orient=HORIZONTAL,variable=self.brightness_var, length=300, from_=-100, to=100,value=1).grid(row=2,column=1,padx=5,pady=5)
		Entry(frame,textvariable=self.brightness_var,width=5).grid(row=2,column=2,padx=5,pady=5)
		self.brightness_var.trace('w',self.force_int)

		Label(frame,text=_('Sharpness')).grid(row=3,column=0,padx=5,pady=5,sticky=W)
		self.sharpness_var=IntVar(name='sharpness')
		self.sharpness_var.set(plug.settings.get('sharpness',0))
		Scale(frame, orient=HORIZONTAL,variable=self.sharpness_var, length=300, from_=-100, to=100,value=1).grid(row=3,column=1,padx=5,pady=5)
		Entry(frame,textvariable=self.sharpness_var,width=5).grid(row=3,column=2,padx=5,pady=5)
		self.sharpness_var.trace('w',self.force_int)

		unsh_frame=Labelframe(frame,text=_('Unsharp mask'))
		unsh_frame.grid(row=4,column=0,columnspan=3,padx=5,pady=5,sticky=EW)

		self.enable_unsharp_var=BooleanVar()
		self.enable_unsharp_var.set(plug.settings.get('enable_unsharp',0))		
		Checkbutton(unsh_frame, text=_("Enable unsharp mask"),variable=self.enable_unsharp_var,onvalue=1,offvalue=0).grid(row=0,column=0,columnspan=3,padx=5,pady=5,sticky=W)

		Label(unsh_frame,text=_('Radius')).grid(row=1,column=0,padx=5,pady=5,sticky=W)
		self.radius_var=IntVar(name='radius')
		self.radius_var.set(plug.settings.get('radius',3))
		Scale(unsh_frame, orient=HORIZONTAL,variable=self.radius_var, length=300, from_=0, to=20,value=1).grid(row=1,column=1,padx=5,pady=5)
		Entry(unsh_frame,textvariable=self.radius_var,width=5).grid(row=1,column=2,padx=5,pady=5)
		self.radius_var.trace('w',self.force_int)	


		Label(unsh_frame,text=_('Percent')).grid(row=2,column=0,padx=5,pady=5,sticky=W)
		self.percent_var=IntVar(name='percent')
		self.percent_var.set(plug.settings.get('percent',100))
		Scale(unsh_frame, orient=HORIZONTAL,variable=self.percent_var, length=300, from_=0, to=200,value=1).grid(row=2,column=1,padx=5,pady=5)
		Entry(unsh_frame,textvariable=self.percent_var,width=5).grid(row=2,column=2,padx=5,pady=5)
		self.percent_var.trace('w',self.force_int)	



		Label(unsh_frame,text=_('Threshold')).grid(row=3,column=0,padx=5,pady=5,sticky=W)
		self.threshold_var=IntVar(name='threshold')
		self.threshold_var.set(plug.settings.get('threshold',5))
		Scale(unsh_frame, orient=HORIZONTAL,variable=self.threshold_var, length=300, from_=0, to=20,value=1).grid(row=3,column=1,padx=5,pady=5)
		Entry(unsh_frame,textvariable=self.threshold_var,width=5).grid(row=3,column=2,padx=5,pady=5)
		self.threshold_var.trace('w',self.force_int)	

	def save_config(self):
		return {
		    name: getattr(self, f'{name}_var').get()
		    for name in [
		        'color',
		        'contrast',
		        'brightness',
		        'sharpness',
		        'enable_unsharp',
		        'radius',
		        'percent',
		        'threshold',
		    ]
		}





