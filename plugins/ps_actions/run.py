from pathlib import Path
from PIL import Image
import time
import os
import sys
from app.utils import *

import photoshop.api as ps
from photoshop import Session
import sys
import json

@run_thread
def run(store,settings,image,vars):
    pth=pil_to_file(image)
    with Session(str(pth), action="open") as ps1:
        ps1.app.doAction(action=settings['action'],action_from=settings['sets'])

    i=file_to_pil(pth)
    msg='Finish for\n'+Path(vars['filename']).name
    
    return i,vars,msg