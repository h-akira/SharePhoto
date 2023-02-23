#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: 2023-02-22 18:11:41

import os
import json
import requests
import mimetypes
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.appendonly','https://www.googleapis.com/auth/photoslibrary']

def get_creds(token_json='token.json',credentials_json='credentials.json'):
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists(token_json):
    creds = Credentials.from_authorized_user_file(token_json, SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(credentials_json, SCOPES)
      creds = flow.run_local_server(port=0)
    # Save the credentials for tahe next run
    with open(token_json, 'w') as token:
      token.write(creds.to_json())    
  return creds

def parse_args():
  import argparse
  parser = argparse.ArgumentParser(description="""\
Upload Image to GooglePhoto by API.
""", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("-t", "--token", metavar="path", default="token.json", help="token.json")
  parser.add_argument("-c", "--credentials", metavar="path", default="credentials.json", help="credentials.json（client_secret_hogehoge.json）")
  parser.add_argument("-d", "--description", metavar="text", help="description of item")
  parser.add_argument("-r", "--response", action="store_true", help="display response")
  parser.add_argument("-l", "--log", metavar="path", help="log file")
  parser.add_argument("files", metavar="input-file", nargs="*", help="input files")
  options = parser.parse_args()
  return options

def main():
  options = parse_args()
  if options.log:
    if os.path.isfile(options.log):
      with open(options.log,mode="r") as f:
        log = f.read()[:-1].split("\n")
    else:
      with open(options.log,mode="w") as f:
        f.write("")
      log = []
  creds = get_creds(options.token,options.credentials)
  with open(options.token, mode="r") as f:
    token = json.load(f)
  for file in options.files:
    MIMEtype = mimetypes.guess_type(file)[0]
    if MIMEtype == None:
      continue
    if MIMEtype.split("/")[0] not in ["video","image"]:
      continue
    if options.log:
      if os.path.basename(file) in log:
        continue
    URL = "https://photoslibrary.googleapis.com/v1/uploads"
    with open(file, mode='rb') as f:
      binary = f.read()
    headers = {
      'Authorization': f'Bearer {token["token"]}',
      "X-Goog-Upload-File-Name": os.path.basename(file),
      "X-Goog-Upload-Content-Type": MIMEtype,
      "Content-type": "application/octet-stream",
      "X-Goog-Upload-Protocol": "raw"
    }
    res = requests.post(URL,data=binary, headers=headers)
    if res.status_code!=200:
      print("Failed to get upload-token")
      continue
    ACCESS_TOKEN = res.text
    URL = "https://photoslibrary.googleapis.com/v1/mediaItems:batchCreate"
    headers = {'Authorization': f'Bearer {token["token"]}',
      "Content-type": "application/json",
      "X-Goog-Upload-Protocol": "raw"
      }
    JSON = {
      "newMediaItems": [
        {
          "simpleMediaItem": {
            "fileName": os.path.basename(file),
            "uploadToken": ACCESS_TOKEN
          }
        }
      ]
    }
    if options.description!=None:
      JSON["newMediaItems"][0]["description"]=options.description
    res = requests.post(URL,headers=headers, data=json.dumps(JSON))
    if options.response:
      print(res.text)
    dic = json.loads(res.text)
    if dic["newMediaItemResults"][0]["status"]["message"]=="Success":
      print(f'Successed to upload \"{dic["newMediaItemResults"][0]["mediaItem"]["filename"]}\"')
      if options.log:
        with open(options.log,mode="a") as f:
          print(os.path.basename(file),file=f)
    else:
      print(f"Failed to upload \"{os.path.basename(file)}\"")

if __name__ == '__main__':
  main()
