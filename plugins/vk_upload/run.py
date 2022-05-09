from pathlib import Path
from PIL import Image
import time
import os
import sys
from app.utils import *
import requests
import io
import json
import requests
import vk



def parse_album(url):
    uid,album='',''
    part=url.split('album')[1]
    uid=part.split('_')[0]

    for ch in part.split('_')[1]:
        if ch.isdigit():
            album+=ch
        else:
            break
    return uid,album





@run_thread
def run(store,settings,image,vars):
    image.thumbnail((7500,7500))
    print(image.size)
    fp=io.BytesIO()
    image.save(fp,format="jpeg",exif=vars.get('exif',None),icc_profile=vars.get('profile',None),quality=80,optimize=True)
    fp.seek(0)
    session = vk.Session(access_token=settings['key'])
    api = vk.API(session)
    uid,album=parse_album(settings['album'])
    group_id=uid.replace('-','') if uid.startswith('-') else None
    upload_url = api.photos.getUploadServer(album_id=album,group_id=group_id,v='5.131')['upload_url']
    request = requests.post(upload_url, files={'photo':(Path(vars['filename']).parts[-1],fp)})
    params = {'server': request.json()['server'],
          'hash': request.json()['hash'],
          'caption':settings['caption'],
          'group_id':group_id,
          'album_id':album,
          'photos_list':request.json()['photos_list'],
          'v':'5.131',

          }
    photo_id = api.photos.save(**params)[0]['id']
    sys.stdout.flush()





    msg='Sent to VK:\n'+str(Path(vars['filename']).name)
    return None,None,msg