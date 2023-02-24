import face_recognition
import numpy as np
import uuid
import config
import os
import math
import cv2
import torch
from FAS import FAS_service
from face_recognition import FaceRecognition

fas = FAS_service(model_path=config.FAS_model_path(), device= "cuda" if torch.cuda.is_available() else "cpu")
face_recognition = FaceRecognition(gpu_id = 1 if torch.cuda.is_available() else -1, face_db=config.FacesPath(), det_size=(640,640))

GREEN = (0, 255, 0)
RED = (0, 0, 255)


def select_large_face_encoding(face_image):
        return face_recognition.detect_lagest(face_image)

def recongition(imgPath):
    img = cv2.imread(imgPath)
    results = face_recognition.recognize(img)
    if(len(results) != 1):
        return '_error_'
    else:
        return results[0]
              

def opencv_recongition_alg(frame,tolerance=1.24,FAS=False,frame_size=160000):
    _shape = frame.shape
    area = _shape[0] * _shape[1]
    resmall = frame_size/area
    relarge = area/frame_size
    small_frame = cv2.resize(frame, (0, 0), fx=resmall, fy=resmall)

    # Face Recognition
    recognized_faces = face_recognition.recognition_more(small_frame)

    fas_color = []
    # Face Anti-Spoofing
    if FAS:
        fas_score = fas.check_faces_cv2(frame, [det_face['bbox'] for det_face in recognized_faces])
        fas_color = []
        #FAS 的 UI
        if fas_score is not None:
                for score in fas_score:
                    fas_color.append(RED if score>0.651313990354538 else GREEN)
    else:
        for face in recognized_faces:
            fas_color.append(RED)
                    

    # Display the results
    for face,color in zip(recognized_faces,fas_color):
        (left,top,right,bottom ) = face['bbox']
        # Scale back up face locations since the frame we detected in was scaled to 1/2 size
        top= math.floor( top * relarge)
        right = math.floor( right * relarge)
        bottom = math.floor( bottom * relarge)
        left = math.floor(left * relarge)

        color = color
        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), color, 1+math.floor(_shape[0]*0.001))

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom), (right, math.floor(bottom+_shape[0]*0.03)), color, cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame,face['name'], (left,math.floor(bottom +_shape[0]*0.03)), font, _shape[0]*0.002, (255, 255, 255), 1+math.floor(_shape[0]*0.0015))
        if FAS:
            cv2.putText(frame, str(score), (left+1,math.floor(top+_shape[0]*0.02)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return frame


def find_faces_in_image(imgPath):
    frame = cv2.imread(imgPath)
    opencv_recongition_alg(frame,frame_size=1000000)
    # # return base64_str of image
    uuid_str = uuid.uuid1().__str__()
    filename =  uuid_str + ".jpg"
    filepath = os.path.join(config.upload(),filename)
    cv2.imwrite(filepath,frame)
    return uuid_str


def web_video_is_effective(url):
    try:
        capture = cv2.VideoCapture(url)
        success,frame = capture.read()
        if success:
            return True
        else:
            return False
    except:
        return False

def find_faces_in_web_video(url,FAS = False):
    capture = cv2.VideoCapture(url)
    while True:
        success, frame = capture.read()  # read the camera frame
        if not success:
            break
        else:
            inframe = opencv_recongition_alg(frame,tolerance=0.55,FAS=FAS)
            ret, buffer = cv2.imencode('.jpg', inframe)
            outframe = buffer.tobytes()
        yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + outframe + b'\r\n')  # concat frame one by one and show result


def compare_two_faces(imgPath1,imgPath2):
    img1 = cv2.imread(imgPath1)
    img2 = cv2.imread(imgPath2) 
    result1 = select_large_face_encoding(img1)
    result2 = select_large_face_encoding(img2)
    if(result1 is None or result2 is None):
        return '_error_'
    else:
        distances = face_recognition.feature_compare2(result1['embedding'],result2['embedding'])
        return {
            "is_same": face_recognition.feature_compare(result1['embedding'],result2['embedding']),
            "score": distances
        }

def slice_face(imgPath):
    img = cv2.imread(imgPath)
    detected_faces = face_recognition.detect(img)
    if(len(detected_faces) == 0):
        return '_error_'
    else:
        mask = np.zeros((img.shape[0],img.shape[1],3),np.uint8)        
        img_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        area = []
        for detected_face in detected_faces:
            landmarks = detected_face['landmark_3d_68']
                #求出两个中点
            left_center_point = ((landmarks[0][0] + landmarks[19][0])/2-2,(landmarks[0][1] + landmarks[19][1])/2-2)
            right_center_point = ((landmarks[16][0] + landmarks[24][0])/2-2,(landmarks[16][1] + landmarks[24][1])/2-2)
            for i in range(0,16):
                cv2.line(mask,(int(landmarks[i][0]),int(landmarks[i][1])),(int(landmarks[i+1][0]),int(landmarks[i+1][1])),(255,255,255),1)
            cv2.line(mask,(int(left_center_point[0]),int(left_center_point[1])),(int(landmarks[0][0]),int(landmarks[0][1])),(255,255,255),1)
            cv2.line(mask,(int(right_center_point[0]),int(right_center_point[1])),(int(landmarks[16][0]),int(landmarks[16][1])),(255,255,255),1)
            cv2.line(mask,(int(landmarks[19][0]),int(landmarks[19][1])),(int(landmarks[24][0]),int(landmarks[24][1])),(255,255,255),1)
            cv2.line(mask,(int(left_center_point[0]),int(left_center_point[1])),(int(landmarks[19][0]),int(landmarks[19][1])),(255,255,255),1)
            cv2.line(mask,(int(right_center_point[0]),int(right_center_point[1])),(int(landmarks[24][0]),int(landmarks[24][1])),(255,255,255),1)
        
        img_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        t, img_gray = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
        # findContours 应该用灰度图，不然会报错
        contours, hierarchy = cv2.findContours(img_gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        for k in range(len(contours)):
            area.append(cv2.contourArea(contours[k]))
        # 轮廓索引
        max_idx = np.argsort(np.array(area))
            
         #对原图像进行轮廓填充，也就是扣除人脸图像
        #res_img = np.zeros((img.shape[0],img.shape[1],3),np.uint8)
        # 按轮廓索引填充颜色
        for idx in max_idx:
            # 填充轮廓
            mask = cv2.drawContours(mask, contours, idx, (255,255,255), cv2.FILLED)
        mask = cv2.bitwise_and(img, mask)
        # cv2.imshow('mask',mask)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        file_uuid = str(uuid.uuid1())
        file_name = file_uuid + ".jpg"         
        cv2.imwrite(os.path.join(config.upload(),file_name),mask)
        return file_uuid
            
                