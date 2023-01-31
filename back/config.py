import yaml as yaml
import os
ConfigPath = "./application.yaml"
default_server = {
    "negotitate": "http",
    "ip": "127.0.0.1",
    "domain": None, 
    "host": "0.0.0.0",
    "port": 5006,
    "debug": False
}

default_upload = "./upload"

default_dataset = {
  "url": "localhost:3306/face_recongition?useUnicode=true&useSSL=false&characterEncoding=utf8&autoReconnect=true&failOverReadOnly=false",
  "host": "localhost",
  "username": "root",
  "password": None,
  "database": "face_recongition"
}

FacesPath = "./faces"
data = []

with open(ConfigPath,'r',encoding='utf-8') as f:
    data = yaml.load(f,Loader=yaml.FullLoader)

def server(): 
    if data['server'] is not None:
        default_server.update(data['server'])
    return default_server


def upload():
    if data['upload'] is not None:
        default_upload =  data['upload']
    # path is not exist
    if os.path.exists(default_upload) == False:
        os.mkdir(default_upload)
    return default_upload

def dbinfo():
    if data['dataset'] is not None:
        default_dataset.update(data['dataset'])
    return default_dataset

def npPath():
    return data['npPath']

def FAS_model_path():
    return data['FAS_model_path']

def FacesPath():
    if data['FacesPath'] is not None:
        FacesPath = data['FacesPath']
    if os.path.exists(FacesPath) == False:
        os.mkdir(FacesPath)
    return FacesPath

if (__name__ == '__main__'):
    print(data)
    print(data['server'])