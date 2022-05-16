from tkinter import *
from tkinter.ttk import *
from pathlib import Path
from tkinter import filedialog
import PIL
from PIL import ImageEnhance
from app.utils import *
class Plugin:
	def __init__(self):
		self.category='process'
		self.name=_('Watermark')
		self.need_config=True


	def force_int(self,varname,index,mode):
		var = getattr(self, f'{varname}_var')
		try:newval=int(var.get())
		except:
			newval=100
		var.set(newval)
		self.redraw_watermark()

	def start_config(self,frame,plug):
		self.sframe=frame
		self.cur_anchor=plug.settings.get('anchor','2:2')
		self.cur_path=Path(plug.path)
		self.path_var=StringVar()
		self.path_entry=Entry(frame,state=DISABLED,textvariable=self.path_var,width=40)
		self.path_var.set(plug.settings.get('path',''))
		self.path_entry.grid(row=0,column=0,padx=5,pady=5,sticky=EW)		
		self.f_image=PhotoImage(file=str(self.cur_path/'folder.png'))
		Button(frame,text=_('Watermark Image (.png)'),compound='left',image=self.f_image,command=self.select_png).grid(row=0,column=1,padx=5,pady=5,sticky=W)


		sl=Frame(frame)
		sl.grid(row=1,column=0,columnspan=2,padx=5,pady=5,sticky=EW)

		sf=Labelframe(sl,text=_('Anchor'))
		sf.pack(side=LEFT,padx=5,pady=5,fill=BOTH,ipady=5)
		s=Style()
		s.configure('my.TButton', font=('bold'))
		Button(sf,text='↖',width=1,command=lambda:self.set_a(0,0)).grid(row=0,column=0,padx=2,pady=2)
		Button(sf,text='↑',width=1,command=lambda:self.set_a(1,0)).grid(row=0,column=1,padx=2,pady=2)
		Button(sf,text='↗',width=1,command=lambda:self.set_a(2,0)).grid(row=0,column=2,padx=2,pady=2)
		Button(sf,text='←',width=1,command=lambda:self.set_a(0,1)).grid(row=1,column=0,padx=2,pady=2)
				
		Button(sf,text='→',width=1,command=lambda:self.set_a(2,1)).grid(row=1,column=2,padx=2,pady=2)
		Button(sf,text='↙',width=1,command=lambda:self.set_a(0,2)).grid(row=2,column=0,padx=2,pady=2)
		Button(sf,text='↓',width=1,command=lambda:self.set_a(1,2)).grid(row=2,column=1,padx=2,pady=2)					
		Button(sf,text='↘',width=1,command=lambda:self.set_a(2,2)).grid(row=2,column=2,padx=2,pady=2)	

		ss=Labelframe(sl,text=_('Settings'))
		ss.pack(side=LEFT,fill=BOTH,padx=5,pady=5)

		Label(ss,text=_('Size')).grid(row=0,column=0,padx=5,pady=5,sticky=W)
		self.size_var=IntVar(name='size')
		self.size_var.set(plug.settings.get('size',10))
		Scale(ss, orient=HORIZONTAL,variable=self.size_var, length=300, from_=0, to=100,value=1).grid(row=0,column=1,padx=5,pady=5)
		Entry(ss,textvariable=self.size_var,width=5).grid(row=0,column=2,padx=5,pady=5)
		self.size_var.trace('w',self.force_int)

		Label(ss,text=_('Indent')).grid(row=1,column=0,padx=5,pady=5,sticky=W)
		self.indent_var=IntVar(name='indent')
		self.indent_var.set(plug.settings.get('indent',0))
		Scale(ss, orient=HORIZONTAL,variable=self.indent_var, length=300, from_=0, to=50,value=1).grid(row=1,column=1,padx=5,pady=5)
		Entry(ss,textvariable=self.indent_var,width=5).grid(row=1,column=2,padx=5,pady=5)
		self.indent_var.trace('w',self.force_int)

		Label(ss,text=_('Opacity')).grid(row=2,column=0,padx=5,pady=5,sticky=W)
		self.opacity_var=IntVar(name='opacity')
		self.opacity_var.set(plug.settings.get('opacity',100))
		Scale(ss, orient=HORIZONTAL,variable=self.opacity_var, length=300, from_=0, to=100,value=1).grid(row=2,column=1,padx=5,pady=5)
		Entry(ss,textvariable=self.opacity_var,width=5).grid(row=2,column=2,padx=5,pady=5)
		self.opacity_var.trace('w',self.force_int)	

		self.canv=Canvas(frame,width=640,height=480)
		self.canv.configure(bg='grey')
		self.canv.grid(row=2,column=0,columnspan=2,padx=5,pady=5)
		self.example=PIL.Image.open(str(self.cur_path/'example.jpg')).convert('RGBA')
		if self.path_var.get():
			self.cur_image=PIL.Image.open(self.path_var.get())
			self.redraw_watermark()

	def set_a(self,h,v):
		self.cur_anchor=f'{h}:{v}'
		self.redraw_watermark()
	
	def redraw_watermark(self):


		nsize=min(self.example.size)*int(self.size_var.get())/100
		c=self.cur_image.copy()
		c.thumbnail((nsize,nsize))
		pod =self.example.copy()
		alpha=c.split()[-1]
		a=ImageEnhance.Brightness(alpha).enhance(int(self.opacity_var.get())/100.0)
		c.putalpha(a)

		v=self.cur_anchor.split(':')
		vx,vy=int(v[0]),int(v[1])
		ws=c.size
		os=pod.size

		indent=min(self.example.size)*int(self.indent_var.get())/100.0
		if vx==0:
			x=indent
		elif vx==2:
			x=os[0]-ws[0]-indent
		elif vx==1:
			x=os[0]/2-ws[0]/2
		if vy==0:
			y=indent
		elif vy==2:
			y=os[1]-ws[1]-indent
		elif vy==1:
			y=os[1]/2-ws[1]/2			




		pod.paste(c,(int(x),int(y)),c)
		self.pi=PIL.ImageTk.PhotoImage(pod)
		self.canv.create_image(0,0,image=self.pi,anchor='nw')


	def save_config(self):
		d = {'path': self.path_var.get()}
		d['size']=self.size_var.get()
		d['indent']=self.indent_var.get()
		d['opacity']=self.opacity_var.get()
		d['anchor']=self.cur_anchor
		return d

	def select_png(self):
		d=filedialog.askopenfilename(defaultextension=".png",filetypes=[(".png images", ".png")])
		self.path_var.set(d)
		self.sframe.focus_force()
		self.cur_image=PIL.Image.open(d)
		self.redraw_watermark()



