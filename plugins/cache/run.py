from pathlib import Path
from PIL import Image
import time
import os
import sys
from app.utils import *
from queue import Queue
import threading


q=Queue()

path=Path().home()/Path('.photomachine')/Path('cache')

def pusher(store,output_q,self_id,message_q):
	while True:
		tarr=store.cache
		try:el=tarr.pop(0)
		except:
			time.sleep(0.01)
			continue
		store.cache=tarr
		img=Image.open(path/(Path(el['filename']).parts[-1]))
		for x in output_q:
			x.put([img.copy(),el])
		(path/Path(el['filename']).parts[-1]).unlink()

		message=[self_id,f'In cache {len(store.cache)} images.']
		message_q.put(message)
		time.sleep(0.01)


def run(store,settings,message_q,output_q,self_id,self_q=None):
	if not(path.exists()):
		path.mkdir()
	th=threading.Thread(target=pusher,args=(store,output_q,self_id,message_q))
	th.start()
	while True:
		if not self_q.empty():
			image,vars=self_q.get()
			self_q.task_done()
			image.save(path/(Path(vars['filename']).parts[-1]),quality=100)
			d=store.cache
			d.append(vars)
			store.cache=d


			#q.put([image,vars])



			message=[self_id,f'In cache {len(d)} images.']
			message_q.put(message)
			#output_q[cur].put([image.copy(),vars])


		time.sleep(0.01)

