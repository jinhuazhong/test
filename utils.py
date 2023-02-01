import os

import fitz


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


def recognize(document) -> list:
