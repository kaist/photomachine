from pathlib import Path
from PIL import Image,ImageOps
import time
import os
import sys
from app.utils import *
from PIL import Image



@run_thread
def run(store,settings,image,vars):
    if settings['exif_rotate']:
        image=ImageOps.exif_transpose(image)
    if settings['flip_h']:
        image=image.transpose(Image.FLIP_LEFT_RIGHT)
    if settings['flip_v']:
        image=image.transpose(Image.FLIP_TOP_BOTTOM)
    if settings['need_rotate']:
        r_a=[-90,90,180]
        if settings['if']==0:
            image=image.rotate(r_a[settings['rotate']],expand=True)
        if settings['if']==1 and image.size[0]<image.size[1]:
            image=image.rotate(r_a[settings['rotate']],expand=True)
        if settings['if']==2 and image.size[0]>image.size[1]:
            image=image.rotate(r_a[settings['rotate']],expand=True)                       
    msg='Done:\n'+Path(vars['filename']).name
    return image,vars,msg
