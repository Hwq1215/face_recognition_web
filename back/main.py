from flask import Flask,request,make_response,Response

import config
import os
import uuid
from werkzeug.utils import secure_filename
import alg_api as api
from flask_cors import *
import urllib
from flask_siwadoc import SiwaDoc
import manage_api
import json

app = Flask(__name__)
siwa = SiwaDoc(app)

CORS(app, supports_credentials=True)

@app.route("/",methods = ['GET'])
def check():
    return "i am run in %s" % config.server()['host']

@app.route("/upload",methods=['POST'])
@siwa.doc()
def face_save():   
    f = request.files['imgfile']
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
    print(request.files)
    api.faces_append
    return 'file uploaded sucessfully'

@app.route("/image",methods=['GET'])
@siwa.doc()
def sendimage():
    img_name = request.args.get('uuid') + '.png'
    img_local = os.path.join(app.config['UPLOAD_FOLDER'],img_name)
    img_file = open(img_local,"rb")
    res = make_response(img_file.read())
    res.headers['Content-Type'] = 'image/png'
    img_file.close()
    return res

@app.route("/face",methods=['GET'])
@siwa.doc()
def sendfaceimage():
    img_name = request.args.get('name')
    bytes = api.get_face(img_name)
    res = Response(bytes, mimetype='image/png') 
    return res

@app.route("/findface",methods=['POST'])
@siwa.doc()
def find_face():
    FAS = request.args.get('isopenfas') == "true"
    LANDMARKS = request.args.get('isopenlandmarks') == "true"
    f = request.files['imgfile']
    path = os.path.join(app.config['UPLOAD_FOLDER'], uuid.uuid1().__str__()[0:9] + secure_filename(f.filename))
    f.save(path)
    result = api.find_faces_in_image(path,FAS= FAS,LANDMARKS = LANDMARKS)
    return {
        "imgUrl":config.imgUrl(result['uuid_str']),
        "names":result['names']
    }

@app.route('/webvideo')
@siwa.doc()
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
@siwa.doc()
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
@siwa.doc()
def slice():
    img = request.files['img']
    key_point = request.form['keypoint']
    if key_point == 'true':
        key_point = True
    else:
        key_point = False
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], uuid.uuid1().__str__()[0:9] + secure_filename(img.filename))
    img.save(img_path)
    data = api.slice_face(img_path,key_point = key_point)
    return config.imgUrl(data)

@app.route("/manage/add",methods=['POST'])
def manageUpload():
    user_name = request.form['name']
    f = request.files['imgfile']
    imgPath = os.path.join(app.config['UPLOAD_FOLDER'], uuid.uuid1().__str__()[0:9] + secure_filename(f.filename))
    f.save(imgPath)
    face_id = manage_api.get_faces_maxid() + 1
    message = api.register_face(imgPath,face_id,user_name)
    if(message[0] == "success"):
        manage_api.insert_face(manage_api.factoryFace(
        face_id = face_id,
        user_name = user_name,
        img_name = message[1]
        ))
    return str(message[0])
    
@app.route("/manage/update",methods=['POST'])
def manageUpdate():
    user_name = request.form['name']
    face_id = request.form['faceId']
    f = request.files['imgfile']
    imgPath = os.path.join(app.config['UPLOAD_FOLDER'], uuid.uuid1().__str__()[0:9] + secure_filename(f.filename))
    f.save(imgPath)
    api.delete_face(face_id)
    message = api.register_face(imgPath,face_id,user_name)
    if(message[0] == "success"):
        manage_api.update_face(manage_api.factoryFace(
        face_id = face_id,
        user_name = user_name,
        img_name = message[1]
        ))
    return str(message[0])

@app.route("/manage/get",methods=['GET'])
def manageGet():
    face_infos = manage_api.get_faces_by_page(request.args.get('page'),request.args.get('pageSize'))
    for face_info in face_infos:
        face_info['imgSrc'] = config.faceUrl(face_info['imgSrc'])
    return json.dumps(face_infos)

@app.route("/manage/total",methods=['GET'])
def manageTotal():
    return str(manage_api.get_faces_num())

@app.route("/manage/delete",methods=['GET'])
def manageDelete():
    try:
        face_id = request.args.get('faceId')
        api.delete_face(face_id)
        manage_api.delete_face(face_id)        
    except:
        return {"msg":"error"}
    return {"msg":"success"}

# def manage():
#     return 
if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = config.upload()
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    # api.move_files(config.FacesPath(),config.upload())
    app.run(config.server()['host'],
            config.server()['port'],
            config.server()['debug'],
            True)
    

