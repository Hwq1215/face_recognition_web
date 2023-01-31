from .networks import SSAN_R,SSAN_F
import torch
from .transformers import *
import numpy as np
import cv2
from .datasets import get_single_image_x
import math

class FAS_service():
    def __init__(self, model_path, device, transformer='transfromer_test_pic') -> None:
        self.device = device
        self.model = SSAN_R(max_iter=4000)
        # self.model = SSAN_F(max_iter=4000)
        self.model.load_state_dict(torch.load(model_path, map_location=self.device)['state_dict'])
        if self.device == 'cuda':
            self.model = self.model.cuda()
        self.model.eval()
        if transformer == 'transfromer_test_pic':
            self.transform = transformer_test_pic()
        elif transformer == 'transfromer_test_pic_ImageNet':
            self.transform = transformer_test_pic_ImageNet()

    def check_faces_batch(self, face_batch):
        with torch.no_grad():
            face_batch = face_batch.to(torch.device(self.device))
            #R
            cls_x1, _, _, _, _ = self.model(face_batch, face_batch)
            # #F
            # cls_x1, _, _, _= self.model(face_batch, face_batch)
            score_norm = torch.softmax(cls_x1, dim=1)[:, 1]
        return score_norm
    
    def check_faces_cv2(self, frame, bbox_list):
        """
        :param frame: cv2 image
        :param bbox_list: list of bbox
        """
        face_list = []
        for bbox in bbox_list:
            face = crop_face_from_scene(frame, bbox, 1.5)
            face = cv2.resize(face, (224, 224))
            sample = {'image_x': face, 'label': 0, 'UUID': 0}
            face_t = self.transform(sample)
            face_t = face_t['image_x'].unsqueeze(0)
            face_list.append(face_t)
        try:
            face_batch = torch.cat(face_list, dim=0)
        except:
            return None
        score_norm = self.check_faces_batch(face_batch)
        return score_norm

def crop_face_from_scene(image, bbox, scale):
    real_h = image.shape[0]
    real_w = image.shape[1]
    x1 = int(bbox[0])
    y1 = int(bbox[1])
    w1 = int(bbox[3]-bbox[1])
    h1 = int(bbox[2]-bbox[0])
    x_mid = (x1 + x1 + w1) / 2.0
    y_mid = (y1 + y1 + h1) / 2.0
    w_scale = scale * w1
    h_scale = scale * h1
    x1 = x_mid - w_scale / 2.0
    y1 = y_mid - h_scale / 2.0
    x2 = x_mid + w_scale / 2.0
    y2 = y_mid + h_scale / 2.0
    y1 = max(math.floor(y1), 0)
    x1 = max(math.floor(x1), 0)
    y2 = min(math.floor(y2), real_h)
    x2 = min(math.floor(x2), real_w)
    region = image[y1:y2, x1:x2]
    return region

if __name__ == "__main__":
    fas = FAS_service('/Users/ooohy/Documents/服创/Project/FAS/results/model/SSAN-R_p1_best.pth', 'cpu')
    image_path_full = '/Volumes/shield/data/CelebA-Spoof_21/CelebA_Spoof/Data/train/1/live/072342.jpg'
    BB_path_full = '/Volumes/shield/data/CelebA-Spoof_21/CelebA_Spoof/Data/train/1/live/072342_BB.txt'
    # image_path_full = '/Volumes/shield/data/CelebA-Spoof_21/CelebA_Spoof/Data/train/1/spoof/314287.jpg'
    # BB_path_full = '/Volumes/shield/data/CelebA-Spoof_21/CelebA_Spoof/Data/train/1/spoof/314287_BB.txt'
    root = '/Volumes/shield/data/CelebA-Spoof_21/CelebA_Spoof/'
    spoof_list = ['Data/test/6964/spoof/494405.png',
'Data/test/9596/spoof/494406.png',
'Data/test/9014/spoof/494407.png',
'Data/test/7607/spoof/494408.png',
'Data/test/5624/spoof/494409.png']
    live_list = ['Data/test/8965/live/494410.png',
    'Data/test/9283/live/494415.png',
    'Data/test/6411/live/494418.png',
    'Data/test/7883/live/494422.png',
    'Data/test/6074/live/494424.png']

    spoof_image_list = []
    for i in range(5):
        image_path = root + spoof_list[i]
        # image_path = root + live_list[i]
        spoof_image_list.append(get_single_image_x(image_path, image_path.replace('.png', '_BB.txt'), 1.5))
    print(fas.check_faces_cv2(spoof_image_list))
