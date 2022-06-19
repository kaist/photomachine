from pathlib import Path
from PIL import Image
import time
import os
import sys
from app.utils import *
import websockets
import asyncio
import json
import requests
WEBSOCKET_URI = "ws://photo-machine.ru:8001/ws/telegram/"


async def start_socket(settings,message_q,output_q,self_id):
    message_q.put([self_id,'Connecting to server...'])
    try:websocket = await websockets.connect(WEBSOCKET_URI)
    except:
        await asyncio.sleep(1)
        await start_socket(settings,message_q,output_q,self_id)    
        return
    await websocket.send(
            json.dumps(
                {
                    'command':'join',
                    'key':settings['key']
                }
            )
        )
    while True:
        message_q.put([self_id,'Waiting photos...'])
        try:message = json.loads(await websocket.recv())['message']
        except:
            await asyncio.sleep(1)
            await start_socket(settings,message_q,output_q,self_id)
            break
        sys.stdout.flush()
        sys.stdout.flush()
        r=requests.get(message['url'], stream=True)
        r.raw.decode_content = True
        try:img,vars=image_open(path=Path(message['filename']),fp=r.raw,just_metadata=False)
        except:continue
        for o in output_q:
            o.put([img.copy(),vars])

        await asyncio.sleep(0.1)

def run(store,settings,message_q,output_q,self_id,self_q=None):

    #o.put([img.copy(),vars])
    asyncio.run(start_socket(settings,message_q,output_q,self_id))
    message_q.put([self_id,'All done!'])
