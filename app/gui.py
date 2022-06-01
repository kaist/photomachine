import uuid
import os
import ctypes as ct
import configparser
import locale
import builtins
import io
from pathlib import Path
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import messagebox
from tkhtmlview import HTMLScrolledText
import webbrowser
from tkinter.font import Font



class Icons:
    def __init__(self):
        self.icons={}

    def init_icons(self):
        for i in Path('app/icons').glob('*.png'):
            self.icons[i.stem]=PhotoImage(file=i)  
                
    def __getattr__(self,fname):

        return self.icons[fname]

icons=Icons()

def dark_title_bar(window):
    window.update()
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ct.windll.user32.GetParent
    hwnd = get_parent(window.winfo_id())
    rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
    value = 2
    value = ct.c_int(value)
    set_window_attribute(hwnd, rendering_policy, ct.byref(value),
                     ct.sizeof(value))



class Translation:
    def read_f(self,path):
        conf=configparser.ConfigParser()
        try:
            conf.read_file(open(Path(path) / f'{self.lang}.txt', encoding='utf-8'))
        except:return
        for x in conf['LANG']:
            self.trans[x]=conf['LANG'][x]

    def __init__(self):
        self.trans={}
        self.lang, enc = locale.getdefaultlocale()
        self.read_f('app/locale')
        for x in Path('plugins').glob('*'):
            self.read_f(x/'locale')
        builtins.__dict__['_'] = self.translate


    def translate(self,word):
        return self.trans.get(word.lower(),word)

trans=Translation()

class PlugAction:
    def __init__(self,plugin=None):
        self.id=str(uuid.uuid4())
        self.x=400
        self.y=220
        if plugin:
            self.path=plugin.path
            self.name=plugin.name
        self.plugin=plugin
        
        self.outputs=[]
        self.settings={}


















