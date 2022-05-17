from tkinter import *
from tkinter.ttk import *
from pathlib import Path
from tkinter import filedialog
import base64

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload


SCOPES = ['https://www.googleapis.com/auth/drive']

credentials_json = 'oauth-credentials.json'
credentials_pickle = 'token.pickle'

def get_creds(adm_token,user_token):
    creds = None
    # Obtain OAuth token / user authorization.
    if user_token:
        creds = user_token
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                adm_token, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
    return creds

class Plugin:
    def __init__(self):
        self.category='output'
        self.name=_('To GoogleDrive')
        self.need_config=True
        self.user_creds=None


    def start_config(self,frame,plug):
        self.new_creds=False
        self.sets=plug.settings
        self.cur_path=Path(plug.path)

        self.a_label=Label(frame,text=_('To use the plugin, log in to google drive'),wraplength=400)
        self.a_label.grid(row=0,column=0,padx=5,pady=5,sticky=W,columnspan=2)
        self.f_image=PhotoImage(file=str(self.cur_path/'gdrive.png'))
        self.b_button=Button(frame,text=_('Authorize'),image=self.f_image,command=self.open_auth,compound='left')
        self.b_button.grid(row=1,column=0,columnspan=2,padx=5,pady=10)


        self.ok_label=Label(frame,text=_('You are logged in to GoogleDrive'))


        
        Label(frame,text=_('Link to folder')).grid(row=3,column=0,padx=5,pady=5,sticky=W)
        self.album_var=StringVar()
        self.album_var.set(plug.settings.get('album',''))
        Entry(frame,width=40,textvariable=self.album_var).grid(row=3,column=1,padx=5,pady=5,sticky=E)

        if plug.settings['creds']:
            self.ok_label.grid(row=2,column=0,padx=5,pady=10,sticky=EW,columnspan=2)
            self.a_label.grid_forget()
            self.b_button.grid_forget()           




 
    def open_auth(self):
        creds=get_creds(self.cur_path/Path('oauth-credentials.json'),user_token=None)
        if creds:
            self.user_creds=creds
            self.ok_label.grid(row=2,column=0,padx=5,pady=10,sticky=EW,columnspan=2)
            self.a_label.grid_forget()
            self.b_button.grid_forget()
            self.new_creds=True

    def save_config(self):

        return {
            'album': self.album_var.get(),
            'creds':base64.b64encode(pickle.dumps(self.user_creds)).decode() if self.new_creds else self.sets['creds']
               }







