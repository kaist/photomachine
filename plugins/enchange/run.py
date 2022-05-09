from pathlib import Path
from PIL import Image,ImageEnhance,ImageFilter
import time
import os
import sys
from app.utils import *


import sys

@run_thread
def run(store,settings,image,vars):
	d={'sharpness':ImageEnhance.Sharpness,'color':ImageEnhance.Color,'contrast':ImageEnhance.Contrast,'brightness':ImageEnhance.Brightness}

	for name in ['color','contrast','brightness','sharpness']:
		val=int(settings[name])


		if val!=0:
			enhancer=d[name](image)
			image=enhancer.enhance(float(val+100)/100.0)

	if settings['enable_unsharp']:
		image=image.filter(ImageFilter.UnsharpMask(radius = int(settings['radius']), percent = int(settings['percent']), threshold = int(settings['threshold'])))

	msg='Finish for\n'+Path(vars['filename']).name
	return image,vars,msg