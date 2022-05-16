from pathlib import Path
import PIL
from PIL import ImageTk
import time
import os
import sys
from app.utils import *
from pathlib import Path
from tkinter import *
from tkinter.ttk import *
import threading
import ctypes as ct


root=Tk()
root.title('Viewer')



def dark_title_bar(window):
    window.update()
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ct.windll.user32.GetParent
    hwnd = get_parent(window.winfo_id())
    rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
    value = 2
    value = ct.c_int(value)
    set_window_attribute(hwnd, rendering_policy, ct.byref(value),
                     ct.sizeof(value))

class Gui:

    def __init__(self,root,settings,self_q):
        self.fs=settings['fullscreen']
        root.bind('<Escape>', self.leave_fs)

        self.self_q=self_q
        self.root=root
        self.cur_folder=Path(__file__).parent
        self.settings=settings
        dark_title_bar(self.root)
        if self.fs:

            self.root.attributes("-fullscreen", True)


        self.root.tk.call('wm', 'iconphoto', self.root._w, PhotoImage(file=str(self.cur_folder/'icon.png')))
        self.root.state('zoomed')
        self.root.title('Viewer')
        scale=self.root.winfo_fpixels('1i')/72
        self.root.tk.call('tk', 'scaling', scale)

        self.root.configure(background='black')
        self.canvas=Canvas(self.root,bd=0, highlightthickness=0, relief='ridge')
        self.canvas.configure(bg='#121212')
        self.canvas.pack(fill=BOTH,expand=True)
        self.listener()

    def leave_fs(self,event=None):
        self.fs=False
        self.root.attributes("-fullscreen", False)
        self.root.update()
        dark_title_bar(self.root)

    def upd_img(self,image,vars):
        self.image=image
        self.image_vars=vars
        self.root.after(5,self.upd_now)

    def upd_now(self):
        self.canvas.delete('image')
        self.canvas.delete('text')
        x,y=self.canvas.winfo_width(),self.canvas.winfo_height()
        if not self.settings['split']:
            self.image.thumbnail((x,y),PIL.Image.ANTIALIAS)
            self.ph_image=PIL.ImageTk.PhotoImage(image=self.image)
            dx=(x-self.image.size[0])/2
            dy=(y-self.image.size[1])/2
            self.canvas.create_image(dx,dy,image=self.ph_image,tags=('image',),anchor=NW)
            self.canvas.create_text(10,10,text=str(Path(self.image_vars['filename']).name),font=(20,),anchor=NW,width=300,tags=('text',),fill='white')
        elif self.settings['left']:
            nx=int(x/2)
            self.image.thumbnail((nx,y),PIL.Image.ANTIALIAS)
            self.ph_image=PIL.ImageTk.PhotoImage(image=self.image)
            dx=(nx-self.image.size[0])/2
            dy=(y-self.image.size[1])/2
            self.canvas.create_image(dx+nx,dy,image=self.ph_image,tags=('image',),anchor=NW)

            self.image2=PIL.Image.open(self.image_vars['filename'])

            self.image2.thumbnail((nx,y),PIL.Image.ANTIALIAS)
            self.ph_image2=PIL.ImageTk.PhotoImage(image=self.image2)
            dx=(nx-self.image2.size[0])/2
            dy=(y-self.image2.size[1])/2
            self.canvas.create_image(dx,dy,image=self.ph_image2,tags=('image',),anchor=NW)

            self.canvas.create_text(10,10,text='Before: '+str(Path(self.image_vars['filename']).name),font=(20,),anchor=NW,width=300,tags=('text',),fill='white')
            self.canvas.create_text(10+nx,10,text='After: '+str(Path(self.image_vars['filename']).name),font=(20,),anchor=NW,width=300,tags=('text',),fill='white')
        else:
            ny=int(y/2)
            self.image.thumbnail((x,ny),PIL.Image.ANTIALIAS)
            self.ph_image=PIL.ImageTk.PhotoImage(image=self.image)
            dx=(x-self.image.size[0])/2
            dy=(ny-self.image.size[1])/2
            self.canvas.create_image(dx,dy+ny,image=self.ph_image,tags=('image',),anchor=NW)

            self.image2=PIL.Image.open(self.image_vars['filename'])

            self.image2.thumbnail((x,ny),PIL.Image.ANTIALIAS)
            self.ph_image2=PIL.ImageTk.PhotoImage(image=self.image2)
            dx=(x-self.image2.size[0])/2
            dy=(ny-self.image2.size[1])/2
            self.canvas.create_image(dx,dy,image=self.ph_image2,tags=('image',),anchor=NW)               

            self.canvas.create_text(10,10,text='Before: '+str(Path(self.image_vars['filename']).name),font=(20,),anchor=NW,width=300,tags=('text',),fill='white')
            self.canvas.create_text(10,10+ny,text='After: '+str(Path(self.image_vars['filename']).name),font=(20,),anchor=NW,width=300,tags=('text',),fill='white')
        self.canvas.tag_raise('text','image')
        sys.stdout.flush()
        #self.after['image']=self.ph_image

    def listener(self):
        if not self.self_q.empty():
            sys.stdout.flush()
            image,vars=self.self_q.get()
            self.upd_img(image,vars)
        self.root.after(50,self.listener)        
        





def run_in(gui,settings,self_q,message_q,self_id):
    if not self_q.empty():
        sys.stdout.flush()
        image,vars=self_q.get()
        gui.upd_img(image,vars)
        message_q.put([self_id,'Show:\n'+Path(vars['filename']).name])
    time.sleep(0.1)






def run(store,settings,message_q,output_q,self_id,self_q=None):
    gui=Gui(root,settings,self_q)
    #th=threading.Thread(target=run_in,args=(gui,settings,self_q,message_q,self_id))
    #th.start()
    root.mainloop()






    

