from flask import Flask,request,make_response,Response

import config
import os
import uuid
from werkzeug.utils import secure_filename
import api
from flask_cors import *
import urllib
import math

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route("/",methods = ['GET'])
def check():
    return "i am run in %s" % config.server()['host']

@app.route("/upload",methods=['POST'])
def face_save():   
    f = request.files['imgfile']
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
    print(request.files)
    api.faces_append
    return 'file uploaded sucessfully'

@app.route("/image",methods=['GET'])
def sendimage():
    img_name = request.args.get('uuid') + '.jpg'
    img_local = os.path.join(app.config['UPLOAD_FOLDER'],img_name)
    img_file = open(img_local,"rb")
    res = make_response(img_file.read())
    res.headers['Content-Type'] = 'image/jpg'
    img_file.close()
    return res

@app.route("/findface",methods=['POST'])
def find_face():
    f = request.files['imgfile']
    path = os.path.join(app.config['UPLOAD_FOLDER'], uuid.uuid1().__str__()[0:9] + secure_filename(f.filename))
    f.save(path)
    produce_file_uuid = api.find_faces_in_image(path)
    if type(config.server()['domain']) != str:
        src_url = 'http://' + str(config.server()['ip']) + ':' + str(config.server()['port']) + '/image?uuid=' + produce_file_uuid
    else:
        src_url = 'http://' + str(config.server()['domain']) + '/image?uuid=' + produce_file_uuid
    return src_url

@app.route('/webvideo')
def web_video():
    url = request.args.get('url')
    url = urllib.parse.unquote(url)
    # url = "http://192.168.0.252:8081/video"
    isOpenFAS = request.args.get('isopenfas')
    if isOpenFAS == '1':
        isOpenFAS = True
    else:
        isOpenFAS = False
    print(url)
    return Response(api.find_faces_in_web_video(url,FAS = isOpenFAS),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/compare",methods=['POST'])
def compare():
    img1 = request.files['img1']
    img2 = request.files['img2']
    img1_path = os.path.join(app.config['UPLOAD_FOLDER'], uuid.uuid1().__str__()[0:9] + secure_filename(img1.filename))
    img2_path = os.path.join(app.config['UPLOAD_FOLDER'], uuid.uuid1().__str__()[0:9] + secure_filename(img2.filename))
    img1.save(img1_path)
    img2.save(img2_path)
    data =  api.compare_two_faces(img1_path,img2_path)
    if data == '_error_':
        return {'is_same':False,'score':-1}  
    return data

@app.route("/slice",methods=['POST'])
def slice():
    img = request.files['img']
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], uuid.uuid1().__str__()[0:9] + secure_filename(img.filename))
    img.save(img_path)
    data = api.slice_face(img_path)
    if type(config.server()['domain']) != str:
        src_url = 'http://' + str(config.server()['ip']) + ':' + str(config.server()['port']) + '/image?uuid=' + data
    else:
        src_url = 'http://' + str(config.server()['domain']) + '/image?uuid=' + data
    return src_url

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = config.upload()
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.run(config.server()['host'],
            config.server()['port'],
            config.server()['debug'],
            True)

