from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
import requests
import sys
import os
import cv2
import time 
import socket 

socket.setdefaulttimeout(1000)

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

def decode_fourcc(v):
  v = int(v)
  return "".join([chr((v >> 8 * i) & 0xFF) for i in range(4)])

def main(fil):
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    file_metadata = {'name': fil}
    media = MediaFileUpload(fil, mimetype='video/mp4')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    # print('File ID: %s' % file.get('id'))
    resp = requests.post('https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable',timeout = 1000)
    #print(resp.status)

if __name__ == '__main__':
    st = time.time()
    main(sys.argv[1])
    t = time.time() - st
    print("Time taken to upload =", t, "seconds")