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
        return static_file(filepath, root=self.root_path+'/static')


    def index(self):
        images={}
        return template('index.html', images={})

    def get_json(self):
        output=[]
        for x in self.store.image_list:
            output.append({'img':'images/'+Path(x[1]['filename']).parts[-1]})
        response.content_type = 'application/json'
        return json.dumps(output)



    def server_images(self,filepath):

        for x in self.store.image_list:
            if Path(x[1]['filename']).parts[-1]==filepath:
                i=x[0]
                buf=io.BytesIO()
                i.save(buf,format='jpeg')
                buf.seek(0)
                response.headers['Content-Type'] = 'image/jpeg'

                return buf.read()

    def run(self):
        bottle.route('/static/<filepath:path>',name='static', callback=self.server_static)
        bottle.route('/images/<filepath:path>',name='images',callback=self.server_images)
        bottle.route('/',callback=self.index)
        bottle.route('/get_json',callback=self.get_json)        
        bottle.run(host='0.0.0.0',port=self.settings['port'],debug=True)



def start_getter(store,self_q,message_q,self_id):
    while True:
        if not self_q.empty():
            image,vars=self_q.get()
            for x in store.image_list:
                if x[1]['filename']==vars['filename']:
                    return
            imgs=store.image_list
            imgs.append([image,vars])
            store.image_list=imgs
            print('add')
            message_q.put([self_id,'Add:\n'+Path(vars['filename']).name])
        time.sleep(0.1)

def run(store,settings,message_q,output_q,self_id,self_q=None):
    if settings['autoclean']:
        store.image_list=[]
    web=Web(settings,store)

    th=threading.Thread(target=start_getter,args=(store,self_q,message_q,self_id))
    th.start()

    web.run()





