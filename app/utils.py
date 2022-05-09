from PIL import Image
from pathlib import Path
import tempfile
import threading
import time
import pickle
import subprocess
import io


def check_raw(filename,image=None):
    if str(filename).lower().endswith('.cr2'):
        dcraw_opts = ["app/dcraw", "-c", "-e", filename]
        dcraw_proc = subprocess.Popen(dcraw_opts, stdout=subprocess.PIPE,shell=False)
        image = io.BytesIO(dcraw_proc.communicate()[0])
        image.seek(0)
        img=Image.open(image)
        return img
    else:
        if image:return image
        else:
            try:
                return Image.open(filename)
            except:return None



def pil_to_file(image):
    dirpath = tempfile.mkdtemp()
    image.save(Path(dirpath)/'image.tif')
    return Path(dirpath)/'image.tif'

def file_to_pil(pth):
    i=Image.open(pth)
    i.load()
    Path(pth).unlink()
    try:Path(pth).parent.unlink()
    except:pass
    return i


def run_thread(fn):
    def wr(store,settings,message_q,output_q,self_id,self_q=None):
        print('start',self_id)
        while True:
            if not self_q.empty():
                image,vars=self_q.get()
                self_q.task_done()
                message=[self_id,'Processing\n'+Path(vars['filename']).name]
                message_q.put(message)
                image,out_vars,msg=fn(store,settings,image,vars)
                if msg:
                    message_q.put([self_id,msg],block=False)
                if not image:
                    continue
                for o in output_q:
                    o.put([image.copy(),out_vars])
            time.sleep(0.01)

    return wr


class PluginStore:
    def __init__(self,pname):
        self.__dict__['v']={}
        self.__dict__['plug_path']=Path().home()/Path('.photomachine')/Path(pname+'.store')
        if not self.__dict__['plug_path'].parent.exists():
            self.__dict__['plug_path'].parent.mkdir()
        if self.__dict__['plug_path'].exists():
            with open(self.__dict__['plug_path'],'rb') as f:
                self.__dict__['v']=pickle.load(f)    

    def __setattr__(self,atr,val):
        self.__dict__['v'][atr]=val

        with open(self.__dict__['plug_path'],'wb') as f:
            pickle.dump( self.__dict__['v'],f)

    def __getattr__(self,atr):
        return self.__dict__['v'][atr]









