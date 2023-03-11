#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: 2023-02-22 18:11:41

import sys
import os
import json
import requests
import mimetypes
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.exceptions import RefreshError

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

def preprocessing(opitons):
  if options.state:
    if os.path.isfile(options.state):
      with open(options.state,mode="r") as f:
        state = f.read()[:-1]
        if state == "Running":
          print("It is not possible to execute more than one at the same time.")
          sys.exit()
        elif state == "Failed":
          print("It failed the last time it was run. please check.")
          print(f"After that, Please delete `{opitons.state}`")
          sys.exit()
        elif state == "Error":
          print("An error occurred during the previous execution. please check.")
          print(f"After that, Please delete `{opitons.state}`")
          sys.exit()
        elif state == "Expired":
          print("`token.json` is invalid. Please delete and reacquire.")
          print(f"After that, Please delete `{options.state}`")
          sys.exit()
    with open(options.state,mode="w") as f:
      print("Running",file=f)

def postprocessiong(options, success=True, error=False, token=False):
  if options.state:
    if error:
      with open(options.state,mode="w") as f:
        if token:
          print("Expired",file=f)
          print("`token.json` is invalid. Please delete and reacquire.")
          print(f"After that, Please delete `{options.state}`")
        else:
          print("Error",file=f)
    else:
      with open(options.state,mode="w") as f:
        if success:
          print("Updated",file=f)
        else:
          print("Failed",file=f)

def parse_args():
  import argparse
  parser = argparse.ArgumentParser(description="""\
Upload Image to GooglePhoto by API.
""", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("-t", "--token", metavar="path", default=os.path.join(os.path.dirname(__file__),"../secret/token.json"), help="token.json")
  parser.add_argument("-c", "--credentials", metavar="path", default=os.path.join(os.path.dirname(__file__),"../secret/credentials.json"), help="credentials.json（client_secret_hogehoge.json）")
  parser.add_argument("-d", "--description", metavar="text", help="description of item (all be the same)")
  parser.add_argument("-r", "--response", action="store_true", help="display response")
  # parser.add_argument("-l", "--log", metavar="path", default=os.path.join(os.path.dirname(__file__),"../secret/log.txt"), help="log-file (skip same file name)")
  parser.add_argument("-l", "--log", metavar="path", help="log-file (skip same file name)")
  # parser.add_argument("-s", "--state", metavar="path", default=os.path.join(os.path.dirname(__file__),"../secret/state.txt"), help="state-file (for i3blocks)")
  parser.add_argument("-s", "--state", metavar="path", help="state-file (for regular running)")
  parser.add_argument("--no-stdout", action="store_true", help="no stdout")
  parser.add_argument("files", metavar="input-file", nargs="*", help="input files")
  options = parser.parse_args()
  return options

def main(options):
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
  success=True
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
    if dic["newMediaItemResults"][0]["status"]["message"] in ["Success","OK"]:
      print(f'Successed to upload \"{os.path.basename(file)}\".')
      if options.log:
        with open(options.log,mode="a") as f:
          print(os.path.basename(file),file=f)
    else:
      print(f"Failed to upload \"{os.path.basename(file)}\".")
      success=False
  return success

if __name__ == '__main__':
  options = parse_args()
  if options.no_stdout:
    sys.stdout = open(os.devnull, 'w')
  try:
    preprocessing(options)
    success = main(options)
    postprocessiong(options, success=success)
  except RefreshError:
    postprocessiong(options, error=True, token=True)
  except SystemExit:
    pass
  except:
    postprocessiong(options, error=True)
    import traceback
    traceback.print_exc()

