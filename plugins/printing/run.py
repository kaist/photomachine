from pathlib import Path
import time
import os
import sys
from app.utils import *
import win32print,win32api
import win32con,win32ui,win32gui
from PIL import Image,ImageWin,ImageOps,ImageCms
import io

PHYSICALWIDTH = 110
PHYSICALHEIGHT = 111
HORZRES = 8
VERTRES = 10
LOGPIXELSX = 88
LOGPIXELSY = 90
PHYSICALOFFSETX = 112
PHYSICALOFFSETY = 113

def print_image(image,settings,vars):
    printer_settings=settings.get('printer_settings',None)
    printer=settings['printer']
    PRINTER_DEFAULTS = {"DesiredAccess":win32print.PRINTER_ALL_ACCESS}
    handle = win32print.OpenPrinter(printer,PRINTER_DEFAULTS)
    info = win32print.GetPrinter(handle, 2)
    pDevModeObj = info["pDevMode"]
    if printer_settings and printer_settings['DeviceName']==printer:
        for k in printer_settings:
            try:
                setattr(pDevModeObj,k,printer_settings[k])
            except AttributeError:
                pass                    
        info["pDevMode"]=pDevModeObj
        win32print.SetPrinter(handle,2,info,0)

    dc = win32gui.CreateDC("WINSPOOL", printer, pDevModeObj)
    hDC = win32ui.CreateDCFromHandle(dc)
    printer_size = hDC.GetDeviceCaps(PHYSICALWIDTH), hDC.GetDeviceCaps(PHYSICALHEIGHT)
    printable_area = hDC.GetDeviceCaps (HORZRES), hDC.GetDeviceCaps (VERTRES)
    printer_margins = hDC.GetDeviceCaps (PHYSICALOFFSETX), hDC.GetDeviceCaps (PHYSICALOFFSETY)

    profile = ImageCms.createProfile("sRGB")
    if vars.get('profile',None):
        icc_profile = ImageCms.ImageCmsProfile(io.BytesIO(vars['profile']))
        image = ImageCms.profileToProfile(
                                     image,
                                     inputProfile=icc_profile,
                                     outputProfile=profile,
                                     renderingIntent=0,
                                     outputMode='RGB'
                                    )
    hDC.StartDoc(vars['filename'])
    hDC.StartPage()
    p_orien='h' if printable_area[0]>printable_area[1] else 'v'
    doc_orien='h' if image.size[0]>image.size[1] else 'v'
    if p_orien!=doc_orien:
        image=image.rotate(90,expand=True)

    if int(settings['contain'])==0:
        image=ImageOps.fit(image,printable_area)
    else:
        image=ImageOps.pad(image,printable_area,color='white')
    dib = ImageWin.Dib(image)
    dib.draw(hDC.GetHandleOutput(),(0,0,printable_area[0],printable_area[1]))
    hDC.EndPage()
    hDC.EndDoc()
    hDC.DeleteDC()


def run(store,settings,message_q,output_q,self_id,self_q=None):
    while True:
        if not self_q.empty():
            image,vars=self_q.get()
            self_q.task_done()
            message=[self_id,'Printing: \n'+Path(vars['filename']).name]
            message_q.put(message)
            print_image(image,settings,vars)
            message=[self_id,'Done: \n'+Path(vars['filename']).name]
            message_q.put(message)

        time.sleep(0.01)