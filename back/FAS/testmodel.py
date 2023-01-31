from networks import SSAN_R
import torch
from torch.utils.data import Dataset, DataLoader
from datasets import ClelebA_Spoofing_test_dataset
from configs import parse_args
from transformers import *

model = SSAN_R()
model.load_state_dict(torch.load('/Users/ooohy/Documents/服创/Project/FAS/results/model/SSAN-R_e3_recent.pth', map_location=torch.device('cpu'))['state_dict'])
args = parse_args()

def test_video(model, test_loader):
    model.eval()
    with torch.no_grad():
        scores_list = []
        for i, sample_batched in enumerate(test_loader):
            image_x, label, UUID = sample_batched["image_x"], sample_batched["label"], sample_batched[
                "UUID"]
            cls_x1_x1, fea_x1_x1, fea_x1_x2,  _, _ = model(image_x, image_x)
            print(image_x)
            score_norm = torch.softmax(cls_x1_x1, dim=1)[:, 1]
            for ii in range(image_x.shape[0]):
                scores_list.append("{} {}\n".format(score_norm[ii], label[ii][0]))
            print(scores_list)
            break
            
ttp = transformer_test_pic()
test_dataset = ClelebA_Spoofing_test_dataset('/Volumes/shield/data/CelebA-Spoof_21/CelebA_Spoof/', transform=ttp)
test_loader = DataLoader(test_dataset, batch_size=20, shuffle=False)
test_video(model, test_loader)