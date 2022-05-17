from pathlib import Path
from PIL import Image
import time
import os
import sys
from app.utils import *
import requests
import io
import requests








@run_thread
@retry_on_error
def run(store,settings,image,vars):
    fp=io.BytesIO()
    image.save(fp,format="jpeg",exif=image.getexif(),icc_profile=vars.get('profile',None),quality=80,optimize=True)
    fp.seek(0)
    request = requests.post(settings['url'], files={'photo':(Path(vars['filename']).parts[-1],fp)})
    msg='Sent to server:\n'+str(Path(vars['filename']).name)
    return None,None,msg