import os

import cv2
import insightface
import numpy as np
from sklearn import preprocessing
import pandas as pd
import uuid

class FaceRecognition:
    def __init__(self, gpu_id=-1, face_db='face_db', threshold=1.24, det_thresh=0.50, det_size=(640, 640)):
        """
        人脸识别工具类
        :param gpu_id: 正数为GPU的ID，负数为使用CPU
        :param face_db: 人脸库文件夹
        :param threshold: 人脸识别阈值
        :param det_thresh: 检测阈值
        :param det_size: 检测模型图片大小
        """
        self.gpu_id = gpu_id
        self.face_db = face_db
        self.threshold = threshold
        self.det_thresh = det_thresh
        self.det_size = det_size

        # 加载人脸识别模型，当allowed_modules=['detection', 'recognition']时，只单纯检测和识别
        self.model = insightface.app.FaceAnalysis(root='./',
                                                  allowed_modules=None,
                                                  providers=['CUDAExecutionProvider'])
        self.model.prepare(ctx_id=self.gpu_id, det_thresh=self.det_thresh, det_size=self.det_size)
        # 人脸库的人脸特征
        self.faces_embedding = list()
        # 加载人脸库中的人脸
        self.load_faces(self.face_db)

    # 加载人脸库中的人脸
    def load_faces(self, face_db_path):
        if not os.path.exists(face_db_path):
            os.makedirs(face_db_path)
        for root, dirs, files in os.walk(face_db_path):
            for file in files:
                if file.endswith(".jpg"):
                    continue
                input_image = cv2.imdecode(np.fromfile(os.path.join(root, file), dtype=np.uint8), 1)
                file_name = file.split(".")[0]
                #防止图片重名
                user_name = file_name.split("-")[0]
                face_id = file_name.split("-")[1]
                face = self.model.get(input_image)[0]
                embedding = np.array(face.embedding).reshape((1, -1))
                embedding = preprocessing.normalize(embedding)
                self.faces_embedding.append({
                    "face_id": face_id,
                    "user_name": user_name,
                    "feature": embedding
                })
    
    # 人脸识别
    def recognition(self, image):
        faces = self.model.get(image)
        results = list()
        for face in faces:
            # 开始人脸识别
            embedding = np.array(face.embedding).reshape((1, -1))
            embedding = preprocessing.normalize(embedding)
            user_name = "unknown"
            for com_face in self.faces_embedding:
                r = self.feature_compare(embedding, com_face["feature"], self.threshold)
                if r:
                    user_name = com_face["user_name"]
            results.append(user_name)
        return results

    #人脸识别带框等信息
    def recognition_more(self, image):
        faces = self.model.get(image)
        results = list()
        for face in faces:
            # 开始人脸识别
            embedding = np.array(face.embedding).reshape((1, -1))
            embedding = preprocessing.normalize(embedding)
            user_name = "unknown"
            for com_face in self.faces_embedding:
                r = self.feature_compare(embedding, com_face["feature"], self.threshold)
                if r:
                    user_name = com_face["user_name"]
            results.append({
                "name": user_name,
                "bbox": np.array(face.bbox).astype(np.int32).tolist(),
                "landmark": np.array(face.landmark_3d_68).astype(np.int32).tolist()
            })
        return results

    @staticmethod
    def feature_compare(feature1, feature2, threshold=1.24):
        diff = np.subtract(feature1, feature2)
        dist = np.sum(np.square(diff), 1)
        if dist < threshold:
            return True
        else:
            return False

    def feature_compare2(self,embedding1,embedding2):
        diff = np.subtract(embedding1, embedding2)
        dist = np.sum(np.square(diff), 1)
        return str(dist)


    # 注册人脸
    # return ('hadexist','') 人脸已存在
    # return ('morefind','') 人脸库中存在多张人脸
    # return ('nofind','') 人脸库中不存在人脸
    # return ('success',path) 注册成功,返回图片路径
    def register(self, image,face_id,user_name):
        faces = self.model.get(image)
        if len(faces) == 0:
            return ('nofind','')
        elif len(faces) > 1:
            return ('morefind','')
        # 判断人脸是否存在
        embedding = np.array(faces[0].embedding).reshape((1, -1))
        embedding = preprocessing.normalize(embedding)
        is_exits = False
        for com_face in self.faces_embedding:
            r = self.feature_compare(embedding, com_face["feature"], self.threshold)
            if r:
                is_exits = True
        if is_exits:
            return ('hadexist','')
        # 符合注册条件保存图片，同时把特征添加到人脸特征库中
        file_name = '%s.png' % (user_name + '-' + str(face_id))
        path = os.path.join(self.face_db,file_name)
        cv2.imencode('.png', image)[1].tofile(path)
        self.faces_embedding.append({
            "face_id": str(face_id),
            "user_name": user_name,
            "feature": embedding
        })
        return ("success",file_name)
    
    # 删除人脸
    def delete(self,face_id):
        for embedding in self.faces_embedding:
            if embedding['face_id'] == str(face_id):
                self.faces_embedding.remove(embedding)
        for root, dirs, files in os.walk(self.face_db):
            for file in files:
                if file.endswith(".jpg"):
                    continue
                file_name = file.split(".")[0]
                #防止图片重名
                f_face_id = file_name.split("-")[1]
                # print(str(f_face_id) + ":: " + face_id)
                if str(f_face_id) == str(face_id):
                    os.remove(os.path.join(root, file))
                    break
    
    # 检测人脸
    def detect(self, image):
        faces = self.model.get(image)
        results = list()
        for face in faces:
            result = dict()
            # 获取人脸属性
            result["bbox"] = np.array(face.bbox).astype(np.int32).tolist()
            result["kps"] = np.array(face.kps).astype(np.int32).tolist()
            result["landmark_3d_68"] = np.array(face.landmark_3d_68).astype(np.int32).tolist()
            result["landmark_2d_100"] = np.array(face.landmark_2d_106).astype(np.int32).tolist()
            result["pose"] = np.array(face.pose).astype(np.int32).tolist()
            result["age"] = face.age
            gender = '男'
            if face.gender == 0:
                gender = '女'
            result["gender"] = gender
            
            # 开始人脸识别
            embedding = np.array(face.embedding).reshape((1, -1))
            embedding = preprocessing.normalize(embedding)
            result["embedding"] = embedding
            results.append(result)
        return results

    # 返回最大人脸信息
    def detect_lagest(self,image):
        results = self.detect(image)
        if len(results) == 0:
            return None
        max_area = 0
        max_result = None
        for result in results:
            bbox = result["bbox"]
            area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
            if area > max_area:
                max_area = area
                max_result = result
        return max_result

if __name__ == '__main__':
    img = cv2.imdecode(np.fromfile('/Volumes/shield/data/CelebA-Spoof_21/CelebA_Spoof/Data/train/1/live/000184.jpg', dtype=np.uint8), -1)
    face_recognitio = FaceRecognition()
    
    # 人脸注册
    result = face_recognitio.register(img, user_name='迪丽热巴')
    print(result)

    # 人脸识别
    results = face_recognitio.recognition(img)
    for result in results:
        print("识别结果：{}".format(result))

    results = face_recognitio.detect(img)
    for result in results:
        print('人脸框坐标：{}'.format(result["bbox"]))
        print('人脸五个关键点：{}'.format(result["kps"]))
        print('人脸3D关键点：{}'.format(result["landmark_3d_68"]))
        print('人脸2D关键点：{}'.format(result["landmark_2d_106"]))
        print('人脸姿态：{}'.format(result["pose"]))
        print('年龄：{}'.format(result["age"]))
        print('性别：{}'.format(result["gender"]))
