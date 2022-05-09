from tkinter import *
from tkinter.ttk import *
from pathlib import Path
from tkinter import filedialog
import win32print,win32api
import win32con,win32ui,win32gui
from tkinter import messagebox

class Plugin:
    def __init__(self):
        self.category='output'
        self.name=_('Print')
        self.need_config=True


    def start_config(self,frame,plug):
        self.frame=frame

        self.cur_path=Path(plug.path)
        self.all_printers=[]
        self.printer_settings=plug.settings.get('printer_settings',None)
        self.printer_var=StringVar()
        if plug.settings.get('printer',None):
            self.printer_var.set(plug.settings['printer'])
        else:
            printer = win32print.GetDefaultPrinterW()
            self.printer_var.set(printer) 

        self.printers_combo=Combobox(frame,textvariable=self.printer_var,state="readonly",width=30)
        self.printers_combo.grid(row=0,column=0,padx=5,pady=5)
        self.printers_combo.bind("<<ComboboxSelected>>", self.select_printer)
        printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1)
        for x in printers:
            self.all_printers.append(x[2])
        self.printers_combo['values']=self.all_printers
        self.f_image=PhotoImage(file=str(self.cur_path/'printer.png'))
        Button(frame,text=_('Printer settings'),command=self.printer_setup,image=self.f_image,compound='left').grid(row=0,column=1,padx=5,pady=5)

        self.contain_var=IntVar()
        self.contain_var.set(plug.settings.get('contain',0))
        Radiobutton(frame, text=_("Borderless (Part of the image may be cropped)"),variable=self.contain_var,value=0).grid(row=1,column=0,columnspan=2,padx=5,pady=5,sticky=W)
        Radiobutton(frame, text=_("With border (full image)"),variable=self.contain_var,value=1).grid(row=2,column=0,columnspan=2,padx=5,pady=5,sticky=W)
       

    def save_config(self):
        d={}
        d['printer']=self.printer_var.get()
        d['printer_settings']=self.printer_settings
        d['contain']=self.contain_var.get()
        return d

    def select_printer(self,event=None):
        pass

        #d=filedialog.askdirectory()
        #self.path_var.set(d)
        #self.sframe.focus_force()

    def printer_setup(self):
        printer=self.printer_var.get()
        PRINTER_DEFAULTS = {"DesiredAccess":win32print.PRINTER_ALL_ACCESS}
        try:
            handle = win32print.OpenPrinter(printer,PRINTER_DEFAULTS)
        except:
            messagebox.showerror(_('Error'), _('Access denied')+': '+printer)
            self.frame.focus_force()
            return
        info = win32print.GetPrinter(handle, 2)
        pDevModeObj = info["pDevMode"]
        if self.printer_settings and self.printer_settings['DeviceName']==printer:
            for k in self.printer_settings:
                try:
                    setattr(pDevModeObj,k,self.printer_settings[k])
                except AttributeError:
                    pass
                                
            info["pDevMode"]=pDevModeObj
            win32print.SetPrinter(handle,2,info,0)

        ret=win32print.DocumentProperties(self.frame.winfo_id(),handle,printer,pDevModeObj,pDevModeObj,5)
        if ret==2:return

        sets={}
        for n in dir(pDevModeObj):
            if type(getattr(pDevModeObj,n) ) is int or type(getattr(pDevModeObj,n) ) is str:
                sets[n]=getattr(pDevModeObj,n)
        self.printer_settings=sets




