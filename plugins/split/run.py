from pathlib import Path
from PIL import Image
import time
import os
import sys
from app.utils import *



def run(store,settings,message_q,output_q,self_id,self_q=None):
	cur=0
	q_count=len(output_q)
	while True:
		if not self_q.empty():
			image,vars=self_q.get()
			self_q.task_done()
			message=[self_id,Path(vars['filename']).name+f'\nSending to #{cur+1}']
			message_q.put(message)
			output_q[cur].put([image.copy(),vars])
			cur+=1
			if cur>(q_count-1):
				cur=0

		time.sleep(0.01)

