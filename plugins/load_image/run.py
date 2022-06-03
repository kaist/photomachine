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
        try:
            image=Image.open(vars['original_filename'])
            vars['loaded']=True
        except:
            return None,None,'Not loaded (skip):\n'+Path(vars['filename']).name
    return image,vars,msg