class Gui:
    def __init__(self,root):
        self.root=root
        self.root.option_add("*tearOff", False)

        style = Style(self.root)
        self.root.tk.call('source', 'app/theme/forest-dark.tcl')
        style.theme_use("forest-dark")

 


        dark_title_bar(self.root)
        self.root.tk.call('wm', 'iconphoto', self.root._w, PhotoImage(file='app/icons/stream.png'))
        self.root.state('zoomed')
        self.root.title('PhotoMachine')
        scale=self.root.winfo_fpixels('1i')/72
        self.root.tk.call('tk', 'scaling', scale)

        self.root.configure(background='black')
        self.root.update_idletasks()




        icons.init_icons()
        self.app=None
        self.new_line=False

        self.top_frame=Frame(self.root)
        self.top_frame.pack(side=TOP,fill=X)

        self.session_frame=Labelframe(self.top_frame,text=_('Sessions'))
        self.session_frame.pack(padx=5,pady=5,side=LEFT)

        Button(self.session_frame,command=self.new_state,width=1,image=icons.new,compound='left').pack(side=LEFT,padx=5,pady=5)
        Button(self.session_frame,text=_('Save'),command=self.save_state,image=icons.save,compound='left').pack(side=LEFT,padx=5,pady=5)
        Button(self.session_frame,text=_('Save As...'),command=self.save_as_state,image=icons.save_as,compound='left').pack(side=LEFT,padx=5,pady=5)        
        Button(self.session_frame,text=_('Open'),command=self.load_state,image=icons.open_file,compound='left').pack(side=LEFT,padx=5,pady=5)  

        misc_frame=Labelframe(self.top_frame,text=_('Photomachine'))
        misc_frame.pack(padx=50,pady=5,side=LEFT)
        self.ps_label=Label(misc_frame,wraplength=200)
        self.ps_label.pack(side=LEFT,padx=5,pady=5)

        Button(misc_frame,image=icons.settings,width=1,compound='left',command=self.config_action).pack(side=LEFT,padx=5,pady=5)
        Button(misc_frame,image=icons.help,width=1,compound='left',command=self.about_plugin).pack(side=LEFT,padx=5,pady=5)        
        Button(misc_frame,image=icons.machine,width=12,text=_('About'),compound='left',command=self.about_photomachine).pack(side=LEFT,padx=5,pady=5)   

        act_frame=Labelframe(self.top_frame,text=_('Run')) 
        self.start_but=Button(act_frame,text=_('Start'),image=icons.play,compound='left',width=7,command=self.startstop)
        self.start_but.pack(side=RIGHT,padx=5,pady=5)
        act_frame.pack(padx=5,pady=5,side=RIGHT)




        self.nb=Notebook(self.root)
        self.nb.pack(padx=5,pady=5,side=BOTTOM,fill=X)
        self.plugs_frame=Frame(self.nb)
        self.plugs_frame.pack(padx=0,pady=0,fill=X)

        self.nb.add(self.plugs_frame,text=_('Actions'))

        self.plugs_filt_frame=Frame(self.plugs_frame)
        self.plugs_filt_frame.pack(side=TOP,fill=X)

        self.filt_var=IntVar()
        self.filt_var.set(0)
        self.filt_var.trace('w',self.change_filter)

        Radiobutton(self.plugs_filt_frame,text=_("All"),variable=self.filt_var,value=0).pack(side=LEFT,padx=5,pady=5)
        Radiobutton(self.plugs_filt_frame,text=_("Input"),variable=self.filt_var,value=1).pack(side=LEFT,padx=5,pady=5)
        Radiobutton(self.plugs_filt_frame,text=_("Process"),variable=self.filt_var,value=2).pack(side=LEFT,padx=5,pady=5)
        Radiobutton(self.plugs_filt_frame,text=_("Output"),variable=self.filt_var,value=3).pack(side=LEFT,padx=5,pady=5)


        self.hscr = Scrollbar(self.plugs_frame, orient = 'horizontal')
        self.hscr.pack(side = BOTTOM, fill = X)

        self.plugs_list=Canvas(self.plugs_frame,xscrollcommand=self.hscr.set)
        self.plugs_list.pack(side=TOP,fill=X,padx=5,pady=5)
        self.hscr.config(command=self.plugs_list.xview)
        self.bind_tree(self.plugs_frame,"<MouseWheel>", self.plugs_scroll)

        self.fav_frame=Frame(self.nb)
        self.fav_frame.pack(padx=0,pady=0,side=TOP,fill=X)

        self.plugs_filt_frame2=Frame(self.fav_frame)
        self.plugs_filt_frame2.pack(side=TOP,fill=X)
        self.f_filt_var=IntVar()
        self.f_filt_var.set(0)
        self.f_filt_var.trace('w',self.change_filter_favor)

        Radiobutton(self.plugs_filt_frame2,text=_("All"),variable=self.f_filt_var,value=0).pack(side=LEFT,padx=5,pady=5)
        Radiobutton(self.plugs_filt_frame2,text=_("Input"),variable=self.f_filt_var,value=1).pack(side=LEFT,padx=5,pady=5)
        Radiobutton(self.plugs_filt_frame2,text=_("Process"),variable=self.f_filt_var,value=2).pack(side=LEFT,padx=5,pady=5)
        Radiobutton(self.plugs_filt_frame2,text=_("Output"),variable=self.f_filt_var,value=3).pack(side=LEFT,padx=5,pady=5)


        self.fhscr = Scrollbar(self.fav_frame, orient = 'horizontal')
        self.fhscr.pack(side = BOTTOM, fill = X)

        self.f_plugs_list=Canvas(self.fav_frame,xscrollcommand=self.fhscr.set,height=50)
        self.f_plugs_list.pack(side=TOP,fill=X,padx=5,pady=5)
        self.fhscr.config(command=self.f_plugs_list.xview)
        self.bind_tree(self.fav_frame,"<MouseWheel>", self.plugs_scroll2)



        self.nb.add(self.fav_frame,text=_('Favorites'))





        self.canvas_frame=Frame(self.root)
        self.canvas_frame.pack(fill=BOTH,expand=True)  

        self.main_canvas=Canvas(self.canvas_frame,width=1000,height=1000,scrollregion=(0,0,1000,1000))
        self.main_canvas.configure(bg='#121212')
        

        self.hbar=Scrollbar(self.canvas_frame,orient=HORIZONTAL)
        self.hbar.pack(side=BOTTOM,fill=X)
        self.hbar.config(command=self.main_canvas.xview)

        self.vbar=Scrollbar(self.canvas_frame,orient=VERTICAL)
        self.vbar.pack(side=RIGHT,fill=Y)
        self.vbar.config(command=self.main_canvas.yview)

        self.main_canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        self.main_canvas.pack(side=LEFT,expand=True,fill=BOTH)






        self.main_canvas.bind('<B1-Motion>',self.canv_motion)
        self.main_canvas.bind('<ButtonRelease-1>',self.canv_release)        
        self.main_canvas.pack()

        self.main_canvas.bind("<MouseWheel>", self.canvas_scroll)

        

        root.after(1000,self.upd_canv)



        self.root.after(100,self.update_ps)
        self.root.after(2500,self.dis_splash)
  

    def update_pstext(self,cpu,mem):
        self.ps_label['text']=f'CPU load:{cpu:3}%\nMemory :{mem:3} MB'


    def dis_splash(self,event=None):
        try:
            import pyi_splash
            pyi_splash.close()
        except:pass

    def bind_tree(self,widget, event, callback):
        "Binds an event to a widget and all its descendants."

        widget.bind(event, callback)

        for child in widget.children.values():
            self.bind_tree(child, event, callback)


    def canvas_scroll(self,event):
        self.main_canvas.yview("scroll",-event.delta,"units")
        return "break" 


    def plugs_scroll(self,event):
        self.plugs_list.xview("scroll",-event.delta,"units")
        return "break" 

    def plugs_scroll2(self,event):
        self.f_plugs_list.xview("scroll",-event.delta,"units")
        return "break" 

    def upd_canv(self,event=None):
        x=self.canvas_frame.winfo_width()
        y=self.canvas_frame.winfo_height()
        if x<800:return
        self.main_canvas.configure(width=x-100,height=y-100,scrollregion=(0,0,x-100,y-100))


    def update_ps(self,event=None):
        self.app.update_ps()
        self.root.after(1000,self.update_ps)


    def center_window(self,win):
        win.resizable(0,0)
        win.attributes('-toolwindow', True)
        win.transient(self.root)

        """
        centers a tkinter window
        :param win: the main window or Toplevel window to center
        """
        win.update_idletasks()
        width = win.winfo_width()
        frm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 2 * frm_width
        height = win.winfo_height()
        titlebar_height = win.winfo_rooty() - win.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = win.winfo_screenwidth() // 2 - win_width // 2
        y = win.winfo_screenheight() // 2 - win_height // 2
        win.geometry(f'+{x}+{y}')
        #win.deiconify()


    def about_photomachine(self):
        win=Toplevel(self.root)
        win.geometry('650x600')
        scale=self.root.winfo_fpixels('1i')/72
        win.tk.call('tk', 'scaling', scale)
        self.center_window(win)

        dark_title_bar(win)
        win.title(_('PhotoMachine'))
        win.tk.call('wm', 'iconphoto', win._w, PhotoImage(file='app/icons/stream.png'))
        win.focus_force()

        fr=Frame(win)
        fr.pack(side=TOP,padx=5,pady=5,fill=BOTH,expand=True)
        self.splash_img=PhotoImage(file='app/icons/splash.png')
        Label(fr,image=self.splash_img).grid(row=0,column=0,columnspan=3)
        Label(fr,text=_('Version')+': '+os.environ['VERSION']).grid(row=1,column=0,padx=5,pady=5,sticky=W)
        Label(fr,text=_('Author')+': '+_('Igor Zalomskij'),anchor=CENTER).grid(row=1,column=1,padx=5,pady=5,sticky=W)
        Label(fr,text=_('Loaded plugins')+': '+str(len(self.app.plugins)),anchor=E).grid(row=1,column=2,padx=5,pady=5,sticky=W)

        Button(fr,text=_('Official site'),image=icons.machine,compound=TOP,command=lambda:webbrowser.open('https://photo-machine.ru')).grid(row=2,column=0,padx=5,pady=15,sticky=EW)     
        Button(fr,text=_('VK Group'),image=icons.vk,compound=TOP,command=lambda:webbrowser.open('https://vk.com/machine_app')).grid(row=2,column=1,padx=5,pady=15,sticky=EW)  
        Button(fr,text=_('Donate project!'),image=icons.donate,compound=TOP,command=lambda:webbrowser.open('https://photo-machine.ru/donate')).grid(row=2,column=2,padx=5,pady=15,sticky=EW) 

        Button(win,text=_('Ok'),image=icons.done,compound='left',command=lambda:win.destroy()).pack(side=BOTTOM,padx=5,pady=5,fill=X)
        #h=HTMLScrolledText(win,html='')
        #h.pack(side=TOP,padx=5,pady=5,fill=BOTH,expand=True)       

    def about_plugin(self,plug=None):
        p = Path(plug.path) if plug else Path('app')
        lang, enc = locale.getdefaultlocale()
        try:
            html = io.open(
                p / Path('locale') / f'{lang}_info.html',
                mode="r",
                encoding="utf-8",
            ).read()

        except:
            try:
                html=io.open(p/Path('locale')/('info.html'),mode="r", encoding="utf-8").read()
            except:
                html=_('This plugin has no help')
        win=Toplevel(self.root)
        win.geometry('900x600')
        scale=self.root.winfo_fpixels('1i')/72
        win.tk.call('tk', 'scaling', scale)
        self.center_window(win)

        dark_title_bar(win)
        if plug:
            win.title(f'{plug.name} ' + _('help'))
            win.tk.call(
                'wm',
                'iconphoto',
                win._w,
                PhotoImage(file=f'{str(plug.path)}/icon.png'),
            )

        else:
            win.title(_('PhotoMachine')+' '+_('help'))
            win.tk.call('wm', 'iconphoto', win._w, PhotoImage(file='app/icons/stream.png'))
        win.focus_force()
        Button(win,text=_('Ok'),image=icons.done,compound='left',command=lambda:win.destroy()).pack(side=BOTTOM,padx=5,pady=5,fill=X)
        h=HTMLScrolledText(win,html=html)
        h.pack(side=TOP,padx=5,pady=5,fill=BOTH,expand=True)


        



    def change_filter(self,var,index,mode):
        self.init_plugins_gui()


    def change_filter_favor(self,var,index,mode):
        self.init_favorites_gui()



    def init_favorites_gui(self):
        label = Label(self.root, text="")
        fnt =Font(font=label['font'])
        filt=self.f_filt_var.get()
        self.f_plug_wingets=[]
        self.f_plug_canvas=[]
        self.f_plugs_list.delete('all')
        t_plugs=[]
        if filt==0:
            for x in self.app.favorites:
                pl=self.app.find_by_path(x[0])
                t_plugs.append((pl,x))
        else:
            d={1:'input',2:'process',3:'output'}
            for x in self.app.favorites:
                pl=self.app.find_by_path(x[0])
                if pl.category==d[filt]:
                    t_plugs.append((pl,x))

        self.f_plugs_list.config(width=len(t_plugs)*250,height=65,scrollregion=(0,0,len(t_plugs)*250,100))
        for n,p in enumerate(t_plugs):


            # plugin,sets=dt
            # self.frame=Frame(width=240,height=100,relief=SOLID)
            # self.frame.config()
            # self.icon=Label(self.frame,image=plugin.icon)
            # self.icon.grid(row=0,column=0,rowspan=2,padx=5,pady=5)
            # Label(self.frame,text=sets[2],image=icons.__getattr__(plugin.category),compound='left').grid(row=0,sticky=W,column=1,columnspan=2,padx=5,pady=3)
            # self.b_fr=Frame(self.frame)
            # self.b_fr.grid(row=1,column=1,sticky=EW)
            # self.button=Button(self.b_fr,text=_('Add'),width=8,image=icons.add,command=lambda: gui.add_plugin(plugin,sets=sets),compound='left')
            # self.button.pack(side=LEFT,padx=5,pady=3)

            # self.delete_button=Button(self.b_fr,width=0,image=icons.trash_action,command=lambda: gui.remove_favorite(sets),compound='left')
            # self.delete_button.pack(side=RIGHT,padx=5,pady=3)
            plug,sets=p


            #w=FavoriteWidget(self,plug)
            #self.f_plugs_list.create_window(n*250,0,window=w.frame,width=240,height=65,anchor=NW)

            self.f_plugs_list.create_rectangle(n*250+2,2,n*250+240,65,outline='black')
            self.f_plugs_list.create_image(n*250+7,16,image=plug.icon,anchor=NW)
            self.f_plugs_list.create_text(n*250+7+60,7,text=sets[2],anchor=NW,fill='white',font=fnt)
            self.f_plugs_list.create_image(n*250+7+40,7,image=icons.__getattr__(plug.category),anchor=NW)  

            self.f_plugs_list.create_rectangle(n*250+7+40,30,n*250+7+40+100,30+30,width=0,fill='#585858',tags=(f'addbind{n}','hl'))
            self.f_plugs_list.create_image(n*250+7+44+5,37,image=icons.add,anchor=NW,tag=f'addbind{n}') 
            self.f_plugs_list.create_text(n*250+7+65+5,37,text=_('Add'),anchor=NW,fill='white',font=fnt,tag=f'addbind{n}')

            self.f_plugs_list.create_rectangle(n*250+7+150,30,n*250+7+150+35,30+30,width=0,fill='#585858',tags=(f'infobind{n}','hl'))
            self.f_plugs_list.create_image(n*250+7+160,37,image=icons.trash_action,anchor=NW,tags=f'infobind{n}') 

            self.f_plugs_list.tag_bind(f'infobind{n}','<Button-1>',lambda event, s=sets : self.remove_favorite(s))

            self.f_plugs_list.tag_bind(f'addbind{n}','<Button-1>',lambda event, p=plug,s=sets : self.add_plugin(p,sets=s))            
            self.f_plugs_list.tag_bind(f'addbind{n}','<Enter>',self.curs_enter)  
            self.f_plugs_list.tag_bind(f'addbind{n}','<Leave>',self.curs_leave)  
            self.f_plugs_list.tag_bind(f'infobind{n}','<Enter>',self.curs_enter)  
            self.f_plugs_list.tag_bind(f'infobind{n}','<Leave>',self.curs_leave)  




    def remove_favorite(self,sets):
        msg= messagebox.askquestion(_('Remove?'),_('Remove from favorites?')+'\n'+sets[2],icon = 'warning')
        if msg != 'yes':return
        self.app.remove_favorite(sets)
        self.init_favorites_gui()


    def init_plugins_gui(self,event=None):
        label = Label(self.root, text="")
        fnt =Font(font=label['font'])
        
        filt=self.filt_var.get()
        self.plug_wingets=[]
        self.plug_canvas=[]
        self.plugs_list.delete('all')
        t_plugs=[]
        if filt==0:
            t_plugs=self.app.plugins
        else:
            d={1:'input',2:'process',3:'output'}
            for x in self.app.plugins:
                if x.category==d[filt]:
                    t_plugs.append(x)



        self.plugs_list.config(width=len(t_plugs)*250,height=65,scrollregion=(0,0,len(t_plugs)*250,100))
        for n,plug in enumerate(t_plugs):
            self.plugs_list.create_rectangle(n*250+2,2,n*250+240,65,outline='black')
            self.plugs_list.create_image(n*250+7,16,image=plug.icon,anchor=NW)
            self.plugs_list.create_text(n*250+7+60,7,text=plug.name,anchor=NW,fill='white',font=fnt)
            self.plugs_list.create_image(n*250+7+40,7,image=icons.__getattr__(plug.category),anchor=NW)  

            self.plugs_list.create_rectangle(n*250+7+40,30,n*250+7+40+100,30+30,width=0,fill='#585858',tags=(f'addbind{n}','hl'))
            self.plugs_list.create_image(n*250+7+44+5,37,image=icons.add,anchor=NW,tag=f'addbind{n}') 
            self.plugs_list.create_text(n*250+7+65+5,37,text=_('Add'),anchor=NW,fill='white',font=fnt,tag=f'addbind{n}')

            self.plugs_list.create_rectangle(n*250+7+150,30,n*250+7+150+35,30+30,width=0,fill='#585858',tags=(f'infobind{n}','hl'))
            self.plugs_list.create_image(n*250+7+160,37,image=icons.info,anchor=NW,tags=f'infobind{n}') 

            self.plugs_list.tag_bind(f'infobind{n}','<Button-1>',lambda event, p=plug : self.about_plugin(p))

            self.plugs_list.tag_bind(f'addbind{n}','<Button-1>',lambda event, p=plug : self.add_plugin(p))            
            self.plugs_list.tag_bind(f'addbind{n}','<Enter>',self.curs_enter)  
            self.plugs_list.tag_bind(f'addbind{n}','<Leave>',self.curs_leave)  
            self.plugs_list.tag_bind(f'infobind{n}','<Enter>',self.curs_enter)  
            self.plugs_list.tag_bind(f'infobind{n}','<Leave>',self.curs_leave)  

    def curs_enter(self,event):
        wid=event.widget
        x = wid.canvasx(event.x)
        y = wid.canvasy(event.y)
        obj=wid.find_closest(x,y)
        if 'hl' in wid.gettags(obj):
            wid.itemconfigure(obj,fill='#606060')
        self.root.config(cursor="hand2")

    def curs_leave(self,event):
        wid=event.widget
        x = wid.canvasx(event.x)
        y = wid.canvasy(event.y)
        obj=wid.find_closest(x,y)
        if 'hl' in wid.gettags(obj):
            wid.itemconfigure(obj,fill='#585858')
        self.root.config(cursor="arrow")


    def redraw_canvas(self):
        self.move_end()
        self.main_canvas.delete('all')
        for plug in self.app.plug_actions:
            self.add_plugin(plug,new=False)
        self.update_lines()
        



    def add_plugin(self,plugin,new=True,sets=False):
        label = Label(self.root, text="")
        fnt =Font(font=label['font'])
        if self.app.is_start:return
        if new:

            act=PlugAction(plugin)
            if not (act.settings) and (hasattr(act.plugin, 'default_config')):
                act.settings=act.plugin.default_config
            if sets:
                act.settings=sets[1]
                act.name=sets[2]
            tx=int(self.main_canvas['width'])/2
            ty=int(self.main_canvas['height'])/2

            while True:
                again=False
                for p in self.app.plug_actions:
                    if (p.x==tx) and (p.y==ty):
                        again=True
                        tx=tx+250
                        ty=ty+100
                if not again:break
            act.x=int(tx)
            act.y=int(ty)


            self.app.plug_actions.append(act)

        else:
            act=plugin


        if self.app.settings['vertical_nodes']:
            dx,dy=0,64/2
            dx1,dy1=125,0
        else:
            dx,dy=125,0
            dx1,dy1=0,65/2

        # self.main_canvas.create_window(
        #     win.x,
        #     win.y,
        #     window=win.frame,
        #     tags=(act.id, f'{str(act.id)}-wintag', 'wintag'),
        #     width=250,
        #     height=65,
        #     anchor=CENTER,
        # )

        # self.main_canvas.create_image(
        #     win.x - dx1,
        #     win.y - dy1,
        #     image=icons.drag if self.app.settings['vertical_nodes'] else icons.drag_h,
        #     tags=(act.id, f'{str(act.id)}-move', 'movetag'),
        #     anchor=CENTER,
        # )


        if act.plugin.category in ['process','output']:
            self.main_canvas.create_image(
                act.x - dx,
                act.y - dy,
                image=icons.input_icon,
                tags=(act.id, f'{str(act.id)}-output', 'inputtag'),
                anchor=CENTER,
            )


        if act.plugin.category in ['input','process']:
            self.main_canvas.create_image(
                act.x + dx,
                act.y + dy,
                image=icons.output_icon,
                tags=(act.id, f'{str(act.id)}-input', 'outputtag'),
                anchor=CENTER,
            )



        self.main_canvas.create_rectangle(act.x-125,act.y-33,act.x+125,act.y+33,outline='black',fill='#313131',tags=(act.id,f'{act.id}-wintag',f'{act.id}-main',f'{str(act.id)}-move', 'movetag'))
        self.main_canvas.create_image(act.x-125+7,act.y-33+16,image=act.plugin.icon,anchor=NW,tags=(act.id,f'{str(act.id)}-move', 'movetag'))

        self.main_canvas.create_text(act.x-125+7+60,act.y-33+7,text=act.name[:22],width=150,anchor=NW,fill='white',font=fnt,tags=(act.id,))
        self.main_canvas.create_image(act.x-125+7+40,act.y-33+7,image=icons.__getattr__(act.plugin.category),anchor=NW,tags=(act.id,))  


        self.main_canvas.create_image(act.x-125+7+215,act.y-33+7,image=icons.rename,anchor=NW,tags=(act.id,'btn',f'renamebind{act.id}','need-del') ) 


        self.main_canvas.create_text(act.x-125+7+40,act.y-33+30,text='',anchor=NW,fill='white',font=fnt,tags=(act.id,f'{act.id}-text'))

        if act.plugin.need_config:
            self.main_canvas.create_rectangle(act.x-125+7+40,act.y-33+30,act.x-125+7+40+100,act.y-33+30+30,width=0,fill='#585858',tags=(act.id,f'setsbind{act.id}','btn','need-del','hl'))
            self.main_canvas.create_image(act.x-125+7+44+5,act.y-33+37,image=icons.config_action,anchor=NW,tags=(act.id,f'setsbind{act.id}','btn','need-del'))
            self.main_canvas.create_text(act.x-125+7+65+5,act.y-33+37,text=_('Config'),anchor=NW,fill='white',font=fnt,tags=(act.id,f'setsbind{act.id}','btn','need-del'))
        else:
            self.main_canvas.create_rectangle(act.x-125+7+40,act.y-33+30,act.x-125+7+40+100,act.y-33+30+30,width=0,fill='#585858',stipple='gray25',tags=(act.id,'need-del'))
            self.main_canvas.create_image(act.x-125+7+44+5,act.y-33+37,image=icons.config_action,anchor=NW,tags=(act.id,'need-del'))
            self.main_canvas.create_text(act.x-125+7+65+5,act.y-33+37,text=_('Config'),anchor=NW,fill='white',font=fnt,tags=(act.id,'need-del'))           


        self.main_canvas.create_rectangle(act.x-125+7+150,act.y-33+30,act.x-125+7+150+35,act.y-33+30+30,width=0,fill='#585858',tags=(act.id,f'favbind{act.id}','btn','need-del','hl'))
        self.main_canvas.create_image(act.x-125+7+160,act.y-33+37,image=icons.favorite,anchor=NW,tags=(act.id,f'favbind{act.id}','btn','need-del'))

        self.main_canvas.create_rectangle(act.x-125+7+195,act.y-33+30,act.x-125+7+195+35,act.y-33+30+30,width=0,fill='#585858',tags=(act.id,f'delbind{act.id}','btn','need-del','hl'))
        self.main_canvas.create_image(act.x-125+7+205,act.y-33+37,image=icons.trash_action,anchor=NW,tags=(act.id,f'delbind{act.id}','btn','need-del'))        

        self.main_canvas.tag_bind(f'setsbind{act.id}','<Button-1>',lambda event, pid=act.id : self.config_action(pid))
        self.main_canvas.tag_bind(f'favbind{act.id}','<Button-1>',lambda event, pid=act.id : self.favorite_action(pid))  
        self.main_canvas.tag_bind(f'delbind{act.id}','<Button-1>',lambda event, pid=act.id : self.delete_action(pid))   

        self.main_canvas.tag_bind(f'renamebind{act.id}','<Button-1>',lambda event, pid=act.id : self.rename_action(act))  

        self.main_canvas.tag_bind('btn','<Enter>',self.curs_enter)  
        self.main_canvas.tag_bind('btn','<Leave>',self.curs_leave)  






        self.main_canvas.tag_bind('inputtag',"<Button-1>",self.line_start)
        self.main_canvas.tag_bind('outputtag',"<Button-1>",self.line_start)     


        self.main_canvas.tag_bind('movetag',"<Button-1>",self.move_click)
        self.main_canvas.tag_bind('movetag',"<B1-Motion>",self.move_motion)
        self.main_canvas.tag_bind('movetag',"<ButtonRelease-1>",self.move_end)        




        self.main_canvas.tag_bind(
            f'{str(act.id)}-move', "<Enter>", self.move_cursor_start
        )

        self.main_canvas.tag_bind(
            f'{str(act.id)}-move', "<Leave>", self.move_cursor_end
        )
           


        self.main_canvas.tag_bind(
            f'{str(act.id)}-input', "<Enter>", self.line_cursor_start
        )

        self.main_canvas.tag_bind(
            f'{str(act.id)}-input', "<Leave>", self.line_cursor_end
        )


        self.main_canvas.tag_bind(
            f'{str(act.id)}-output', "<Enter>", self.line_cursor_start
        )

        self.main_canvas.tag_bind(
            f'{str(act.id)}-output', "<Leave>", self.line_cursor_end
        )


        #self.main_canvas.tag_raise('movetag','wintag')




    def line_start(self,event):
        self.new_line=True
        tag=self.main_canvas.gettags(event.widget.find_withtag("current"))
        self.new_line_uid=tag[0]
        if 'inputtag' in tag:
            self.new_line_type='input'
        elif 'outputtag' in tag:
            self.new_line_type='output'

        c = event.widget
        x = c.canvasx(event.x)
        y = c.canvasy(event.y)
        self.temp_line_start=x,y
        self.temp_line=self.main_canvas.create_line(x,y,x,y,dash=(5,2),fill='#626567')


    def canv_motion(self,event):
        if self.new_line:
            c = event.widget
            x = c.canvasx(event.x)
            y = c.canvasy(event.y)
            self.main_canvas.coords(self.temp_line,self.temp_line_start[0],self.temp_line_start[1],x,y)
            self.root.config(cursor="tcross")
            obj=self.main_canvas.find_closest(x,y,halo=1)[0]
            tag=self.main_canvas.gettags(obj)


    def canv_release(self,event):
        if not self.new_line:
            return
        self.main_canvas.delete(self.temp_line)
        self.root.config(cursor="arrow")
        self.new_line=False
        c = event.widget
        x = c.canvasx(event.x)
        y = c.canvasy(event.y)
        #tag=self.main_canvas.gettags(event.widget.find_withtag("current"))
        obj=self.main_canvas.find_closest(x,y,halo=1)
        tag=self.main_canvas.gettags(obj)
        tp=None
        if tag and tag[0]!=self.new_line_uid:
            if 'inputtag' in tag:
                tp='input'
            elif 'outputtag' in tag:
                tp='output'
            if not tp:return

            if self.new_line_type!=tp:
                if self.new_line_type=='input':
                    self.app.connect(tag[0],self.new_line_uid)
                else:
                    self.app.connect(self.new_line_uid,tag[0])

            #self.main_canvas.coords(self.temp_line,self.temp_line_start[0],self.temp_line_start[1],event.x,event.y)
            #self.root.config(cursor="tcross")

    def move_cursor_start(self,event):
        self.root.config(cursor="fleur")

    def move_cursor_end(self,event):
        self.root.config(cursor="arrow")

    def line_cursor_start(self,event):
        self.root.config(cursor="tcross")

    def line_cursor_end(self,event):
        self.root.config(cursor="arrow")

    def move_click(self,event):
        self.last_x=event.x
        self.last_y=event.y

    def move_motion(self,event):
        tag=self.main_canvas.gettags(event.widget.find_withtag("current"))[0]
        self.main_canvas.move(tag,event.x-self.last_x,event.y-self.last_y)
        self.last_x=event.x
        self.last_y=event.y
        tgs = self.main_canvas.find_withtag(f'{tag}-main')
        c=self.main_canvas.coords(tgs)

        self.app.update_coords(tag,c[0]+125,c[1]+65/2)
        self.update_lines()

    def move_end(self,event=None):
        x=[]
        y=[]
        for p in self.app.plug_actions:
            x.append(p.x)
            y.append(p.y)
        if not(x):
            self.upd_canv()
            return
        self.main_canvas.configure(width=max(x)+300,height=max(y)+300,scrollregion=(0,0,max(x)+300,max(y)+300))


    def update_lines(self):
        self.main_canvas.delete('lines')
        for plug in self.app.plug_actions:
            from_uid=str(plug.id)
            for plug_to in plug.outputs:
                from_dot=self.main_canvas.coords(f'{from_uid}-main')
                if self.app.settings['vertical_nodes']:
                    print(from_dot)
                    from_dot=from_dot[0]+125,from_dot[1]+65
                else:
                    from_dot=from_dot[0]+250,from_dot[1]+65/2                   

                to_dot=self.main_canvas.coords(f'{plug_to}-main')
                if self.app.settings['vertical_nodes']:                
                    to_dot=to_dot[0]+125,to_dot[1]
                else:
                    to_dot=to_dot[0],to_dot[1]+65/2
                if self.app.settings['vertical_nodes']:
                    dx,dy=0,8
                else:
                    dx,dy=8,0

                self.main_canvas.create_line(from_dot[0]+dx,from_dot[1]+dy,to_dot[0]-dx,to_dot[1]-dy,tags=('lines',plug_to),width=1.5,fill='#626567')
                middle_x=from_dot[0]+(to_dot[0]-from_dot[0])/2
                middle_y=from_dot[1]+(to_dot[1]-from_dot[1])/2          

                self.main_canvas.create_image(
                    middle_x,
                    middle_y,
                    image=icons.delete_line,
                    tags=('lines', 'delete_line', f'{from_uid}:{plug_to}'),
                    anchor=CENTER,
                )

        self.main_canvas.tag_bind('delete_line',"<Enter>",self.delete_line_cursor_start)
        self.main_canvas.tag_bind('delete_line',"<Leave>",self.delete_line_cursor_end)
        self.main_canvas.tag_bind('delete_line',"<Button-1>",self.delete_line_action)   
            

    def delete_line_cursor_start(self,event):
        if self.app.is_start:return
        self.root.config(cursor="hand2")

    def delete_line_cursor_end(self,event):
        self.root.config(cursor="arrow")

    def delete_line_action(self,event):
        if self.app.is_start:
            return
        tag=self.main_canvas.gettags(event.widget.find_withtag("current"))
        self.root.config(cursor="arrow")
        self.app.disconnect(tag[-2].split(':'))

    def delete_action(self,uid):
        self.app.delete_action(uid)
        self.curs_leave(event=None)



    def new_update(self,resp):
        win=Toplevel(self.root)
        win.geometry('500x300')
        self.center_window(win)  
        dark_title_bar(win)
        win.title(_('New update is available'))
        win.tk.call('wm', 'iconphoto', win._w, PhotoImage(file='app/icons/stream.png'))
        win.focus_force()
        fr=Frame(win)
        fr.pack(side=BOTTOM,padx=5,pady=5,fill=X)
        Button(fr,text=_('Download update'),image=icons.download,compound='left',command=lambda:webbrowser.open('https://photo-machine.ru/download/')).pack(side=LEFT,padx=5,pady=5,fill=X)        
        Button(fr,text=_('Close'),image=icons.cancel,compound='left',command=lambda:win.destroy()).pack(side=RIGHT,padx=5,pady=5,fill=X)
        h=HTMLScrolledText(win,html=resp['changelog'])
        h.pack(side=TOP,padx=5,pady=5)


    def start_main_config(self,frame):
        Label(frame,wraplength=300,text=_('Maximum number of photos in the queue. The more, the more RAM a program can take up.')).grid(row=0,column=0,padx=5,pady=5,sticky=W)
        self.max_q_var=IntVar(value=self.app.settings['max_q'])
        Entry(frame,textvariable=self.max_q_var,width=10).grid(row=0,column=1,padx=5,pady=5,sticky=W)

        self.vert_nodes_var=IntVar(value=self.app.settings['vertical_nodes'])
        Radiobutton(frame,text=_('Connect nodes horizontal'),variable=self.vert_nodes_var,value=0).grid(row=1,column=0,padx=5,pady=5,columnspan=2,sticky=W)
        Radiobutton(frame,text=_('Connect nodes vertical'),variable=self.vert_nodes_var,value=1).grid(row=2,column=0,padx=5,pady=5,columnspan=2,sticky=W)


        self.check_updates_var=BooleanVar(value=self.app.settings['check_updates'])
        Checkbutton(frame,variable=self.check_updates_var,text=_('Check for updates automatically')).grid(row=3,column=0,columnspan=2,sticky=W)



        self.error_var=BooleanVar(value=self.app.settings['send_errors'])
        Checkbutton(frame,variable=self.error_var,text=_('Send error reports')).grid(row=4,column=0,columnspan=2,sticky=W)

    def save_main_config(self):
        d = {'max_q': int(self.max_q_var.get())}
        d['check_updates']=int(self.check_updates_var.get())
        d['send_errors']=int(self.error_var.get())
        d['vertical_nodes']=self.vert_nodes_var.get()

        return d


    def config_action(self,uid=None):
        plug=self.app.find_by_uid(uid)
        self.set_top_w=Toplevel(self.root)
        self.center_window(self.set_top_w)
        dark_title_bar(self.set_top_w)
        win=self.set_top_w

        if plug:
            win.title(f'{plug.plugin.name} ' + _('settings'))
            win.tk.call(
                'wm',
                'iconphoto',
                win._w,
                PhotoImage(file=f'{str(plug.path)}/icon.png'),
            )

            frame = Labelframe(win, text=f'{plug.plugin.name} ' + _('settings'))
        else:
            win.title(_('settings'))
            win.tk.call('wm', 'iconphoto', win._w, PhotoImage(file='app/icons/stream.png'))
            frame=Frame(win)
        win.focus_force()
        frame.pack(fill=X,padx=5,pady=5)
        actions=Frame(win)
        actions.pack(fill=X,padx=5,pady=5)
        Button(actions,text=_('Cancel'),image=icons.cancel,compound='left',command=self.cancel_settings).pack(side=RIGHT,padx=5,pady=5)
        Button(actions,text=_('Save'),image=icons.done,compound='left',command=lambda:self.save_config(uid)).pack(side=RIGHT,padx=5,pady=5)




        self.app.config_action(uid,frame)


    def rename_action(self,plugin):
        self.set_top_w=Toplevel(self.root)
        self.center_window(self.set_top_w)
        dark_title_bar(self.set_top_w)
        win=self.set_top_w
        win.title(_('Rename')+': '+plugin.name)
        win.tk.call(
            'wm',
            'iconphoto',
            win._w,
            PhotoImage(file=f'{str(plugin.path)}/icon.png'),
        )

        win.focus_force()
        frame=Labelframe(win,text=_('New name...'))
        frame.pack(fill=X,padx=5,pady=5)
        self.new_name_var=StringVar()
        self.new_name_var.set(plugin.name)
        e=Entry(frame,width=30,textvariable=self.new_name_var)
        e.pack(padx=5,pady=5)
        actions=Frame(win)
        actions.pack(fill=X,padx=5,pady=5)

        Button(actions,text=_('Cancel'),image=icons.cancel,compound='left',command=self.cancel_settings).pack(side=RIGHT,padx=5,pady=5)
        Button(actions,text=_('Save'),image=icons.done,compound='left',command=lambda:self.save_new_name(plugin)).pack(side=RIGHT,padx=5,pady=5)
        e.focus()
        e.icursor(END)

    def save_new_name(self,plugin):
        plugin.name=self.new_name_var.get()
        self.set_top_w.destroy()
        self.redraw_canvas()


    def favorite_action(self,uid):
        self.cur_favor_uid=uid
        plug=self.app.find_by_uid(uid)
        if not(plug.settings) and plug.plugin.need_config:
            messagebox.showerror(_('Config error'), _('Action not configured. Why add it to favorites?'))
            return
        self.set_top_w=Toplevel(self.root)
        self.center_window(self.set_top_w)
        dark_title_bar(self.set_top_w)
        win=self.set_top_w
        win.title(_('Add to favorite: ')+plug.plugin.name)
        win.tk.call(
            'wm',
            'iconphoto',
            win._w,
            PhotoImage(file=f'{str(plug.path)}/icon.png'),
        )

        win.focus_force()
        frame=Labelframe(win,text=_('Save As...'))
        frame.pack(fill=X,padx=5,pady=5)
        self.fav_name_var=StringVar()
        self.fav_name_var.set(plug.name)
        Entry(frame,width=30,textvariable=self.fav_name_var).pack(padx=5,pady=5)
        actions=Frame(win)
        actions.pack(fill=X,padx=5,pady=5)

        Button(actions,text=_('Cancel'),image=icons.cancel,compound='left',command=self.cancel_settings).pack(side=RIGHT,padx=5,pady=5)
        Button(actions,text=_('Save'),image=icons.done,compound='left',command=lambda:self.save_favorite(uid)).pack(side=RIGHT,padx=5,pady=5)

    def save_favorite(self,uid):
        self.app.save_favorite(uid,self.fav_name_var.get())
        self.set_top_w.destroy()        

    def save_config(self,uid):
        self.app.save_config(uid)
        self.set_top_w.destroy()

    def cancel_settings(self):
        self.set_top_w.destroy()

    def save_state(self):
        if not self.app.cur_filename:
            self.save_as_state()
            return
        self.app.save_state()

    def save_as_state(self):
        if d := filedialog.asksaveasfilename(
            defaultextension=".nodes", filetypes=[("PhotoMachine files", ".nodes")]
        ):
            self.app.save_state(filename=d)
    def new_state(self):
        if self.app.is_start:return
        self.app.new_state()




    def load_state(self):
        if self.app.is_start:return
        if d := filedialog.askopenfilename(
            defaultextension=".nodes", filetypes=[("PhotoMachine files", ".nodes")]
        ):
            self.app.load_state(d)


    def new_message(self,message):
        uid,msg=message
        self.main_canvas.itemconfigure(f'{uid}-text', text=msg)


    def update_count(self,uid,count):
        for plug in self.canv_runs:
            if uid==plug.plugin.id:
                plug.update_count(count)

    def startstop(self):
        if self.app.is_start:
            self.stop()
            self.start_but['text']=_('Start')
            self.start_but['image']=icons.play
        else:
            if not self.check_configs():return
            self.start()
            self.start_but['text']=_('Stop')
            self.start_but['image']=icons.stop          

    def start(self):

        self.main_canvas.delete('need-del')
        self.app.start()

    def stop(self):
        #self.redraw_canvas()
        self.app.stop()
        self.redraw_canvas()

    def check_configs(self):
        out_warn = [
            plug.plugin.name
            for plug in self.app.plug_actions
            if plug.plugin.need_config and not plug.settings
        ]

        if out_warn:messagebox.showerror(_('Config error'), _('These actions are not configured')+':\n'+'\n'.join(out_warn))

        return not(out_warn)

