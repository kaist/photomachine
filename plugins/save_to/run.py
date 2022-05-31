from pathlib import Path
from PIL import Image
import time
import os
import sys
import io
from app.utils import *


@run_thread
def run(store,settings,image,vars):
	if settings['format'].startswith('pmi'):
		settings['format']='pmi'
	pth=Path(settings['path'])/Path(vars['filename']).name
	pth=pth.with_suffix('')
	pth=pth.with_suffix('.'+settings['format'])

	if settings['format']=='pmi':
		fp=to_pm(image,vars)
		with open(pth,'wb') as fl:
			fl.write(fp.read())
	else:
		image.save(pth,quality=90,optimize=True,exif=image.getexif(),icc_profile=vars.get('profile',None))
	msg='Saved\n'+str(pth.name)
	return None,None,msg