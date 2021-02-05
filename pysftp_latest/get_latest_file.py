import pysftp
import sys
import requests
from requests.auth import HTTPBasicAuth 
import json
import base64
import os

PATH = os.path.join( os.path.abspath(os.path.join(os.getcwd(), os.pardir)),'Downloaded_Files' )
with open(os.path.join( os.path.abspath(os.path.join(os.getcwd(), os.pardir)),'sftp_config.json' )) as f:
    CREDS = json.load(f)
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

HOST = CREDS["HOSTNAME"]
USER = CREDS["HOST_USERNAME"]
PASS = CREDS["HOST_PASS"]
URL = CREDS["INSTANCE_URL"]
LOCAL_FILE_PATH = None
latestfile = None
with pysftp.Connection(HOST, username=USER, password=PASS,cnopts=cnopts) as sftp:
    sftp.cwd(CREDS["SFTP_FILE_ADDR"])
    latest = 0
    for fileattr in sftp.listdir_attr():
        if fileattr.st_mtime > latest:
            latest = fileattr.st_mtime
            latestfile = fileattr.filename
    if latestfile is not None:
        LOCAL_FILE_PATH = f"{PATH}\\{latestfile}"
        sftp.get(latestfile, LOCAL_FILE_PATH)
json_send = {}
json_send["filename"] = latestfile[:-5]
json_send["data"] = base64.b64encode(open(LOCAL_FILE _PATH, 'rb').read()).decode('utf-8')
requests.post(URL, auth = HTTPBasicAuth(CREDS["MID_SERVER_USERNAME"],CREDS["MID_SERVER_PASSWORD"]) , data=json.dumps(json_send))
