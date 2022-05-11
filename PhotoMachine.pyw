import sys,os
sys.dont_write_bytecode=True
from pathlib import Path

if hasattr(sys,"frozen"):
    os.chdir(os.path.dirname(sys.executable))

    p=Path().home()/Path('.photomachine')/Path('error.txt')
    if not p.parent.exists():
        p.parent.mkdir()
    sys.stderr=open(p,'a+')



VERSION='1.05'

import threading
from pathlib import Path
from importlib.machinery import SourceFileLoader
import json
import time
import multiprocessing
import sys 
import os 
import psutil
import pickle

from app.utils import PluginStore





MAX_Q=3

def start_plug(path,settings,message_q,output_q,self_id,self_q=None):
    run=SourceFileLoader("run", str(path/'run.py')).load_module().run
    store=PluginStore(Path(path).parts[-1])
    run(store,settings,message_q,output_q,self_id,self_q)


class App:
    def __init__(self,gui,open_file,startup_start):
        
        self.version=VERSION
        self.favorites=[]

        p=Path().home()/Path('.photomachine')/Path('favorites.items')
        if p.exists():
            with open(p,'rb') as f:
                try:self.favorites=pickle.load(f)
                except:pass

        self.startup_start=startup_start
        self.plug_q={}
        self.app_run=True
        self.cur_filename=None
        self.gui=gui
        self.is_start=False
        self.gui.app=self
        self.all_process=[]
        self.plugins=[]
        self.plug_actions=[]
        self.init_plugins()






        th=threading.Thread(target=self.dispatcher,args=())
        th.start()
        if open_file:
            self.load_state(open_file)


    def init_plugins(self):
        plugins=Path('plugins/').glob('*')
        for p in plugins:
            if p.is_dir():
                try:foo = SourceFileLoader("Plugin", str(p/'plugin.py')).load_module().Plugin()
                except ModuleNotFoundError:continue
                foo.icon=PhotoImage(file=str(p/'icon.png'))
                foo.path=p  
                self.plugins.append(foo)

                    
        self.gui.init_plugins_gui()
        self.gui.init_favorites_gui()

    def find_by_path(self,path):
        for p in self.plugins:
            if path==str(p.path):
                return p


    def find_by_uid(self,uid):
        for p in self.plug_actions:
            if str(uid)==str(p.id):
                return p

    def connect(self,from_id,to_id):
        plug=self.find_by_uid(from_id)
        plug.outputs.append(to_id)
        self.gui.update_lines()

    def disconnect(self,uids):
        from_uid,to_uid=uids
        plug=self.find_by_uid(from_uid)
        plug.outputs.remove(to_uid)
        self.gui.update_lines()

    def delete_action(self,uid):
        plug=self.find_by_uid(uid)
        self.plug_actions.remove(plug)
        for x in self.plug_actions:
            try:x.outputs.remove(str(uid))
            except:pass
        self.gui.redraw_canvas()


    def update_coords(self,uid,x,y):
        plug=self.find_by_uid(uid)
        plug.x=x
        plug.y=y

    def config_action(self,uid,frame):
        plug=self.find_by_uid(uid)
        plug.plugin.start_config(frame,plug)

    def save_config(self,uid):
        plug=self.find_by_uid(uid)    
        plug.settings=plug.plugin.save_config() 

    def remove_favorite(self,sets):
        self.favorites.remove(sets)
        p=Path().home()/Path('.photomachine')/Path('favorites.items')
        if not p.parent.exists():
            p.parent.mkdir()
        with open(p,'wb') as f:
            pickle.dump(self.favorites,f)        

    def save_favorite(self,uid,name):
        plug=self.find_by_uid(uid)
        self.favorites.append([str(plug.plugin.path),plug.settings,name])
        p=Path().home()/Path('.photomachine')/Path('favorites.items')
        if not p.parent.exists():
            p.parent.mkdir()
        with open(p,'wb') as f:
            pickle.dump(self.favorites,f)
        self.gui.init_favorites_gui()


    def to_dump(self):
        output=[]
        for act in self.plug_actions:
            d={}
            d['id']=act.id
            d['x']=act.x
            d['y']=act.y
            d['plugin']=str(act.plugin.path)
            d['outputs']=act.outputs
            d['settings']=act.settings
            d['name']=act.name
            output.append(d)
        return output


    def save_state(self,filename=None):
        if not filename:
            filename=self.cur_filename
        self.cur_filename=filename
        root.title('PhotoMachine > '+filename)
        f=open(filename,'w')
        c=json.dumps(self.to_dump())
        f.write(c)
        f.close()

    def new_state(self):
        self.cur_filename=None
        root.title('PhotoMachine')
        self.plug_actions=[]
        self.gui.redraw_canvas()
        self.gui.update_lines()           

    def from_dump(self,obj):
        self.plug_actions=[]
        for x in obj:
            n=PlugAction()
            n.id=x['id']
            n.x=x['x']
            n.y=x['y']
            n.outputs=x['outputs']
            n.settings=x['settings']
            n.path=x['plugin']
            n.name=x['name']
            p=Path(x['plugin'])
            foo = SourceFileLoader("Plugin", str(p/'plugin.py')).load_module().Plugin()
            foo.icon=PhotoImage(file=str(p/'icon.png'))
            foo.path=p
            n.plugin=foo
            self.plug_actions.append(n)
        self.gui.redraw_canvas()
        self.gui.update_lines()


    def load_state(self,filename):
        self.cur_filename=filename
        root.title('PhotoMachine > '+filename)
        f=open(filename)
        c=json.loads(f.read())
        self.from_dump(c)

    def start(self):
        self.is_start=True
        self.plug_q={}
        self.all_process=[]
        for plug in self.plug_actions:
                q=self.manager.Queue(maxsize=5)
                self.plug_q[plug.id]=q

        for work in self.plug_actions:
            out_q=[]
            for o in work.outputs:
                out_q.append(self.plug_q[o])
            #plug,settings,message_q,output_q,self_id,out_q
            p=multiprocessing.Process(target=start_plug,args=(work.plugin.path,work.settings,self.q,out_q,work.id,self.plug_q[work.id]))
            p.start()
            self.all_process.append(p)

             

    def stop(self):
        self.gui.start_but['state']=DISABLED
        for x in self.all_process:
            x.kill()

        while not self.q.empty():
            try:
                self.q.get(False)
            except Empty:
                continue
            self.q.task_done()


        for t in self.plug_q:
            x=self.plug_q[t]
            while not x.empty():
                try:
                    x.get(False)
                    x.task_done()   
                except Empty:
                    continue
                
        self.plug_q={}         
        self.all_process=[]
        self.is_start=False
        self.gui.start_but['state']=NORMAL

    def on_closing(self):
        self.stop()
        self.app_run=False
        root.destroy()

    def update_ps(self):
        ch=self.proc.children()
        ram=self.proc.memory_info()[0]
        for x in ch:
            ram+=x.memory_info()[0]
        ram=int(ram/1024/1024)
        cpu=int(psutil.cpu_percent(interval=None))
        self.gui.update_pstext(cpu,ram)


    def dispatcher(self):

        self.proc=psutil.Process()

        self.manager=multiprocessing.Manager()

        self.q=self.manager.Queue()
        if self.startup_start:
            self.gui.startstop()
        while self.app_run:
            if not self.q.empty():
                message=self.q.get(block=False)
                self.q.task_done()
                self.gui.new_message(message)

            time.sleep(0.01)


if __name__=='__main__':
    multiprocessing.freeze_support()
    open_file=False
    startup_start=False
    if len(sys.argv)>1:
        open_file=sys.argv[1]
        if '--start' in sys.argv:
            startup_start=True


    from tkinter import Tk
    from app.gui import *
    root=Tk()
    root.withdraw()
    gui=Gui(root)
    app=App(gui,open_file=open_file,startup_start=startup_start)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


