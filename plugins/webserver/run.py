from pathlib import Path
from PIL import Image
import time
import os
import sys
from app.utils import *
import io
import threading
import bottle
from bottle import route, run, template,view,static_file,response
import json
import shutil
import qrcode

c_path=DATA_PATH/Path('webserver')

class Web:
    def __init__(self,settings,store):
        self.settings=settings
        self.store=store
        if settings['external']==0:
            self.root_path='plugins/webserver/themes/'+settings['theme']
        else:
            self.root_path=settings['path']
        bottle.TEMPLATE_PATH.append(self.root_path)




    def server_static(self,filepath):
        return static_file(filepath, root=f'{self.root_path}/static')


    def index(self):
        images={}
        return template('index.html', images={},text=self.settings['text'])

    def get_json(self):
        output = [
            {'img': 'images/' + Path(x).parts[-1]}
            for x in self.store.image_list
        ]

        response.content_type = 'application/json'
        return json.dumps(output)



    def server_images(self,filepath):

        for x in self.store.image_list:
            if Path(x).parts[-1]==filepath:
                f=open((c_path/Path(x).parts[-1]).with_suffix('.phi'),'rb')
                image,vars=from_pm(f)
                f.close()
                buf=io.BytesIO()
                image.save(buf,format='jpeg')
                buf.seek(0)
                response.headers['Content-Type'] = 'image/jpeg'
                return buf.read()

    def logo(self):
        if self.settings['logo'] and not self.settings['link']:
            fp=open(self.settings['logo'],'rb')
            response.headers['Content-Type'] = 'image/jpeg'
            return fp.read()
        if self.settings['link']:
            img = qrcode.make(self.settings['link'])
            buf=io.BytesIO()
            img.save(buf,format='png')
            buf.seek(0)
            response.headers['Content-Type'] = 'image/png'
            return buf.read()
    def bg(self):
        if self.settings['bg']:
            fp=open(self.settings['bg'],'rb')
            response.headers['Content-Type'] = 'image/jpeg'
            return fp.read()       


    def run(self):
        bottle.route('/static/<filepath:path>',name='static', callback=self.server_static)
        bottle.route('/images/<filepath:path>',name='images',callback=self.server_images)
        bottle.route('/logo.png',name='logo',callback=self.logo)
        bottle.route('/bg.jpg',name='bg',callback=self.bg)
        bottle.route('/',callback=self.index)
        bottle.route('/get_json',callback=self.get_json)        
        bottle.run(host='0.0.0.0',port=self.settings['port'],debug=True)



def start_getter(store,self_q,message_q,self_id):
    while True:
        if not self_q.empty():
            image,vars=self_q.get()
            self_q.task_done()
            for x in store.image_list:
                if x==vars['filename']:
                    return
            imgs=store.image_list
            imgs.append(vars['filename'])
            store.image_list=imgs
            fp=to_pm(image,vars)
            with open((c_path/Path(vars['filename']).parts[-1]).with_suffix('.phi'),'wb') as f:
                f.write(fp.read())
            del fp
            message_q.put([self_id,'Add:\n'+Path(vars['filename']).name])
        time.sleep(0.1)

def run(store,settings,message_q,output_q,self_id,self_q=None):
    if settings['autoclean']:
        store.image_list=[]
        try:shutil.rmtree(c_path)
        except:pass
    if not c_path.exists():
        c_path.mkdir()
    web=Web(settings,store)

    th=threading.Thread(target=start_getter,args=(store,self_q,message_q,self_id))
    th.start()

    web.run()





