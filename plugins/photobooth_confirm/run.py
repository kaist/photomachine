from pathlib import Path
from PIL import Image
import time
import os
import sys
from app.utils import *



def run(store,settings,message_q,output_q,self_id,self_q=None):
    while True:
        if not self_q.empty():
            image,vars=self_q.get()
            self_q.task_done()
            if 'callback' in vars:
                temp_image=[image,vars]
                vars['confirm_callback']=self_q
                vars['callback'].put([image,vars])
            else:
                for o in output_q:
                    o.put([image,vars])


            #message=[self_id,Path(vars['filename']).name+f'\nSending to #{cur+1}']
            #message_q.put(message)
            #output_q[cur].put([image.copy(),vars])

        time.sleep(0.01)

