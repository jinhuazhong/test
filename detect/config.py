#-*- coding:utf-8 -*-
#'''
# Created on 18-12-11 上午10:09
#
# @Author: Greg Gao(laygin)
#'''
import os

# base_dir = 'path to dataset base dir'
base_dir = './images'
img_dir = os.path.join(base_dir, 'VOC2007_text_detection/JPEGImages')#图片数据集文件夹的路径
xml_dir = os.path.join(base_dir, 'VOC2007_text_detection/Annotations')#标签文件夹路径

# icdar17_mlt_img_dir = '/home/data2/egz/ICDAR2017_MLT/train/'
# icdar17_mlt_gt_dir = '/home/data2/egz/ICDAR2017_MLT/train_gt/'
num_workers = 2
pretrained_weights = ''#预训练模型路径

train_txt_file = os.path.join(base_dir, r'VOC2007_text_detection/ImageSets/Main/train.txt')#txt文件路径
val_txt_file = os.path.join(base_dir, r'VOC2007_text_detection/ImageSets/Main/val.txt')


anchor_scale = 16
IOU_NEGATIVE = 0.3
IOU_POSITIVE = 0.7
IOU_SELECT = 0.7

RPN_POSITIVE_NUM = 150
RPN_TOTAL_NUM = 300

# bgr can find from  here: https://github.com/fchollet/deep-learning-models/blob/master/imagenet_utils.py
IMAGE_MEAN = [123.68, 116.779, 103.939]


checkpoints_dir = './checkpoints'#存放训练好的模型文件夹的路径
outputs = r'./logs'
