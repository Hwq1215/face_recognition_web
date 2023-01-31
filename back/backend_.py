import cv2
from FAS import FAS_service
import numpy as np
import torch
from face_recognition import FaceRecognition

class SafeFaceRecognition():
    def __init__(self, model_path, face_db, det_size, device=None, check_interval=1):
        if not device:
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.FAS = FAS_service(model_path=model_path, device=device)
        self.FR = FaceRecognition(gpu_id = 1 if device == 'cuda' else -1, face_db=face_db, det_size=det_size)
        self.video_capture = cv2.VideoCapture(0)
        self.check_interval = check_interval
    def start(self):
        frame_count = 0
        while True:
            ret, frame = self.video_capture.read()
            frame_count += 1

            # 人脸检测
            face_names = list()
            detected_faces = self.FR.detect(frame)
            # 人脸识别
            recognized_faces = self.FR.recognition(frame)
            # Face Anti-Spoofing
            fas_score = self.FAS.check_faces_cv2(frame, [det_face['bbox'] for det_face in detected_faces])
            fas_color = []
            # fas_score = [False,False]
            # fas_color = [(0,0,225),(0,0,255)]
            if fas_score is not None:
                for score in fas_score:
                    fas_color.append((0, 0, 255) if score>0.651313990354538 else (0, 255, 0))

                # UI显示
                for face_info, color, score, name in zip(detected_faces, fas_color, fas_score, recognized_faces):
                    bbox = face_info['bbox']
                    landmark = face_info['landmark_3d_68']
                    cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)
                    cv2.putText(frame, name, (bbox[0], bbox[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    cv2.putText(frame, str(score), (bbox[0], bbox[1]+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    for i in range(len(landmark)):
                        cv2.circle(frame, (landmark[i][0], landmark[i][1]), 1, (0, 0, 255), 2)
            cv2.imshow('Video', frame)
            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
        self.video_capture.release()
        cv2.destroyAllWindows()
    
    def load_face_db(self, face_db):
        self.FR.load_faces(face_db)

    def load_embedding_db(self, embedding_db):
        self.FR.load_embedding_db(embedding_db)

if __name__ == '__main__':
    model_path = 'D:/pythonTools/face_recognize/fc_system/back/FAS/results/model/SSAN-R_p3_best.pth'
    face_db = 'face_db'
    det_size = (640, 640)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    FR = SafeFaceRecognition(model_path, face_db, det_size, device)
    FR.start()