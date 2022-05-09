from pathlib import Path
from PIL import Image
import time
import os
import sys
from app.utils import *




@run_thread
def run(store,settings,image,vars):
	image.thumbnail((settings['width'],settings['height']),Image.ANTIALIAS)
	msg='Finish for\n'+Path(vars['filename']).name
	return image,vars,msg