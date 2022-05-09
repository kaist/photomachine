from pathlib import Path
from PIL import Image,ImageEnhance,ImageOps
import time
import os
import sys
from app.utils import *




@run_thread
def run(store,settings,image,vars):
	c=Image.open(settings['path'])

	nsize=int(min(image.size)*int(settings['size'])/100)
	c=ImageOps.contain(c, (nsize,nsize), method=Image.ANTIALIAS)
	#c.thumbnail((nsize,nsize))
	pod =image
	alpha=c.split()[-1]
	a=ImageEnhance.Brightness(alpha).enhance(int(settings['opacity'])/100.0)
	c.putalpha(a)

	v=settings['anchor'].split(':')
	vx,vy=int(v[0]),int(v[1])
	ws=c.size
	os=pod.size

	indent=min(pod.size)*int(settings['indent'])/100.0
	if vx==0:
		x=indent
	elif vx==2:
		x=os[0]-ws[0]-indent
	elif vx==1:
		x=os[0]/2-ws[0]/2
	if vy==0:
		y=indent
	elif vy==2:
		y=os[1]-ws[1]-indent
	elif vy==1:
		y=os[1]/2-ws[1]/2			




	pod.paste(c,(int(x),int(y)),c)




	msg='Finish for\n'+Path(vars['filename']).name
	return pod,vars,msg