from PIL import Image
from pathlib import Path
import tempfile
import time
import pickle
import sys



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


def retry_on_error(fn):
    def wr(store,settings,image,vars):
        while True:
            try:
                ret=fn(store,settings,image,vars)
                is_ok=True
            except:is_ok=False
            if is_ok:break
            time.sleep(1)
        return ret

    return wr

def run_thread(fn):
    def wr(store,settings,message_q,output_q,self_id,self_q=None):
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
        self.__dict__['plug_path'] = (
            Path().home() / Path('.photomachine') / Path(f'{pname}.store')
        )

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









