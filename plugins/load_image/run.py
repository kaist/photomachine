from pathlib import Path
from PIL import Image
import time
import os
import sys
from app.utils import *



@run_thread
def run(store,settings,image,vars):
    msg='Loading:\n'+Path(vars['filename']).name
    if not vars['loaded']:
        image=Image.open(vars['filename'])
        vars['loaded']=True
        return image,vars,msg
    else:
        return image,vars,msg