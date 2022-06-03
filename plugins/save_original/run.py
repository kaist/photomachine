from pathlib import Path
from PIL import Image
import time
import os
import sys
import io
import shutil
from app.utils import *


@run_thread
def run(store,settings,image,vars):
	if 'is_renamed' in vars:
		pth=Path(settings['path'])/Path(vars['filename'])
	else:
		pth=Path(settings['path'])/Path(vars['filename']).name
		
	if not pth.parent.exists():
		pth.parent.mkdir()	

	if not ('original_filename' in vars):
		return None,None,'No original for:\n'+str(pth.name)
	try:shutil.copyfile(vars['original_filename'],pth)
	except:
		return None,None,'Copy error:\n'+str(pth.name)
	if settings['delete']:
		try:Path(vars['original_filename']).unlink()
		except:pass

	

	msg='Saved\n'+str(pth.name)
	return None,None,msg