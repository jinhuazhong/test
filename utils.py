import os

import fitz


def pdf_to_image(pdf_file,
                 image_format='png',
                 ):

    # create output folder

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

def recognize(document) -> list:
