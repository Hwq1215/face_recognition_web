import math
from torch.utils.data import Dataset, DataLoader
import cv2
import pandas as pd
import os 
import json
import torch
import random

def crop_face_from_scene(image, BB_path_full, scale):
    f = open(BB_path_full, 'r')
    lines = f.readlines()
    bbox = lines[0].split()
    f.close()
    real_h = image.shape[0]
    real_w = image.shape[1]
    x1 = int(int(bbox[0])*(real_w / 224))
    y1 = int(int(bbox[1])*(real_h / 224))
    w1 = int(int(bbox[2])*(real_w / 224))
    h1 = int(int(bbox[3])*(real_h / 224))
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

def get_single_image_x(image_path_full, BB_path_full, scale):
    image = cv2.imread(image_path_full)
    region = crop_face_from_scene(image, BB_path_full, scale)
    image = cv2.resize(region, (224, 224))
    return image



class ClelebA_Spoofing_test_dataset(Dataset):
    def __init__(self, root_dir, transform=None, scale_up=1.5, scale_down=1.0, img_size=256, map_size=32,
                 UUID=-1):
        self.frame = pd.read_csv(os.path.join(root_dir, 'metas/intra_test/test_label.txt'), sep=' ', header=None)
        self.root_dir = root_dir
        # self.map_root_dir = os.path.join(root_dir, "depth")
        self.transform = transform
        self.scale_up = scale_up
        self.img_size = img_size
        self.map_size = map_size
        # self.UUID = UUID
        self.info_dict = json.load(open(os.path.join(root_dir, 'metas/intra_test/test_label.json'), 'r'))

    def __len__(self):
        return len(self.frame)

    def __getitem__(self, idx):
        spoofing_label = self.frame.iloc[idx, 1]
        image_path = os.path.join(self.root_dir, self.frame.iloc[idx, 0])
        UUID = self.read_image_info_from_json(self.frame.iloc[idx, 0])
        try:
            image_x = get_single_image_x(image_path, image_path.replace('.png', '_BB.txt'), self.scale_up)
        except:
            print("get image error: ", image_path)
            rand_idx = random.randint(0, len(self.frame))
            UUID = self.read_image_info_from_json(self.frame.iloc[rand_idx, 0])
            spoofing_label = self.frame.iloc[rand_idx, 1]
            image_path = os.path.join(self.root_dir, self.frame.iloc[rand_idx, 0])
            image_x = get_single_image_x(image_path, image_path.replace('.jpg', '_BB.txt'), self.scale_up)
        sample = {'image_x': image_x, 'label': spoofing_label, "UUID": UUID}
        if self.transform:
            sample = self.transform(sample)
        return sample

    def read_image_info_from_json(self, image_path_rela):
        spoof_type = torch.tensor(int(self.info_dict[image_path_rela][40])).long() # 11 classes
        illumination_condition = torch.tensor(int(self.info_dict[image_path_rela][41])).long() # 5 classes
        environment_condition = torch.tensor(int(self.info_dict[image_path_rela][42])).long() # 3 classes
        # print("sp_type:", spoof_type, "illu_condition:", illumination_condition, "env_condition:", environment_condition)
        return spoof_type, illumination_condition, environment_condition
