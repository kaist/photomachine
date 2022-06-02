from pathlib import Path
from PIL import Image
import time
import os
import sys
from app.utils import *

from datetime import datetime,timedelta
from PIL import ExifTags

@run_thread
def run(store,settings,image,vars):
    now=datetime.now()

    exif=vars['exif']
    for x in exif:
        if ExifTags.TAGS[x]=='DateTime':
            dt=exif[x]
            dt=datetime.strptime(dt, '%Y:%m:%d %H:%M:%S')
            break
    if not dt:
        msg='No EXIF (skip):\n'+Path(vars['filename']).name
        return None,vars,msg 

    if settings['units']==0:
        delta=timedelta(days=settings['time'])
    elif settings['units']==1:
        delta=timedelta(hours=settings['time'])
    else:
        delta=timedelta(minutes=settings['time'])
    delta_exif=now-dt

    sys.stdout.flush()


    if settings['if']==0:
        if_bool=delta_exif>delta
    else:
        if_bool=delta_exif<delta

    if if_bool:
        msg='Approved:\n'+Path(vars['filename']).name
        return image,vars,msg
    else:
        msg='Skip:\n'+Path(vars['filename']).name
        return None,vars,msg