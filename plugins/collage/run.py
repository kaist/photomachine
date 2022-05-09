from pathlib import Path
from PIL import Image,ImageOps
import time
import os
import sys
from app.utils import *



def run(store,settings,message_q,output_q,self_id,self_q=None):
    cur=0
    is_complete=True
    q_count=len(settings['elements'])
    tmr=time.time()
    while True:
        if not self_q.empty():
            image,vars=self_q.get()
            self_q.task_done()
            message=[self_id,f'Image #{cur+1} in collage:\n'+Path(vars['filename']).name]
            message_q.put(message)
            tmr=time.time()
            el=settings['elements'][cur]
            if cur==0:
                is_complete=False
                i=Image.new('RGB',(int(settings['hsize']),int(settings['vsize'])),'white')

            if int(el['contain'])==0:
                tp=ImageOps.pad(image,(el['sizex'],el['sizey']),color='white')
            else:
                tp=ImageOps.fit(image,(el['sizex'],el['sizey']))
            i.paste(tp,(el['x'],el['y']))


            #message=[self_id,Path(vars['filename']).name+f'\nSending to #{cur+1}']
            #message_q.put(message)
            #output_q[cur].put([image.copy(),vars])
            cur+=1
            if cur>(q_count-1):
                is_complete=True
                for o in output_q:
                    o.put([i.copy(),vars])
                cur=0
        if is_complete==False and (time.time()-tmr)>int(settings['timeout']):
            for o in output_q:
                o.put([i.copy(),vars])
            is_complete=True
            cur=0
            message=[self_id,f'Timeout!\n'+Path(vars['filename']).name]
            message_q.put(message)     
        time.sleep(0.01)

