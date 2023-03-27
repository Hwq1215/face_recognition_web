import yaml as yaml
import os
import uuid
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

default_FacesPath = "./faces"

default_staticPath = "./static"

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
        default_FacesPath = data['FacesPath']
    if os.path.exists(default_FacesPath) == False:
        os.mkdir(default_FacesPath)
    return default_FacesPath

def staticPath():
    if data['staticPath'] is not None:
        default_staticPath = data['staticPath']
    if os.path.exists(default_staticPath) == False:
        os.mkdir(default_staticPath)
    return data['staticPath']

def imgUrl(data):
    if type(server()['domain']) != str:
        src_url = 'http://' + str(server()['ip']) + ':' + str(server()['port']) + '/image?uuid=' + data + '&t=' + str(uuid.uuid1())[0:6]
    else:
        src_url = 'http://' + str(server()['domain']) + '/image?uuid=' + data + '&t=' + str(uuid.uuid1())[0:6]
    return src_url

def faceUrl(data):
    if type(server()['domain']) != str:
        src_url = 'http://' + str(server()['ip']) + ':' + str(server()['port']) + '/face?name=' + data + '&t=' + str(uuid.uuid1())[0:6]
    else:
        src_url = 'http://' + str(server()['domain']) + '/face?name=' + data + '&t=' + str(uuid.uuid1())[0:6]
    return src_url

if (__name__ == '__main__'):
    print(data)
    print(data['server'])