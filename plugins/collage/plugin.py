from tkinter import *
from tkinter.ttk import *
from pathlib import Path
from tkinter import filedialog
import time
from app.utils import *
import PIL
from PIL import ImageDraw,ImageFont




class Plugin:
    def __init__(self):
        self.category='process'
        self.name=_('Collage')
        self.need_config=True

    def force_int(self,varname,index,mode):
        var = getattr(self, f'{varname}_var')
        try:newval=int(var.get())
        except:
            try:newval=''.join(char for char in str(var.get()) if char.isdigit())
            except:return
        var.set(newval)
        if varname in ('hsize','vsize'):
            self.update_image()



    def start_config(self,frame,plug):
        self.cur_element=None

        self.cur_path=Path(plug.path)
        self.frame=frame
        self.elements=[]

        self.sframe=Frame(frame)
        self.sframe.pack(side=LEFT,fill=BOTH)

        sizef=Labelframe(self.sframe,text=_('Main image size'))
        sizef.pack(fill=X,padx=5,pady=5,side=TOP)
        self.hsize_var=IntVar(name='hsize')
        self.hsize_var.set(plug.settings.get('hsize',2480))
        Label(sizef,text=_('Width (px.)')).grid(row=0,column=0,padx=5,pady=5,sticky=E)
        Entry(sizef,textvariable=self.hsize_var,width=5).grid(row=0,column=1,padx=5,pady=5,sticky=W)
        self.hsize_var.trace('w',self.force_int)

        self.vsize_var=IntVar(name='vsize')
        self.vsize_var.set(plug.settings.get('vsize',3508))
        Label(sizef,text=_('Height (px.)')).grid(row=0,column=2,padx=5,pady=5,sticky=E)
        Entry(sizef,textvariable=self.vsize_var,width=5).grid(row=0,column=3,padx=5,pady=5,sticky=W)
        self.vsize_var.trace('w',self.force_int)

        itemsf=Labelframe(self.sframe,text=_('Elements'))
        itemsf.pack(fill=BOTH,padx=5,pady=5,side=TOP)

        bf=Frame(itemsf)
        bf.pack(side=TOP,fill=X)


        self.posx_var=IntVar(name='posx')
        self.posx_var.set(50)
        Label(bf,text=_('Pos. X')).grid(row=0,column=0,padx=5,pady=5,sticky=E)
        Entry(bf,textvariable=self.posx_var,width=5).grid(row=0,column=1,padx=5,pady=5,sticky=W)
        self.posx_var.trace('w',self.force_int)

        self.posy_var=IntVar(name='posy')
        self.posy_var.set(50)
        Label(bf,text=_('Pos. Y')).grid(row=0,column=2,padx=5,pady=5,sticky=E)
        Entry(bf,textvariable=self.posy_var,width=5).grid(row=0,column=3,padx=5,pady=5,sticky=W)
        self.posy_var.trace('w',self.force_int)


        self.sizex_var=IntVar(name='sizex')
        self.sizex_var.set(640)
        Label(bf,text=_('Width')).grid(row=1,column=0,padx=5,pady=5,sticky=E)
        Entry(bf,textvariable=self.sizex_var,width=5).grid(row=1,column=1,padx=5,pady=5,sticky=W)
        self.sizex_var.trace('w',self.force_int)


        self.sizey_var=IntVar(name='sizey')
        self.sizey_var.set(480)
        Label(bf,text=_('Width')).grid(row=1,column=2,padx=5,pady=5,sticky=E)
        Entry(bf,textvariable=self.sizey_var,width=5).grid(row=1,column=3,padx=5,pady=5,sticky=W)
        self.sizey_var.trace('w',self.force_int)

        self.contain_var=IntVar()
        self.contain_var.set(0)
        Radiobutton(bf, text=_("Fit image"),variable=self.contain_var,value=0).grid(row=2,column=0,columnspan=4,padx=5,pady=5,sticky=W)
        Radiobutton(bf, text=_("Cover image"),variable=self.contain_var,value=1).grid(row=3,column=0,columnspan=4,padx=5,pady=5,sticky=W)

        bbf=Frame(bf)
        bbf.grid(row=4,column=0,columnspan=4,sticky=EW)

        Button(bbf,text=_('Add'),command=self.add_element).pack(side=LEFT,padx=5,pady=5)

        self.save_but=Button(bbf,text=_('Save'),width=12,command=self.save_element)
        self.save_but.pack(side=LEFT,padx=5,pady=5)

        self.del_but=Button(bbf,text=_('Remove'),width=12,command=self.remove_element)
        self.del_but.pack(side=LEFT,padx=5,pady=5)



        lstframe=Frame(itemsf)
        lstframe.pack(side=BOTTOM,fill=BOTH,padx=5,pady=5)

        self.lst=Listbox(lstframe,width=45,activestyle="none")
        self.lst.pack(side=LEFT,fill=BOTH)
        self.lst.bind("<<ListboxSelect>>", self.select_element)

        scroll=Scrollbar(lstframe)
        scroll.pack(side = RIGHT, fill = BOTH)
        self.lst.config(yscrollcommand = scroll.set)

        tf=Label(self.sframe)
        tf.pack(fill=X)
        Label(tf,text=_('Timeout (sec.)')).grid(row=0,column=0,padx=5,pady=5,sticky=W)
        self.timeout_var=IntVar(name='timeout')
        self.timeout_var.set(plug.settings.get('timeout',30))
        Entry(tf,textvariable=self.timeout_var,width=5).grid(row=0,column=1,padx=5,pady=5,sticky=W)
        Label(tf,wraplength=300,text=_('This is the time in seconds that the plugin waits for the next image. If the time has passed, the plugin no longer waits for the next image and sends the incomplete layout.')).grid(row=1,column=0,columnspan=2,padx=5,pady=5,sticky=EW)
        self.timeout_var.trace('w',self.force_int)

        self.canvas=Canvas(self.frame,width=640,height=640)
        self.canvas.pack(side=RIGHT)

        if plug.settings.get('elements',None):
            self.elements=plug.settings['elements']
            self.update_list()
        self.update_image()


    def update_image(self):
        img=PIL.Image.new('RGB',(int(self.hsize_var.get()),int(self.vsize_var.get())),'white')
        draw = ImageDraw.Draw(img)
        for n,x in enumerate(self.elements):
            draw.rectangle((x['x'],x['y'],x['x']+x['sizex'],x['y']+x['sizey']),fill='grey')
            draw.text((x['x']+20,x['y']+20),text=f'#{n+1}',anchor='lt',fill='black',font=ImageFont.truetype("arial.ttf", 150))


        img.thumbnail((640,640))
        self.c_image=PIL.ImageTk.PhotoImage(image=img)
        dx=(640-img.size[0])/2
        dy=(640-img.size[1])/2
        self.canvas.create_image(dx,dy,image=self.c_image,tags=('image',),anchor=NW)


    def select_element(self,event):
        try:selection = event.widget.curselection()[0]
        except:return
        self.cur_element=selection
        el=self.elements[selection]
        self.posx_var.set(el['x'])
        self.posy_var.set(el['y'])
        self.sizex_var.set(el['sizex'])
        self.sizey_var.set(el['sizey'])
        self.contain_var.set(el['contain'])

        self.del_but['text']=_('Remove')+f' (#{selection+1})'
        self.save_but['text']=_('Save')+f' (#{selection+1})'

    def remove_element(self):

        try:
            del self.elements[self.cur_element]
        except:return
        self.cur_element=None
        self.update_list()

    def save_element(self):
        el = {'x': int(self.posx_var.get())}
        el['y']=int(self.posy_var.get())
        el['sizex']=int(self.sizex_var.get())
        el['sizey']=int(self.sizey_var.get())
        el['contain']=int(self.contain_var.get())
        try:
            self.elements[self.cur_element]=el
        except:pass

        self.update_list()

        try:self.lst.select_set(self.cur_element)
        except:pass

    def add_element(self):
        el = {'x': int(self.posx_var.get())}
        el['y']=int(self.posy_var.get())
        el['sizex']=int(self.sizex_var.get())
        el['sizey']=int(self.sizey_var.get())
        el['contain']=int(self.contain_var.get())
        self.elements.append(el)
        self.update_list()

    def update_list(self):
        self.lst.delete(0,END)
        for n,x in enumerate(self.elements):
            g = 'cover' if x['contain'] else 'fit'
            s=f'#{n+1:2}  Pos X:{x["x"]:4} Pos Y:{x["y"]:4} Size: {x["sizex"]:4}x{x["sizey"]:4} ({g})'
            self.lst.insert(END,s)
        self.del_but['text']=_('Remove')
        self.save_but['text']=_('Save')
        self.update_image()

    def save_config(self):
        d = {'hsize': self.hsize_var.get()}
        d['vsize']=self.vsize_var.get()
        d['elements']=self.elements
        d['timeout']=self.timeout_var.get()

        return d





