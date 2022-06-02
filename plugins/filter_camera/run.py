from pathlib import Path
from PIL import Image
import time
import os
import sys
from app.utils import *

from PIL import ExifTags

@run_thread
def run(store,settings,image,vars):

    exif=vars['exif']
    tags=[]

    for x in exif:
        if ExifTags.TAGS[x]in ['Model','LensModel','Copyright','BodySerialNumber']:
            tags.append(exif[x])

    if not tags:
        msg='No EXIF (skip):\n'+Path(vars['filename']).name
        return None,vars,msg 
    apr=False
    for t in tags:
        if settings['contain'].lower() in t.lower():
            apr=True
    if apr:
        msg='Approved:\n'+Path(vars['filename']).name
        return image,vars,msg  
    else:
        msg='Skip:\n'+Path(vars['filename']).name
        return None,vars,msg             


