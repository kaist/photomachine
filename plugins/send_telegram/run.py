from pathlib import Path
from PIL import Image
import time
import os
import sys
from app.utils import *
import requests
import io
import json

@run_thread
@retry_on_error
def run(store,settings,image,vars):
    fp=io.BytesIO()
    image.save(fp,format="jpeg",exif=image.getexif(),icc_profile=vars.get('profile',None),quality=80,optimize=True)
    fp.seek(0)
    files = {'image': fp}
    values = {'fname':vars['filename'],'caption':settings['caption'],'key':settings['key'],'asdoc':settings['asdoc']}
    r = requests.post('https://machine.zalomskij.ru/telegram/bot_sendphoto/', files=files, data=values)
    resp=json.loads(r.text)
    msg='Sent to telegram:\n'+str(Path(vars['filename']).name)
    return None,None,msg