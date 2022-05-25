from pathlib import Path
from PIL import Image,ImageCms
import time
import os
import sys
import io
from app.utils import *
import requests
import locale
import subprocess
enc=locale.getpreferredencoding()


def all_files():
    lst=[]
    known_urls=[]
    def flist(url):
        known_urls.append(url)
        root = requests.get(f'http://ezshare.card/{url}')
        for x in root.text.split('\n'):
            if '/download?file' in x:
                dwn=x.split('="')[1].split('">')[0]
                if dwn.lower().endswith('.jpg'):
                    lst.append(dwn)
            if 'dir?dir=' in x:
                durl=x.split('="')[1].split('">')[0]
                if durl not in known_urls:
                    flist(durl)

    root=flist('dir?dir=A:')
    return lst



def run(store,settings,message_q,output_q,self_id,self_q=None):
    if settings['autoclean']:
        store.image_list=[]
    try:image_list=store.image_list
    except:
        image_list=[]
        store.image_list=[]

    count=0
    while True:
        is_ok=True
        if settings['connect']:
            cur_ap=''
            cur=subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces']).decode(enc,errors='ignore').split('\n')
            for x in cur:
                if ' SSID: ' in x:
                    cur_ap=x.split(': ')[1].split('\n')[0]
            if cur_ap.strip()!=settings['ap'].strip():
                try:data = subprocess.check_output(['netsh', 'wlan', 'connect', f'name={settings["ap"]}'])
                except:
                    is_ok=False
                    message=[self_id,'EzShare is not available']
                    message_q.put(message)
                    time.sleep(5)
                    continue

            time.sleep(5)
        message=[self_id,'Getting image list...']
        message_q.put(message)
        try:lst=all_files()
        except:
            is_ok=False
            lst=[]

        for x in lst:
            if not is_ok:break
            if x in image_list:continue
            try:
                r=requests.get(x,stream=True)
                i=io.BytesIO()
                i.write(r.raw.read())
                i.seek(0)
                img=Image.open(i)
            except:
                is_ok=False
                continue

            t=img.getexif()
            exif = {e: t[e] for e in t}
            try:xmp=img.getxmp()
            except:xmp={}
            filename=x.split('%5C')[-1]

            try:
                icc_profile =img.info.get('icc_profile')
            except:
                icc_profile=None
            for o in output_q:
                vars={'filename':filename,'count':count,'exif':exif,'profile':icc_profile,'loaded':True,'xmp':xmp}
                message=[self_id,'Load file {0} \n(count: {1})'.format(filename,count)]
                message_q.put(message)
                o.put([img.copy(),vars])
            image_list.append(x)
            store.image_list=image_list
            count+=1
        if is_ok:
            message=[self_id,'Waiting...']
        else:
            message=[self_id,'EzShare is not available']
        message_q.put(message)
        if settings['disconnect']:
            try:data = subprocess.check_output(['netsh', 'wlan', 'connect', f'name={settings["dis_ap"]}'])
            except:pass





        time.sleep(settings['pause'])


