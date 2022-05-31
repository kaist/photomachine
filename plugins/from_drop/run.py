from pathlib import Path
import PIL
import time
import os
import sys
from app.utils import *
from pathlib import Path
from tkinter import *
from tkinter.ttk import *
import threading
import ctypes as ct
import tkinterDnD
import queue
root=tkinterDnD.Tk()  
root.title('Drop files')

q=queue.Queue()

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
        self.self_q=self_q
        self.root=root

        self.root.geometry('250x200')
        self.cur_folder=Path(__file__).parent
        self.settings=settings

        self.root.resizable(0,0)
        self.root.focus_force()
        self.root.tk.call('wm', 'iconphoto', self.root._w, PhotoImage(file=str(self.cur_folder/'icon.png')))
        self.root.title('Drop files')
        scale=self.root.winfo_fpixels('1i')/72
        self.root.tk.call('tk', 'scaling', scale)
        self.root.attributes('-topmost', True)
        self.root.update()


        self.root.configure(background='black')


        self.canvas=Canvas(self.root,bd=0, highlightthickness=0, relief='ridge')
        self.canvas.configure(bg='#121212')
        self.canvas.pack(fill=BOTH,expand=True)
        self.f_image=PhotoImage(file=str(self.cur_folder/'image.png'))
        self.canvas.create_image((125,100),image=self.f_image,anchor=CENTER)

        self.canvas.register_drop_target("*")
        self.canvas.bind("<<Drop:DND_Files>>", self.drop)
        self.root.bind_all("<<Paste>>", self.handle_clipboard)


    def handle_clipboard(self,event):
        lines = self.root.clipboard_get().split('\n')
        self.drop(fls=lines)
        

    def drop(self,event=None,fls=None):
        if event:
            fls=self.root.splitlist(event.data)
        filelist=[]
        print(fls)
        for f in fls:
            p=Path(f)
            if p.is_dir():
                l=p.glob('**/*')
                for n in l:
                    filelist.append(n)
            else:
                filelist.append(p)
        for x in filelist:
            q.put(x)
            if self.settings['remember']==1:
                try:i_list=store.image_list
                except:
                    store.image_list=[]
                    i_list=store.image_list
                if str(x) in i_list:
                    continue
                i_list.append(str(x))
                store.image_list=i_list



def run_in(settings,store,message_q,self_id,output_q):
    i_list=[]
    count=0
    while True:
        if not q.empty():
            fl=q.get()
            q.task_done()
            sys.stdout.flush()
            if settings['remember']==1:
                try:i_list=store.image_list
                except:
                    store.image_list=[]
                    i_list=store.image_list
                if str(fl) in i_list:
                    continue
                i_list.append(str(fl))
                store.image_list=i_list




            try:img,vars=image_open(path=x,just_metadata=settings['metadata'])
            except:continue
            vars['count']=count
            for o in output_q:
                message=[self_id,'Load file {0} \n(count: {1})'.format(fl.name,count)]
                message_q.put(message)
                o.put([img.copy(),vars])
            count+=1
            if settings['delete']==1:
                try:x.unlink()
                except:pass


        time.sleep(0.1)










def run(store,settings,message_q,output_q,self_id,self_q=None):
    if settings['autoclean']:
        store.image_list=[]
    gui=Gui(root,settings,self_q)
    th=threading.Thread(target=run_in,args=(settings,store,message_q,self_id,output_q))
    th.start()
    root.mainloop()






    

