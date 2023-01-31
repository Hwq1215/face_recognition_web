import torch
import torch.nn as nn
import os
from networks import SSAN_R
from optimizers import get_optimizer
from torch.utils.data import Dataset, DataLoader
from transformers import *
from utils import *
from configs import parse_args
import time
import numpy as np
import random
from loss import *
import pandas as pd
from datasets import ClelebA_Spoofing_train_dataset
from datasets import ClelebA_Spoofing_test_dataset


def test_video(model, test_loader, score_path, epoch):
    model.eval()
    with torch.no_grad():
        start_time = time.time()
        scores_list = []
        for i, sample_batched in enumerate(test_loader):
            image_x, label, UUID = sample_batched["image_x"].cuda(), sample_batched["label"].cuda(), sample_batched[
                "UUID"]
            spoof_type, illumination_condition, environment_condition = UUID
            spoof_type.cuda()
            illumination_condition.cuda()
            environment_condition.cuda()

            cls_x1_x1, fea_x1_x1, fea_x1_x2,  _, _ = model(image_x, image_x)
            score_norm = torch.softmax(cls_x1_x1, dim=1)[:, 1]
            for ii in range(image_x.shape[0]):
                scores_list.append("{} {}\n".format(score_norm[ii], label[ii][0]))
            
        map_score_val_filename = os.path.join(score_path, "score.txt")
        print("score: write test scores to {}".format(map_score_val_filename))
        with open(map_score_val_filename, "w") as f:
            f.writelines(scores_list)
        
        test_ACC, fpr, FRR, HTER, auc_test, test_err = performances_val(map_score_val_filename)
        print("## {} score:")
        print("epoch:{:d}, test:  val_ACC={:.4f}, HTER={:.4f}, AUC={:.4f}, val_err={:.4f}, ACC={:.4f}".format(epoch + 1,
                                                                                                            test_ACC,
                                                                                                            HTER,
                                                                                                            auc_test,
                                                                                                            test_err,
                                                                                                            test_ACC))
        print("test phase cost {:.4f}s".format(time.time() - start_time))
        return HTER, auc_test


def main(args):
    print('loading info')
    df = pd.read_csv(os.path.join(args.data_dir, 'metas/intra_test/test_label.txt'), sep=' ', header=None)
    transformer = transformer_train()

    # prepare dataset
    print('loading data')
    dataset = ClelebA_Spoofing_train_dataset(args.data_dir, transform=transformer)
    test_dataset = ClelebA_Spoofing_test_dataset(args.data_dir, transform=transformer)
    train_loader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True, num_workers=8)
    test_loader = DataLoader(test_dataset, batch_size=args.batch_size, shuffle=False, num_workers=8)

    print('loading model')
    model = SSAN_R(max_iter=args.num_epochs * len(train_loader)).cuda()
    model = nn.DataParallel(model).cuda()

    optimizer = get_optimizer(
            args.optimizer, model,
            lr=args.base_lr,
            momentum=args.momentum,
            weight_decay=args.weight_decay)

    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=args.step_size, gamma=args.gamma)

    model_root_path = os.path.join(args.result_path, "model")
    check_folder(model_root_path)
    score_root_path = os.path.join(args.result_path, "score")
    check_folder(score_root_path)
    csv_root_path = os.path.join(args.result_path, "csv")
    check_folder(csv_root_path)

    binary_fuc = nn.CrossEntropyLoss()
    map_fuc = nn.MSELoss()
    contra_fun = ContrastLoss()


    eva = {
        "best_epoch": -1,
        "best_HTER": 100,
        "best_auc": -100
    }

    
    for epoch in range(args.start_epoch, args.num_epochs):
        binary_loss_record = AvgrageMeter()
        constra_loss_record = AvgrageMeter()
        adv_loss_record = AvgrageMeter()
        loss_record = AvgrageMeter()
        # train
        model.train()

        for i, sample_batched in enumerate(train_loader):
            image_x, label, UUID = sample_batched["image_x"].cuda(), sample_batched["label"].cuda(), sample_batched[
                "UUID"]
            spoof_type, illumination_condition, environment_condition = UUID
            # spoof_type = spoof_type.cuda()
            illumination_condition = illumination_condition.cuda()
            environment_condition = environment_condition.cuda()
            environment_condition.cuda()

            rand_idx = torch.randperm(image_x.shape[0])
            cls_x1_x1, fea_x1_x1, fea_x1_x2, domain_invariant_ic, domain_invariant_ec = model(image_x, image_x[rand_idx, :, :, :])
            binary_loss = binary_fuc(cls_x1_x1, label[:, 0].long())
            contrast_label = label[:, 0].long() == label[rand_idx, 0].long()
            contrast_label = torch.where(contrast_label == True, 1, -1)
            constra_loss = contra_fun(fea_x1_x1, fea_x1_x2, contrast_label)
            adv_loss = binary_fuc(domain_invariant_ic, illumination_condition.long()) + binary_fuc(domain_invariant_ec, environment_condition.long())
            loss_all = binary_loss + constra_loss + adv_loss

            n = image_x.shape[0]
            binary_loss_record.update(binary_loss.data, n)
            constra_loss_record.update(constra_loss.data, n)
            adv_loss_record.update(adv_loss.data, n)
            loss_record.update(loss_all.data, n)

            model.zero_grad()
            loss_all.backward()
            optimizer.step()
            lr = optimizer.param_groups[0]['lr']
            if i % args.print_freq == args.print_freq - 1:
                print(
                    "epoch:{:d}, mini-batch:{:d}, lr={:.4f}, binary_loss={:.4f}, constra_loss={:.4f}, adv_loss={:.4f}, Loss={:.4f}".format(
                        epoch + 1, i + 1, lr, binary_loss_record.avg, constra_loss_record.avg, adv_loss_record.avg,
                        loss_record.avg))

        print("epoch:{:d}, Train: lr={:f}, Loss={:.4f}".format(epoch + 1, lr, loss_record.avg))
        scheduler.step()

        # test
        epoch_test = 1    
        if epoch % epoch_test == epoch_test - 1: 
            score_path = os.path.join(score_root_path, "epoch_{}".format(epoch + 1))
            check_folder(score_path) 
            print("testing epoch {}".format(epoch + 1))
            HTER, auc_test = test_video(model, test_loader, score_path, epoch)
            
            # save model
            if auc_test - HTER >= eva["best_auc"] - eva["best_HTER"]:
                eva["best_auc"] = auc_test
                eva["best_HTER"] = HTER
                eva["best_epoch"] = epoch + 1
                model_path = os.path.join(model_root_path, "{}_p{}_best.pth".format(args.model_type, epoch+1))
                torch.save({
                    'epoch': epoch + 1,
                    'state_dict': model.module.state_dict(),
                    'optimizer': optimizer.state_dict(),
                    'scheduler': scheduler,
                    'args': args,
                }, model_path)
                print("Model saved to {}".format(model_path))
            print("[Best result] epoch:{}, HTER={:.4f}, AUC={:.4f}".format(eva["best_epoch"], eva["best_HTER"],
                                                                            eva["best_auc"]))
            model_path = os.path.join(model_root_path, "{}_e{}_recent.pth".format(args.model_type, epoch+1))
            torch.save({
                'epoch': epoch + 1,
                'state_dict': model.module.state_dict(),
                'optimizer': optimizer.state_dict(),
                'scheduler': scheduler,
                'args': args,
            }, model_path)
            print("Model saved to {}".format(model_path))     


if __name__ == '__main__':
    args = parse_args()
    main(args)