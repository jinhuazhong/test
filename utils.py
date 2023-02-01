import os

import cv2
import fitz
import numpy as np


def pdf_to_image(pdf_file,
                 image_format='png',
                 ) -> list:
    # create output folder

    # extract pdf_dir pages and convert to image
    pdf = fitz.open(pdf_file)
    images = list()
    for i, page in enumerate(pdf):
        rotate = int(0)
        # 每个尺寸的缩放系数为20，这将为我们生成分辨率提高四倍的图像。
        zoom_x = 15.0
        zoom_y = 15.0
        trans = fitz.Matrix(zoom_x, zoom_y)  # .preRotate(rotate)
        pixel_map: fitz.fitz.Pixmap = page.get_pixmap(matrix=trans, alpha=False)
        images.append(pixel_map.tobytes(output='png'))
    pdf.close()
    return images


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


def recognize(document) -> list:
    images = pdf_to_image(document)
    i: bytes
    for i in images:
        img = cv2.imdecode(np.frombuffer(i, np.uint8), cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w = img.shape[0], img.shape[1]
        m = 2
        n = 2
        divide_image2 = divide_method2(img, m + 1, n + 1)  # 该函数中m+1和n+1表示网格点个数，m和n分别表示分块的块数
        save_blocks(title, divide_image2)
        print("第", title, "个已分块完毕")
        print("-----------------------------")
        title += 1
