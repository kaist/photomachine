from pathlib import Path
from PIL import Image,ImageCms
import time
import os
import sys
import io
from app.utils import *
from PIL.ExifTags import TAGS
import defusedxml

def run(store,settings,message_q,output_q,self_id,self_q=None):
    if settings['autoclean']:
        store.image_list=[]
    count=0
    while True:
        if settings['subfolder']==0:
            p=Path(settings['path']).glob('*.*')
        else:
            p=Path(settings['path']).glob('**/*')        
        for x in p:
            if settings['remember']==1:
                try:i_list=store.image_list
                except:
                    store.image_list=[]
                    i_list=store.image_list
                if str(x) in i_list:
                    continue
                i_list.append(str(x))
                store.image_list=i_list

            try:
                img=Image.open(x)
                exif=img.getexif()
                try:xmp=img.getxmp()
                except:xmp={}
                filename=img.filename

                try:
                    icc_profile =img.info.get('icc_profile')
                except:
                    icc_profile=None
                if settings['metadata']:
                    img=Image.new('RGB',(1,1))
                    loaded=False
                else:        
                    img.load()
                    loaded=True        
            except:continue
            for o in output_q:
                vars={'filename':filename,'count':count,'exif':exif,'profile':icc_profile,'loaded':loaded,'xmp':xmp}
                message=[self_id,'Load file {0} \n(count: {1})'.format(x.name,count)]
                message_q.put(message)
                o.put([img.copy(),vars])
            if settings['delete']==1:
                try:x.unlink()
                except:pass
            count+=1
            time.sleep(0.1)
        message_q.put([self_id,'All done!'])
        if settings['watch']:
            message_q.put([self_id,f'Waiting...\n(count: {count})'])
            time.sleep(settings['interval'])
        else:
            break

