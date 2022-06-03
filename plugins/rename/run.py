from pathlib import Path
from PIL import Image
import time
import os
import sys
from app.utils import *
from datetime import datetime
from PIL import ExifTags



def run(store,settings,message_q,output_q,self_id,self_q=None):
    if settings['autoclean']:
        store.counter=0
    try:
        counter=store.counter
    except:
        store.counter=0
    counter=store.counter
    while True:
        if not self_q.empty():
            image,vars=self_q.get()
            self_q.task_done()
            p=Path(vars['filename'])
            patt=settings['templ']
            digs=settings['digits']
            dt=datetime.now()
            if settings['time']==0:
                exif=vars['exif']
                for x in exif:
                    if ExifTags.TAGS[x]=='DateTime':
                        dt=exif[x]
                        dt=datetime.strptime(dt, '%Y:%m:%d %H:%M:%S')
                        break

            c=str(counter).zfill(digs)
            patt=patt.replace('[COUNT]',c)
            patt=patt.replace('[YEAR]',dt.strftime('%Y'))
            patt=patt.replace('[MONTH]',dt.strftime('%m'))
            patt=patt.replace('[DAY]',dt.strftime('%d'))  
            patt=patt.replace('[HOUR]',dt.strftime('%H'))
            patt=patt.replace('[MINUTE]',dt.strftime('%M'))
            patt=patt.replace('[SECOND]',dt.strftime('%S'))   
            new_path=Path(patt+p.suffix)
            msg='New name:\n'+new_path.name
            message_q.put([self_id,msg])
            vars['filename']=new_path
            vars['is_renamed']=True
            for o in output_q:
                o.put([image.copy(),vars])
            counter+=1
            store.counter=counter
        time.sleep(0.1)