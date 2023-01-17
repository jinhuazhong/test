import os
from ocr import ocr
import time
import shutil
import numpy as np
from PIL import Image
from glob import glob
import json
import requests
import datetime
import fitz
import re
import os
# -*- coding: utf-8 -*-
"""
pre-install 3 modules:
pip install traits
pip install fitz
pip install pymupdf
"""
import numpy as np
import matplotlib.pyplot as plt
import cv2

import os
import fitz
import linecache


def pdf_to_image(pdf_file,
                 output_folder=None,
                 image_format='png',
                 ):

    # create output folder
    if output_folder is None:
        output_folder = os.path.splitext(pdf_file)[0]
    os.makedirs(output_folder, exist_ok=True)

    # extract pdf_dir pages and convert to image
    pdf = fitz.open(pdf_file)

    for i, page in enumerate(pdf):
        rotate = int(0)
        # 每个尺寸的缩放系数为20，这将为我们生成分辨率提高四倍的图像。
        zoom_x = 15.0
        zoom_y = 15.0
        trans = fitz.Matrix(zoom_x, zoom_y)#.preRotate(rotate)
        pixel_map = page.get_pixmap(matrix=trans, alpha=False)
        pixel_map.save(
            os.path.join(output_folder, '{}.{}'.format(str(i), image_format)))
    pdf.close()
def single_pic_proc(image_file):
    image = np.array(Image.open(image_file).convert('RGB'))
    result, image_framed = ocr(image)
    return result,image_framed


# 边里该文件夹下的文件名称
def read_directory(directory_name):
    file_list = []
    for filename in os.listdir(directory_name):
        str = directory_name + '/' + filename
        file_list.append(str)
    return file_list


def divide_method1(img, m, n):  # 分割成m行n列
    print(img.shape)
    h, w = img.shape[0], img.shape[1]
    gx = np.round(h).astype(np.int)
    gy = np.round(w).astype(np.int)
    divide_image = np.zeros([m - 1, n - 1, int(h * 1.0 / (m - 1) + 0.5), int(w * 1.0 / (n - 1) + 0.5), 3],
                            np.uint8)
    for i in range(m - 1):
        for j in range(n - 1):
            print(i)
            print(j)
            print(img[gy[i][j]:gy[i + 1][j + 1], gx[i][j]:gx[i + 1][j + 1], :])
            divide_image[i, j, 0:gy[i + 1][j + 1] - gy[i][j], 0:gx[i + 1][j + 1] - gx[i][j], :] = img[
                                                                                                  gy[i][j]:gy[i + 1][
                                                                                                      j + 1],
                                                                                                  gx[i][j]:gx[i + 1][
                                                                                                      j + 1], :]

    return divide_image


def divide_method2(img, m, n):  # 分割成m行n列
    h, w = img.shape[0], img.shape[1]
    grid_h = int(h * 1.0 / (m - 1) + 0.5)  # 每个网格的高
    grid_w = int(w * 1.0 / (n - 1) + 0.5)  # 每个网格的宽

    # 满足整除关系时的高、宽
    h = grid_h * (m - 1)
    w = grid_w * (n - 1)

    # 图像缩放
    img_re = cv2.resize(img, (w, h),
                        cv2.INTER_LINEAR)  # 也可以用img_re=skimage.transform.resize(img, (h,w)).astype(np.uint8)
    # plt.imshow(img_re)
    gx, gy = np.meshgrid(np.linspace(0, w, n), np.linspace(0, h, m))
    gx = gx.astype(np.int_)
    gy = gy.astype(np.int_)

    divide_image = np.zeros([m - 1, n - 1, grid_h, grid_w, 3],
                            np.uint8)

    for i in range(m - 1):
        for j in range(n - 1):
            divide_image[i, j, ...] = img_re[
                                      gy[i][j]:gy[i + 1][j + 1], gx[i][j]:gx[i + 1][j + 1], :]
    return divide_image


def save_blocks(title, divide_image):  #
    m, n = divide_image.shape[0], divide_image.shape[1]
    for i in range(m):
        for j in range(n):
            plt.imshow(divide_image[i, j, :])
            plt.axis('off')
            plotPath = str(title) + "+" + str(i) + str(j) + '.jpg'  # 图片保存路径
            plt.savefig("./img_list4/" + plotPath)



if __name__ == '__main__':

    pdf_file = '.\\pdf_dir\\test.pdf'

    output_folder = 'images1'
    pdf_to_image(pdf_file, output_folder)
    intput = read_directory("./images1")
    print("PDF页数为：", len(intput))
    title = 1
    print("==============开始分块处理图片==============")
    for input_path in intput:
        print("开始处理第", title, "个，其地址为：", input_path)
        img = cv2.imread(input_path)  # 图片地址
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w = img.shape[0], img.shape[1]
        m = 2
        n = 2
        divide_image2 = divide_method2(img, m + 1, n + 1)  # 该函数中m+1和n+1表示网格点个数，m和n分别表示分块的块数
        save_blocks(title, divide_image2)
        print("第", title, "个已分块完毕")
        print("-----------------------------")
        title += 1
    print("==============完成全部分块==============")

    image_files = glob('./img_list4/*.*')
    result_dir = './test_pdf_result_22'
    if os.path.exists(result_dir):
        shutil.rmtree(result_dir)
    os.mkdir(result_dir)


    temp = ""
    temp1 = ""
    arr = []
    arr1 = []
    contend = {}
    count = 0
    page = 1
    flag = 0
    data = {'name': os.path.basename(pdf_file)}

    for image_file in sorted(image_files):
        t = time.time()
        result, image_framed = single_pic_proc(image_file)
        output_file = os.path.join(result_dir, image_file.split('/')[-1])
        txt_file = os.path.join(result_dir, image_file.split('/')[-1].split('.')[0] + '.txt')
        if not os.path.exists(os.path.dirname(txt_file)):
            os.mkdir(os.path.dirname(txt_file))
        print(txt_file)
        txt_f = open(txt_file, 'w')
        Image.fromarray(image_framed).save(output_file)
        print("Mission complete, it took {:.3f}s".format(time.time() - t))
        print("\nRecognition Result:\n")
        for key in result:
            print(result[key][1])
            arr.append(result[key][1])
            txt_f.write(result[key][1] + '\n')

        for i in range(len(arr)):
            temp += arr[i]

        flag += 1
        # print('===================================================')
        # print(temp)
        if(flag % 4 != 0):
            arr1.append(temp)
        else:
            arr1.append(temp)
            temp1 = "".join(arr1)
            contend[page] = temp1
            # print('===================================================')
            # print(contend)
            page += 1
            arr1.clear()
        arr.clear()
        temp = ""
        txt_f.close()

    data['page'] = contend
    info_json = json.dumps(data)
    #print(info_json)
    #url = "https://47.242.189.250:9090/"
    #response = requests.post(url, info_json, verify=False)
    #print(response.txt)









