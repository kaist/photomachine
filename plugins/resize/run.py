from pathlib import Path
from PIL import Image
from app.utils import run_thread

@run_thread
def run(store,settings,image,vars):
	image.thumbnail((settings['width'],settings['height']),Image.ANTIALIAS)
	return image,vars,'Finish for\n'+Path(vars['filename']).name