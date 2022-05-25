from pathlib import Path
from PIL import Image
import time
import os
import sys
from app.utils import *



def run(store,settings,message_q,output_q,self_id,self_q=None):

	while True:
		if not self_q.empty():
			image,vars=self_q.get()
			self_q.task_done()
			message=[self_id,Path(vars['filename']).name+f'\nCopies #{settings["copies"]}']
			message_q.put(message)
			for x in range(settings['copies']):
				for o in output_q:
					o.put([image.copy(),vars])


		time.sleep(0.01)