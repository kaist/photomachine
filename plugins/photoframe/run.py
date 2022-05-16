from pathlib import Path
from PIL import Image,ImageOps
import time
import os
import sys
from app.utils import *



@run_thread
def run(store,settings,image,vars):
    if image.size[0]>image.size[1]:
        frame = (
            Image.open(settings['hpath'])
            if settings['hpath']
            else Image.open(settings['vpath'])
        )

    elif settings['vpath']:
        frame=Image.open(settings['vpath'])
    else:
        frame=Image.open(settings['hpath'])

    if int(settings['contain'])==0:
        image=ImageOps.fit(image,frame.size)
    else:
        frame=ImageOps.fit(frame,image.size)
    image.paste(frame,(0,0),frame)


    msg='Finish for\n'+Path(vars['filename']).name
    return image,vars,msg
