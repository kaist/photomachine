from pathlib import Path
from PIL import Image
import time
import os
import sys
from app.utils import *
import pillow_lut




@run_thread
def run(store,settings,image,vars):
	if settings['blend']==100:
		lut=pillow_lut.load_cube_file(settings['path'])
		image=image.filter(lut)
	else:
		old=image.copy()
		lut=pillow_lut.load_cube_file(settings['path'])
		image=image.filter(lut)		
		image=Image.blend(old,image,alpha=settings['blend']/100)
	msg='Finish for\n'+Path(vars['filename']).name
	return image,vars,msg