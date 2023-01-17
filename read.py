# coding=utf-8
import os
import xlwt  # 操作excel模块
import sys

file_path = sys.path[0]+'\\data.xls'  # sys.path[0]为要获取当前路径，filenamelist为要写入的文件
f = xlwt.Workbook(encoding='utf-8', style_compression=0)  # 新建一个excel
sheet = f.add_sheet('sheet1')  # 新建一个sheet
pathDir = os.listdir(sys.path[0])  # 文件放置在当前文件夹中，用来获取当前文件夹内所有文件目录

i = 0  # 将文件列表写入data.xls
for s in pathDir:
    s = s.split('.')[0]
    sheet.write(0, i, s)  # 参数i,0,s分别代表行，列，写入值
    i = i+1

fopen = open("D:/Code/Python/invoice/ocr/test_result/test_images/t1.txt", 'r')
lines = fopen.readlines()

j = 1
for line in lines:
    sheet.write(j, 0, line)
    j = j+1

f.save(file_path)
fopen1 = open("D:/Code/Python/invoice/ocr/test_result/test_images/t2.txt", 'r')
lines1 = fopen1.readlines()

b = 1
for line1 in lines1:
    sheet.write(b, 1, line1)
    b = b+1

print(file_path)
print(i)  # 显示文件名数量
f.save(file_path)

