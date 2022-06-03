import os
from PIL import Image
from pathlib import Path
import tempfile
import time
import pickle
import sys
import io
import struct

DATA_PATH=Path(os.environ['DATA_PATH'])



def image_open(path=None,fp=None,just_metadata=False):
    if path.suffix=='.pmi':
        fp=open(path,'rb')
        return from_pm(fp)

    if fp:
        img=Image.open(fp)
    else:
        img=Image.open(path)
    try:xmp=img.getxmp()
    except:xmp={}
    try:filename=img.filename
    except:
        filename=path
    try:
        icc_profile =img.info.get('icc_profile')
    except:
        icc_profile=None
    try:t=img.getexif()
    except:t={}
    if just_metadata:
        img=Image.new('RGB',(1,1))
        loaded=False
    else:        
        img.load()
        loaded=True        

    exif = {e: t[e] for e in t}
    try:
        exif2=img.getexif().get_ifd(0x8769)
        exif.update(exif2)
    except:pass
    vars={'filename':filename,'exif':exif,'profile':icc_profile,'loaded':loaded,'xmp':xmp}
    return img,vars

def to_pm(image,vars):
    img_fp=io.BytesIO()
    if image.mode!='RGB':
        image=image.convert('RGB')
    image.save(img_fp,format='jpeg',quality=90,exif=image.getexif(),icc_profile=vars.get('profile',None))
    img_len=img_fp.getbuffer().nbytes
    img_fp.seek(0)

    data_fp=io.BytesIO()
    pickle.dump(vars, data_fp, pickle.HIGHEST_PROTOCOL)
    data_len=data_fp.getbuffer().nbytes
    data_fp.seek(0)

    main_fp=io.BytesIO()
    main_fp.write(struct.pack('ll',img_len,data_len))
    main_fp.write(img_fp.read())
    main_fp.write(data_fp.read())
    main_fp.seek(0)
    return main_fp

def from_pm(fp):
    fp.seek(0)
    img_len,data_len=struct.unpack('ll',fp.read(8))

    img_io=io.BytesIO()
    img_io.write(fp.read(img_len))
    img_io.seek(0)

    data_io=io.BytesIO()
    data_io.write(fp.read(data_len))
    data_io.seek(0)

    image=Image.open(img_io)
    vars=pickle.load(data_io)
    return image,vars







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
            DATA_PATH/ Path(f'{pname}.store')
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









