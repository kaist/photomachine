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
import requests
import threading
import lxml.html


root=Tk()
root.title('Photobooth')



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

    def __init__(self,root,settings,self_q,output_q):
        self.self_q=self_q
        self.output_q=output_q
        self.digicam_list=[]
        self.download_list=[]
        root.attributes("-topmost",True)
        self.digicam_url=settings['url']
        self.root_path=Path(settings['theme_path']) if settings['external_theme'] else Path('plugins/photobooth/theme/')
        self.background_img=PhotoImage(file=self.root_path/'background.png')
        self.approve_img=PhotoImage(file=self.root_path/'approve.png')
        self.fs=settings['fullscreen']
        self.live_timer=settings['timer']
        self.img_count=settings['count']
        self.confirm_waiter=settings['confirm']
        








        root.bind('<Escape>', self.leave_fs)
        root.bind('<>')
        self.self_q=self_q
        self.root=root
        self.cur_folder=Path(__file__).parent
        self.settings=settings
        dark_title_bar(self.root)
        if self.fs:
            self.root.attributes("-fullscreen", True)
        self.root.tk.call('wm', 'iconphoto', self.root._w, PhotoImage(file=str(self.cur_folder/'icon.png')))
        self.root.state('zoomed')
        self.root.title('PhotoBooth')
        scale=self.root.winfo_fpixels('1i')/72
        self.root.tk.call('tk', 'scaling', scale)
        self.root.configure(background='black')
        self.canvas=Canvas(self.root,bd=0, highlightthickness=0, relief='ridge')
        self.canvas.configure(bg='#121212')
        self.canvas.pack(fill=BOTH,expand=True)

        self.root.after(100,self.init_start)

        self.root.after(1,self.parse_img_list)






    def leave_fs(self,event=None):
        self.fs=False
        self.root.attributes("-fullscreen", False)
        self.root.update()
        dark_title_bar(self.root)

    def upd_img(self,image,vars):
        self.image=image
        self.image_vars=vars
        self.root.after(5,self.upd_now)




    def init_start(self,event=None):
        self.download_list=[]
        self.canvas.delete('image')
        img=PIL.Image.open(self.root_path/Path('start.jpg'))
        x,y=self.canvas.winfo_width(),self.canvas.winfo_height()
        img=PIL.ImageOps.fit(img,(x,y))
        self.start_img=PIL.ImageTk.PhotoImage(image=img)
        self.canvas.create_image(0,0,image=self.start_img,tags=('image',),anchor=NW)
        self.canvas.tag_bind('image','<Button-1>', self.start_booth)


    def start_booth(self,event=None):
        if event and event.y < self.canvas.winfo_height() / 2:
            return
        self.canvas.tag_unbind('image', '<Button-1>')
        sys.stdout.flush()
        resp = requests.get(f'{self.digicam_url}/liveview.html?CMD=LiveViewWnd_Show')
        self.x,self.y=self.canvas.winfo_width(),self.canvas.winfo_height()


        th=threading.Thread(target=self.cam_stream)
        th.start()

    def upd_live_img(self,event=None):
        self.start_img=PIL.ImageTk.PhotoImage(image=self.live_img)
        self.canvas.create_image(0,0,image=self.start_img,tags=('image',),anchor=NW)
        text=(self.live_timer-int(time.time()-self.cur_time))
        self.canvas.create_text(10,10,text=str(text),font=(120,),anchor=NW,width=300,tags=('image',),fill='white')

    def cam_stream(self,event=None):
        self.cur_time=time.time()
        count=0

        while True:
            r = requests.get(
                f'{self.digicam_url}/liveview.jpg?rand={str(time.time())}',
                stream=True,
            )


            try:img=PIL.Image.open(r.raw)
            except:continue
            self.live_img=PIL.ImageOps.pad(img,(self.x,self.y))
            self.root.after(0,self.upd_live_img)
            if (self.live_timer-int(time.time()-self.cur_time))<1:
                self.shoot()
                self.cur_time=time.time()
                count+=1
                if count>self.img_count-1:
                    break
        resp = requests.get(f'{self.digicam_url}/?CMD=LiveViewWnd_Hide')
        self.final_booth()



    def final_booth(self):
        for x in self.download_list:
            r = requests.get(f'{self.digicam_url}/image/{x}', stream=True)
            i=PIL.Image.open(r.raw)
            t=i.getexif()
            exif = {e: t[e] for e in t}
            for o in self.output_q:
                o.put([i.copy(),{'filename':x,'exif':exif,'callback':self.self_q}])

        if not self.confirm_waiter:
            root.after(1,self.init_start)
        else:
            while True:
                if not self.self_q.empty():
                    image,vars=self.self_q.get()
                    self.self_q.task_done()
                    self.confirm_image(image,vars)
                    break
                time.sleep(0.1)



    def confirm_image(self,image,vars):
        self.temp_output=(image.copy(),vars)
        image.thumbnail((self.x,self.y))
        self.aprove_temp=PIL.ImageTk.PhotoImage(image)
        self.canvas.create_image(0,0,image=self.background_img,tags=('image',),anchor=NW)
        dx=(self.x-image.size[0])/2
        dy=(self.y-image.size[1])/2
        self.canvas.create_image(dx,dy,image=self.aprove_temp,tags=('image',),anchor=NW)  
        self.canvas.create_image(0,0,image=self.approve_img,tags=('image',),anchor=NW)  
        self.canvas.tag_bind('image','<Button-1>', self.approve_or_deny) 


    def approve_or_deny(self,event=None):
        if event.x<self.canvas.winfo_width()/2:
            image,vars=self.temp_output
            del vars['callback']
            vars['confirm_callback'].put([image,vars])

        self.canvas.tag_unbind('image', '<Button-1>')
        self.init_start()

        


    def parse_img_list(self,event=None,wait=False):
        ret=[]
        while True:
            r = requests.get(f'{self.digicam_url}/slide.html')
            try:tree = lxml.html.fromstring(r.text)
            except:continue
            try:res=tree.xpath('//figcaption[@itemprop="caption description"]')
            except:continue
            for x in res:
                cur=x.text.strip()
                if cur not in self.digicam_list:
                    ret.append(cur)
                    self.digicam_list.append(cur)
            if not wait:break
            if ret:break
            time.sleep(0.1)
        return ret





    def shoot(self):
        r = requests.get(f'{self.digicam_url}/?CMD=Capture')
        img=self.parse_img_list(wait=True)
        for x in img:
            self.download_list.append(x)
        sys.stdout.flush()
        #resp=requests.get(self.digicam_url+'/liveview.html?CMD=LiveViewWnd_Hide')
        #resp=requests.get(self.digicam_url+'/liveview.html?CMD=LiveViewWnd_Show')       

















def run(store,settings,message_q,output_q,self_id,self_q=None):
    gui=Gui(root,settings,self_q,output_q)
    #th=threading.Thread(target=run_in,args=(gui,settings,self_q,message_q,self_id))
    #th.start()
    root.mainloop()






    

