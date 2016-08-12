# coding: utf8
from PIL import Image

from otsu import getGray

__author__ = 'tanghan'

''' 微血管提取步骤
    1. (二值图像)形态学腐蚀，消除小血管
    2. 图片异或运算，得小血管坐标
    3. 图片与运算，的的主血管坐标
    4. 小血管角度偏转，或者沿主血管移动
    补充：
        形态学开闭运算在而知图像处理中的应用
'''

# 腐蚀, 采用矩形结构元
def erosion(binimg, diskradius=1, pointcounts = 1):
    pixels = binimg.load()
    imgsize = binimg.size
    imgpix = []
    for y in xrange(0, imgsize[1]):
        temp = []
        for x in xrange(0, imgsize[0]):
            # 探测的像素点总数
            totalpoints = 0
            # 背景点数
            bgpoints = 0
            for m in xrange(x-diskradius, x+diskradius+1):
                for n in xrange(y-diskradius, y+diskradius+1):
                    if (m >= 0 and m <= imgsize[0]-1) and (n >= 0 and n <= imgsize[1]-1) and (m != x and n != y):
                        totalpoints = totalpoints + 1
                        if pixels[m, n] == 0:
                            bgpoints = bgpoints + 1
            if bgpoints >= pointcounts:
                temp.append(0)
            else:
                temp.append(1)
        imgpix.append(temp)
    tempimg = getGray('template.png').resize((imgsize[0], imgsize[1]))

    pixels = tempimg.load()
    for y in xrange(0, len(imgpix)):
        for x in xrange(0, len(imgpix[0])):
            if imgpix[y][x] == 0:
                pixels[x, y] = 0
            else:
                pixels[x, y] = 255
    return tempimg

# 形态学 膨胀操作
def dilation(binimg, diskradius=1, pointcounts=1):
    pixels = binimg.load()
    imgsize = binimg.size
    imgpix = []
    for y in xrange(0, imgsize[1]):
        temp = []
        for x in xrange(0, imgsize[0]):
            # 探测的像素点总数
            totalpoints = 0
            # 背景点数
            colorpoints = 0
            for m in xrange(x - diskradius, x + diskradius + 1):
                for n in xrange(y - diskradius, y + diskradius + 1):
                    if (m >= 0 and m <= imgsize[0] - 1) and (n >= 0 and n <= imgsize[1] - 1) and (m != x and n != y):
                        totalpoints = totalpoints + 1
                        if pixels[m, n] == 255:
                            colorpoints = colorpoints + 1
            if colorpoints >= pointcounts:
                temp.append(1)
            else:
                temp.append(0)
        imgpix.append(temp)
    tempimg = getGray('template.png').resize((imgsize[0], imgsize[1]))

    pixels = tempimg.load()
    for y in xrange(0, len(imgpix)):
        for x in xrange(0, len(imgpix[0])):
            if imgpix[y][x] == 0:
                pixels[x, y] = 0
            else:
                pixels[x, y] = 255
    return tempimg

# 形态学 开运算
def MorphologicalOpening(binaryimg, diskradius = 1, pointcounts = 1):
    return dilation(erosion(binimg=binaryimg, diskradius=diskradius, pointcounts=pointcounts), diskradius=diskradius, pointcounts=pointcounts)

# 形态学闭运算
def MorphologicalClose(binaryimg, diskradius = 1, pointcounts = 1):
    return erosion(dilation(binimg=binaryimg, diskradius=diskradius, pointcounts=pointcounts), diskradius=diskradius, pointcounts=pointcounts)


# 异或运算， 获取小血管坐标
# 参数：originimg：原图片
#      erosimg：处理后的图片
def xor_extractcap(originimg, erosimg):
    originimg.show()
    erosimg.show()
    o_pixels = originimg.load()
    e_pixels = erosimg.load()
    imgsize = originimg.size
    pix = []
    for y in xrange(imgsize[1]):
        temp = []
        for x in xrange(imgsize[0]):
            if e_pixels[x, y] == 255 and o_pixels == 0:
                temp.append(1)
            else:
                temp.append(0)

        pix.append(temp)

    for y in xrange(0, len(pix)):
        for x in xrange(0, len(pix[0])):
            if pix[y][x] == 0:
                e_pixels[x, y] = 0
            else:
                e_pixels[x, y] = 255
    return erosimg

# 去噪点
def removenoise(binaryimg, radius = 1, pointcounts = 2):
    pixels = binaryimg.load()
    imgsize = binaryimg.size
    pix = []
    for y in xrange(imgsize[1]):
        temp = []
        for x in xrange(imgsize[0]):
            if pixels[x, y] == 255:
                points = 0
                for m in xrange(x-radius, x+radius+1):
                    for n in xrange(y-radius, y+radius+1):
                        if (m >= 0 and m <= imgsize[0] -1) and (n >= 0 and n <= imgsize[1]-1) and (m != x and n != y):
                            if pixels[m, n] == 255:
                                points += 1
                if points >= pointcounts:
                    temp.append(1)
                else:
                    temp.append(0)
            else:
                temp.append(0)
        pix.append(temp)

    for y in xrange(len(pix)):
        for x in xrange(len(pix[0])):
            if pix[y][x] == 0:
                pixels[x, y] = 0
            else:
                pixels[x, y] = 255

    return binaryimg

if __name__ == "__main__":
    bimg = getGray("labels-ah/im0001.ah.ppm")
    # pixels = bimg.load()
    # imgsize = bimg.size
    # t = []
    # for x in xrange(imgsize[0]):
    #     s = []
    #     for y in xrange(imgsize[1]):
    #         if pixels[x, y] == 255:
    #             s.append(0)
    #         else:
    #             s.append(1)
    #     t.append(s)
    # with open('test.txt', 'wb') as txtfile:
    #     for x in xrange(len(t)):
    #         for y in xrange(len(t[0])):
    #             txtfile.write(str(t[x][y]))
    #         txtfile.write('\n')
    # erosimg = erosion(bimg, diskradius=2, pointcounts=5)
    # erosimg.show()
    # erosimg.show()
    # erosimg = erosion(erosimg, diskradius=1, pointcounts=2)
    # erosimg = removenoise(erosimg, radius=2, pointcounts=4).show()
    # dilation(erosimg, diskradius=2, pointcounts=7).show()
    # erosimg = xor_extractcap(bimg, erosimg)
    # erosimg = erosion(erosimg, diskradius=1, pointcounts=2)
    # removenoise(erosimg)
    bimg.show()
    img = MorphologicalOpening(bimg, diskradius=2, pointcounts=7)
    MorphologicalClose(img, diskradius=2, pointcounts=7).show()