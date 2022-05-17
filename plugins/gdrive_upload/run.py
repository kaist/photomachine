from pathlib import Path
from PIL import Image
import time
import os
import sys
from app.utils import *
import requests
import io
import json

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaIoBaseUpload
import base64

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

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


def parse_url(url):
    u=url.split('/')[-1]
    if '?' in u:
        u=u.split('?')[0]
    return u




@run_thread
@retry_on_error
def run(store,settings,image,vars):
    image.thumbnail((7500,7500))

    fp=io.BytesIO()
    image.save(fp,format="jpeg",exif=image.getexif(),icc_profile=vars.get('profile',None),quality=80,optimize=True)
    fp.seek(0)
    tkn=pickle.loads(base64.b64decode(settings['creds']))
    creds = get_creds(Path('plugins/gdrive_upload')/Path('oauth-credentials.json'),user_token=tkn)
    drive_service = build('drive', 'v3', credentials=creds)
    shared_drive_id =parse_url(settings['album'])
    file_metadata = {
        'name': str(Path(vars['filename']).name),
        'mimeType': 'image/jpeg',
        'parents': [shared_drive_id]}
    media = MediaIoBaseUpload(fp, mimetype='image/jpeg')
    f = drive_service.files().create(
        body=file_metadata, media_body=media, supportsAllDrives=True).execute()





    msg='Sent to GDrive:\n'+str(Path(vars['filename']).name)
    return None,None,msg