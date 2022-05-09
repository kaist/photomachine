from pathlib import Path
from PIL import Image
import time
import os
import sys
from app.utils import *



@run_thread
def run(store,settings,image,vars):
    xmp=vars['xmp']
    sys.stdout.flush()
    try:
        rating=int(xmp['xmpmeta']['RDF']['Description']['Rating'])
    except:
        rating=0

    if int(settings['if'])==0:
        bl=rating>int(settings['rating'])
    elif int(settings['if'])==1:
        bl=int(settings['rating'])==rating
    else:
        bl=rating<int(settings['rating'])
    if bl:
        msg='Approved:\n'+Path(vars['filename']).name
        return image,vars,msg
    else:
        msg='Skip:\n'+Path(vars['filename']).name
        return None,vars,msg